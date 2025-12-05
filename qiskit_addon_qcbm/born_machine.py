# This code is a QAMP project based on Qiskit.
"""Define the Quantum Circuit Born Machine."""

from qiskit import QuantumCircuit
from qiskit.circuit.library import efficient_su2


class QCBM:
    """Quantum Circuit Born Machine"""

    def __init__(self, num_qubits, num_layers, ansatz=None):
        self.num_layers = num_layers
        if isinstance(ansatz, QuantumCircuit):
            self.qcbm = ansatz
        else:
            self.qcbm = efficient_su2(num_qubits, reps=num_layers)

    def train(self, loss_fcn=None):
        """Train the QCBM."""
        print(f"""The QCBM has: 
              {self.qcbm.num_qubits} qubits,
              {self.num_layers} layers,
              and a depth of {self.qcbm.depth()}.""")
