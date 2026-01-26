# Quantum Circuit Born Machine (QCBM) for Molecular Generation

This notebook implements a hybrid quantum–classical molecular generation pipeline
using a Quantum Circuit Born Machine (QCBM). Molecules are represented in a chemically
meaningful latent space derived from SELFIES tokens, enabling valid quantum learning
and sampling.

This notebook builds upon several ideas and code components developed in  
<a href="https://github.com/aspuru-guzik-group/quantum-generative-models">aspuru-guzik-group/quantum-generative-models</a>,  
in particular the script `stoned_sim.py` within the `stoned_algorithm` module.

Related scientific references include:  
- <a href="https://www.nature.com/articles/s41587-024-02526-3">Nature Reports s41587-024-02526-3</a>  
- <a href="https://arxiv.org/abs/2402.08210">arXiv:2402.08210</a> (extended technical version)

The `syba` module used for synthetic accessibility scoring has been imported from  
<a href="https://github.com/lich-uct/syba">lich-uct/syba</a>.

The files `syba.csv.gz` and `syba4.csv.gz` were obtained from  
<a href="https://anaconda.org/LICH/syba/files">anaconda.org/LICH/syba/files</a>.

This notebook additionally makes use of the `QCBM.distribution_metrics` module, developed by:

Natalie Hawkins  
Quantum Algorithms and Applications  
QuantumBits  
Seattle, WA  

and  

Jorge Plazas  
Escuela Politécnica Superior  
Universidad Francisco de Vitoria  
Madrid, Spain  

and  

Debshata Choudhury  
BS Data Science, IIT Madras  
B.Tech Computer Science, ASET Noida  
New Delhi, India  

as part of IBM QAMP 2025.

The source code for the `distribution_metrics` module is available at:  
<a href="https://github.com/jorgeplazas/Qiskit-QCBMs/blob/main/Code/distribution_metrics.py">
https://github.com/jorgeplazas/Qiskit-QCBMs/blob/main/Code/distribution_metrics.py
</a>

<div align="center">

## QCBM–Driven Molecular Generation Pipeline

**Raw chemical data**  
$\downarrow$  

**SMILES strings (KRAS inhibitors dataset)**  
$\downarrow$  

**SELFIES encoding**  
(guaranteed syntactic validity of molecular strings)  
$\downarrow$  

**Latent chemical representation**  
(SELFIES token-count vectors, dimension = 32)  
$\downarrow$  

**Target probability distribution**  
$p_{\text{target}}(i) = \dfrac{\|x_i\|}{\sum_j \|x_j\|}$  
where $x_i$ is the latent vector of molecule $i$  
$\downarrow$  

**QCBM training objective**  
Minimize distribution mismatch  
$\downarrow$  

**Loss functions**  

Maximum Mean Discrepancy (MMD)  
$$
\text{MMD}^2(p,q)=\mathbb{E}_{x,x'\sim p}[k(x,x')] + \mathbb{E}_{y,y'\sim q}[k(y,y')] - 2\mathbb{E}_{x\sim p,y\sim q}[k(x,y)]
$$  

Sinkhorn distance (entropy-regularized optimal transport)  
$$
W_\varepsilon(p,q)
$$  
$\downarrow$  

**Trained QCBM distribution**  
$p_{\text{QCBM}} \approx p_{\text{target}}$  
$\downarrow$  

**Sampling from quantum distribution**  
$m \sim p_{\text{QCBM}}$  
$\downarrow$  

**Nearest-neighbor decoding in latent space**  
(cosine similarity)  
$\downarrow$  

**SELFIES → SMILES decoding**  
$\downarrow$  

**RDKit sanitization**  
(chemical validity enforcement)  
$\downarrow$  

**SYBA synthetic accessibility filtering**  
Retain molecules satisfying  
$$
\text{SYBA score} > 0
$$  
$\downarrow$  

**Final output**  

Chemically valid, synthetically accessible  
QCBM-generated molecules with:  

• quantum probability  
• latent similarity  
• SYBA score  

</div>
