# This code is a QAMP project based on Qiskit.
"""Tests for the QCBM submodule."""

from qiskit_addon_qcbm.born_machine import QCBM


# Test: QCBM Creation
def test_QCBM_Creation():
    qcbm = QCBM(num_qubits=4, num_layers=3)

    assert qcbm.num_qubits == 4
    assert qcbm.num_layers == 3
