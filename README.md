# Computers & Security 2025

This repository contains the code for the paper "Investigating the Impact of Label-flipping Attacks against Federated Learning for Collaborative Intrusion Detection", published in the 2025 special issue of Computers & Security: "Advances in Robust Intrusion Detection through Machine Learning".
If you use this data or the mentioned experimentation framework, please cite the following paper:

```bibtex
% Coming soon.
```

## Abstract

The recent advances in Federated Learning (FL) and its promise of privacy-preserving information sharing have led to a renewed interest in the development of collaborative models for Intrusion Detection Systems (IDSs).
However, its distributed nature makes FL vulnerable to malicious contributions from its participants, including data poisoning attacks.
Label-flipping attacks — where the labels of a subset of the training data are flipped — have been overlooked in the context of IDSs that leverage FL primitives.
This work contributes to closing this gap by providing a systematic and comprehensive overview of the impact of label-flipping attacks on Federated IDSs (FIDSs).
We show that the effects of such attacks can range from severe to highly mitigated, depending on hyperparameters and dataset characteristics, and that their mitigation is non-trivial in heterogeneous settings.
We discuss these findings in the context of existing literature and propose recommendations for the evaluation of FIDSs.
Finally, we provide a methodology and tools to extend our findings to other models and datasets, thus enabling the comparable evaluation of existing and future countermeasures.


## Usage

This repository contains pointers to access the code and results presented in the paper.
The `assessment` folder contains the notebooks used to generate the results presented in the paper, as well as the JSON files used to store the results of each experiment.

Given the size of the experiments and the amount of data generated, the saved gradients used in the "Similarity" experiment are not included in this repository, and can be downloaded from the following link: [assessment.zip](http://seafile.srcd.imta.fr/f/b70b33f286b54b7e86b0/?dl=1).

If you wish to generate the results from scratch, or extend the study to other models or datasets, please refer to the [`eiffel`](https://github.com/leolavaur/eiffel) repository which was used to generate the results presented in the paper.
