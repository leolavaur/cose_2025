# Computers & Security 2024

This repository contains the code for the paper "Investigating the Impact of Label-flipping Attacks against Federated Intrusion Detection Systems", submitted to the December 2024 special issue of Computers & Security: "Advances in Robust Intrusion Detection through Machine Learning".
If you use this code, please cite the following paper:

```bibtex
% Coming soon.
```

## Abstract

The recent advances in Federated Learning (FL) and its promise of privacy-preserving information sharing have led to a renewed interest in the development of collaborative models for Intrusion Detection Systems (IDS).
However, its distributed nature makes FL vulnerable to malicious contributions from its participants, including data poisoning attacks.
Label-flipping attacks---where the labels of a subset of the training data are flipped---have been overlooked in the context of IDSs that leverage FL primitives.
This work contributes in closing this gap by providing a systematic and comprehensive overview of the impact of label-flipping attacks on Federated Intrusion Detection Systems (FIDS=).
We show that the effects of such attacks can range from severe to highly mitigated, depending on hyperparameters and dataset characteristics, and that their mitigation is non-trivial in heterogeneous settings.
Furthermore, we provide a methodology and tools to extend our findings to other models and datasets, thus enabling the comparable evaluation of existing and future countermeasures.


## Usage

This repository contains pointers to access the code and results presented in the paper.
Given the sheer size of the experiments, and the amount of data generated, the results themselves are hosted on a second support:

> At the time, you can access the results from my experiments monorepo: [FL-IDS/exps/assessment](https://github.com/leolavaur/fl-ids/tree/main/exps/assessment). Note that this subject to change.

If you wish to generate the results from scratch, or extend the study to other models or datasets, please refer to the [`eiffel`](https://github.com/leolavaur/eiffel) repository for more information.

## License

This code is released under the MIT License. See the `LICENSE` file for more information.
