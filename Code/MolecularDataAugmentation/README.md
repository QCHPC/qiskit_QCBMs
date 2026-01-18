## Generation of synthetic data via the STONED-SELFIES algorithm


### Exploration of the chemical space of neighborhoods of known of KRAS inhibitors. 


This notebook builds upon some of the code and ideas developed in <a href="https://github.com/aspuru-guzik-group/quantum-generative-models">/aspuru-guzik-group/quantum-generative-models/ </a> (esp. the script `stoned_sim.py` within `stoned_algorithm`). See also  <a href="https://www.nature.com/articles/s41587-024-02526-3"> Nature Reports s41587-024-02526-3 </a> and  <a href="https://arxiv.org/abs/2402.08210">arXiv/2402.08210 </a> for the more thorough arXiv version. 

This computation is just an example meant to provide a small training dataset. Starting with 643 molecules we augment the dataset to 6430 molecules by generating N = 9 viable mutations neighboring each of the original molecules. The parameter N can be adjusted according to the needs of a given workflow. This parameter determines the size of the training dataset used further in the pipeline. For a full workflow with enough resources similar to the one in the article one would use N ~ 1000. 

The datasets include only the SMILES and SELFIES  formats for each molecule. For training hybrid algorithms their `fingerprints` can be used (fingerprints are sparse vector representations of molecules cf. Section 4 in the notebook).
