# This code is a QAMP project based on Qiskit.
"""Define the Quantum Circuit Born Machine."""

from qiskit import QuantumCircuit
from qiskit.circuit.library import efficient_su2
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer.primitives import SamplerV2 as AerSamplerV2
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeFez

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from qiskit_addon_qcbm.datasets import MixtureGaussianData


class QCBM:
    """Quantum Circuit Born Machine"""

    def __init__(self, num_qubits, num_layers, ansatz=None, data=None):
        self.num_layers = num_layers
        self.num_qubits = num_qubits
        if isinstance(ansatz, QuantumCircuit):
            self.qcbm = ansatz
        else:
            self.qcbm = efficient_su2(num_qubits, reps=num_layers)
            self.qcbm.measure_all()
        self.data = data

    def draw(self, ):
        """Draw the QCBM circuit."""

        display(self.qcbm.draw("mpl"))


    def print(self, ):
        """Provide the stats on the QCBM."""

        print(f"""The QCBM has: 
              {self.qcbm.num_qubits} qubits,
              {self.num_layers} layers,
              {self.qcbm.num_parameters} parameters,
              depth of {self.qcbm.depth()}, and
              data of length {len(self.data)}.""")

    def train(self, data=None, loss_fcn=None, num_iterations=10, num_shots=100, backend=FakeFez()):
        """Train the QCBM."""

        if self.data is None and data is None:
            raise TypeError("data must be other than None.")
        elif data is not None:
            self.data = data

        self.backend = backend

        if loss_fcn is None:
        # Use the MMD^2 to calculate the loss
            # Radial Basis Function Sigma values
            rbf_sigmas = np.array([0.25, 60])
            # An array whose elements are 0 to (Hilbert dim - 1)
            nparange_hilbert_dim = np.arange(2**self.num_qubits)

            mmd = MMD(rbf_sigmas, nparange_hilbert_dim)
            loss_fcn = mmd.mmd_loss

        self.train_history = {
            "divergence": [],
            "iterations": 0,
            "loss": [],            
            "num_shots": num_shots,
            "prev_params": None,            
        }
    
        ansatz_params = 2 * np.pi * np.random.random(self.qcbm.num_parameters)

        sampler = Sampler(mode=self.backend, options={"default_shots": num_shots})

        pm = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        self.ansatz_isa = pm.run(self.qcbm)
  
        self.target_probs = data
        # target_probs = MixtureGaussianData.mixture_gaussian_pdf(x, mus, sigmas)

        result = minimize(
            self.compute_loss,
            ansatz_params,
            args=(self.ansatz_isa, sampler, loss_fcn, self.train_history, self.target_probs),
            method="cobyla",
            options={"maxiter": num_iterations}
        )

        x_max = 2**self.num_qubits

        counts_dict = self.train_history["counts_dict"]
        qcbm_probs = np.zeros(2**self.num_qubits)          
        sum_counts = sum(counts_dict.values())  
        for value, count in counts_dict.items():
            index = int(value, 2)
            qcbm_probs[index] = count/sum_counts

        self.plot_compare_model_and_target_probs(x_max, self.target_probs, qcbm_probs)

        return self.train_history

    def compute_loss(self, params, ansatz_isa, sampler, loss_fcn, train_history, target_probs):
        """Return the value of the loss function.

        Parameters:
            params (ndarray): Array of ansatz parameters
            ansatz_isa (QuantumCircuit): Parameterized transpiled ansatz circuit
            sampler (SamplerV2): Sampler primitive instance
            loss_fcn (python function): Function using to compute the loss, aka cost
            train_history (dict): Dictionary for storing intermediate results
            target_probs (ndarray): the actual probability distribution
                 
        Returns:
            float: Scalar loss value
        """
        pub = (ansatz_isa, [params]) # params is a numpy array, we need a list for the PUB format

        # Run the sampler job
        job = sampler.run([pub])
        result = job.result()
    
        # Get the data for the first (and only) PUB
        pub_result = result[0]
        counts_dict = pub_result.data.meas.get_counts()

        qcbm_probs = np.zeros(2**self.num_qubits)          
        sum_counts = sum(counts_dict.values())  
        for value, count in counts_dict.items():
            index = int(value, 2)
            qcbm_probs[index] = count/sum_counts

        if train_history["iterations"] == 0:
            print("sum of counts:", sum_counts)
            print("num shots:", sampler.options.default_shots)
            plt.plot(qcbm_probs, label="qcbm")
            plt.plot(target_probs, label="target")
            plt.xlabel("Bitstring as Integer Value")
            plt.ylabel("Probability")            
            plt.legend()
            plt.show()

        loss = loss_fcn(qcbm_probs, target_probs)

        print(f"Iters. done: {train_history['iterations']} [Current cost: {loss}]")

        train_history["iterations"] += 1
        train_history["loss"].append(loss)
        train_history["prev_params"] = params            
        train_history["counts_dict"] = counts_dict

        return loss
        
    def plot_compare_model_and_target_probs(self, x_max, target_probs, qcbm_probs):
        """Compare the probabilities obtained with QCBM with the actual probability distribution."""
        
        plt.plot(range(x_max), target_probs, linestyle="-.", label="target")
        plt.bar(range(x_max), qcbm_probs, color="green", alpha=0.5, label="qcbm")

        plt.xlabel("Bitstring as Integer Value")
        plt.ylabel("Probability")

        plt.legend()
        plt.show()

        return None


class MMD:
    """Maximum Mean Discrepancy"""

    def __init__(self, rbf_sigmas, nparange_hilbert_dim):
        gammas = 1 / (2 * (rbf_sigmas**2))
        sq_dists = np.abs(nparange_hilbert_dim[:, None] - nparange_hilbert_dim[None, :]) ** 2
        self.K = sum(np.exp(-gamma * sq_dists) for gamma in gammas) / len(rbf_sigmas)
        self.rbf_sigmas = rbf_sigmas

    def k_expval(self, px, py):
        # Kernel expectation value
        return px @ self.K @ py

    def mmd_loss(self, px, py):
        pxy = px - py
        return self.k_expval(pxy, pxy)
    