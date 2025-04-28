import operator

import numpy as np
import pandas as pd
from eiffel.datasets.dataset import Dataset
from eiffel.datasets.partitioners import (
    IIDPartitioner,
    NIIDClassPartitioner,
    Partitioner,
)
from flwr.common import FitRes, parameters_to_ndarrays
from flwr.server.client_proxy import ClientProxy
from flwr.server.strategy import FedAvg
from sklearn.cluster import KMeans


class AttackPartitioner(NIIDClassPartitioner):
    """Custom partitioner reproducing partitioning for all attackers.

    In the current version of `eiffel`, attackers in a `Pool` object are not taken into
    consideration. However, `Partitioner` objects return a `list`, thereby preserving
    the shards' order. Since `Pool`s instanciate benign clients first and use
    `list.pop` to select the shard to assign, the attackers shards must be placed at the
    begining of the list provided by the `all` method.
    """

    def __init__(
        self,
        *args,
        n_attackers: int = 0,
        benign_strategy: str = "iid",
        attacker_target: list[str] | None,
        **kwargs,
    ) -> None:
        """Initialize the AttackPartitioner.

        For reference on the other parameters, see the `NIIDClassPartitioner`,
        `IIDPartitioner` and `Partitioner` classes.

        Parameters
        ----------
        n_attackers : int
            Number of attackers in the dataset.
        benign_strategy : str
            Strategy to use for benign clients, either `iid` or `kmeans`. Defaults to
            `iid`.
        """
        super().__init__(*args, **kwargs)
        self.n_attackers = n_attackers
        self.benign_strategy = benign_strategy
        self.attacker_target = attacker_target

    def _partition(self, dataset: Dataset) -> None:
        """Partition the dataset."""

        # Partition benign samples

        benign_set = dataset[dataset.y == 0]
        benign_shards: list[Dataset] = []

        if self.benign_strategy == "iid":
            pt = IIDPartitioner(
                class_column=self.class_column,
                n_partitions=self.n_partitions,
                seed=self.seed,
            )
        elif self.benign_strategy == "kmeans":
            pt = KMeansPartitioner(
                n_partitions=self.n_partitions,
                seed=self.seed,
            )
        else:
            raise ValueError(
                f"Unsuported strategy '{self.benign_strategy}' for benign samples"
                " partitioning. Supported strategies are 'iid' and 'kmeans'."
            )

        pt.load(benign_set)
        benign_shards = pt.all()

        # Partition malicious samples

        malicious_set = dataset[dataset.y == 1]
        malicious_shards: list[Dataset] = []

        if self.n_attackers > 0:

            frac = self.n_attackers / self.n_partitions
            poisoned_malicious_set, legit_malicious_set = malicious_set.split(
                at=frac, seed=self.seed
            )

            pt = NIIDClassPartitioner(
                class_column=self.class_column,
                # All attackers must have the target class available in their training datasets.
                preserved_classes=self.preserved_classes + (self.attacker_target or []),
                n_partitions=self.n_attackers,
                n_drop=self.n_drop,
                n_keep=self.n_keep,
                df_key=self.df_key,
                seed=self.seed,
            )
            pt.load(poisoned_malicious_set)
            malicious_shards = pt.all()

            malicious_set = legit_malicious_set

        pt = NIIDClassPartitioner(
            class_column=self.class_column,
            preserved_classes=self.preserved_classes,
            n_partitions=self.n_partitions - self.n_attackers,
            n_drop=self.n_drop,
            n_keep=self.n_keep,
            df_key=self.df_key,
            seed=self.seed,
        )
        pt.load(malicious_set)
        malicious_shards += pt.all()

        # Combine benign and malicious shards

        shards = list(map(operator.add, malicious_shards, benign_shards))

        self.partitions = shards


class KMeansPartitioner(Partitioner):
    """Partitioner using KMeans clustering.

    This partitioner uses KMeans clustering to partition the dataset into `n_partitions`
    shards. The clustering is performed on the features of the dataset.
    """

    def _partition(self, dataset: Dataset) -> None:
        """Partition the dataset."""
        kmeans = KMeans(n_clusters=self.n_partitions, random_state=self.seed)
        kmeans.fit(dataset.X)
        clusters = kmeans.predict(dataset.X)

        self.partitions = [dataset[clusters == i] for i in range(self.n_partitions)]


class SaveFedAvg(FedAvg):
    """Strategy to save models after each round.

    Models are stored in a `pandas.DataFrame` which is then saved to a file in the
    current working directory at the end of each round.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the SaveFedAvg strategy."""
        super().__init__(*args, **kwargs)
        if self.initial_parameters is None:
            raise ValueError("The initial parameters must be provided.")
        self.last_params: list[np.ndarray] = parameters_to_ndarrays(
            self.initial_parameters
        )

    def aggregate_fit(
        self,
        server_round: int,
        results: list[tuple[ClientProxy, FitRes]],
        failures: list[tuple[ClientProxy, FitRes] | BaseException],
    ):
        """Aggregate the fit results."""

        models = pd.DataFrame(columns=["Client", "Round", "Model"])
        grads = pd.DataFrame(columns=["Client", "Round", "Gradients"])

        for client, fit_res in results:
            flatten_model = np.concatenate(
                [a.ravel() for a in parameters_to_ndarrays(fit_res.parameters)]
            )
            models = pd.concat([
                models,
                pd.DataFrame({
                    "Client": [client.cid],
                    "Round": [server_round],
                    "Model": [flatten_model],
                }),
            ])
            flatten_last_params = np.concatenate([a.ravel() for a in self.last_params])
            grads = pd.concat([
                grads,
                pd.DataFrame({
                    "Client": [client.cid],
                    "Round": [server_round],
                    "Gradients": [flatten_model - flatten_last_params],
                }),
            ])

        # models.to_pickle(f"models_r{server_round}.pkl")
        grads.to_pickle(f"grads_r{server_round}.pkl")

        params, config = super().aggregate_fit(server_round, results, failures)
        self.last_params = parameters_to_ndarrays(params)
        return params, config
