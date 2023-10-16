from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal, cast

import numpy as np
from mqt.bench.utils import calc_qubit_index, calc_supermarq_features
from mqt.predictor import Calibration
from mqt.predictor.utils import (
    get_rigetti_qubit_dict,
)

if TYPE_CHECKING:
    from qiskit import QuantumCircuit

logger = logging.getLogger("mqt-predictor")

figure_of_merit = Literal["expected_fidelity", "critical_depth"]


def crit_depth(qc: QuantumCircuit, precision: int = 10) -> float:
    """Calculates the critical depth of a given quantum circuit."""
    supermarq_features = calc_supermarq_features(qc)
    return cast(float, np.round(1 - supermarq_features.critical_depth, precision))


def expected_fidelity(qc: QuantumCircuit, device_name: str, precision: int = 10) -> float:
    """Calculates the expected fidelity of a given quantum circuit on a given device.

    Args:
        qc (QuantumCircuit): The quantum circuit to be compiled.
        device_name (str): The device to be used for compilation.
        precision (int, optional): The precision of the returned value. Defaults to 10.

    Returns:
        float: The expected fidelity of the given quantum circuit on the given device.
    """

    if "ibm" in device_name:
        res = calc_expected_fidelity_ibm(qc, device_name)

    elif "oqc_lucy" in device_name:
        res = calc_expected_fidelity_oqc_lucy(qc)

    elif "ionq" in device_name:
        res = calc_expected_fidelity_ionq(qc, device_name)

    elif "quantinuum_h2" in device_name:
        res = calc_expected_fidelity_quantinuum_h2(qc)

    elif "rigetti_aspen_m2" in device_name:
        res = calc_expected_fidelity_rigetti_aspen_m2(qc)

    else:
        error_msg = "Device not supported"
        raise ValueError(error_msg)

    return cast(float, np.round(res, precision))


def calc_expected_fidelity_rigetti_aspen_m2(qc: QuantumCircuit) -> float:
    res = 1.0
    calibration = Calibration.Calibration()

    mapping = get_rigetti_qubit_dict()
    for instruction, qargs, _cargs in qc.data:
        gate_type = instruction.name

        assert gate_type in ["rx", "rz", "cz", "measure", "barrier"]
        if gate_type != "barrier":
            assert len(qargs) in [1, 2]
            first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
            if len(qargs) == 1:
                if gate_type == "measure":
                    specific_fidelity = calibration.rigetti_m2_calibration["fid_1Q_readout"][mapping[str(first_qubit)]]
                else:
                    specific_fidelity = calibration.rigetti_m2_calibration["fid_1Q"][mapping[str(first_qubit)]]
            else:
                second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                tmp = (
                    str(
                        min(
                            int(mapping[str(first_qubit)]),
                            int(mapping[str(second_qubit)]),
                        )
                    )
                    + "-"
                    + str(
                        max(
                            int(mapping[str(first_qubit)]),
                            int(mapping[str(second_qubit)]),
                        )
                    )
                )
                if (
                    calibration.rigetti_m2_calibration["fid_2Q_CZ"].get(tmp) is None
                    or calibration.rigetti_m2_calibration["fid_2Q_CZ"][tmp] is None
                ):
                    specific_fidelity = calibration.rigetti_m2_calibration["avg_2Q"]
                else:
                    specific_fidelity = calibration.rigetti_m2_calibration["fid_2Q_CZ"][tmp]

            res *= specific_fidelity
    return res


def calc_expected_fidelity_quantinuum_h2(qc: QuantumCircuit) -> float:
    res = 1.0
    calibration = Calibration.Calibration().quantinuum_h2_calibration
    for instruction, qargs, _cargs in qc.data:
        gate_type = instruction.name
        assert gate_type in ["rzz", "rz", "ry", "rx", "measure", "barrier"]
        if gate_type != "barrier":
            assert len(qargs) in [1, 2]
            if len(qargs) == 1:
                specific_fidelity = calibration["avg_1Q"]
            elif len(qargs) == 2:
                specific_fidelity = calibration["avg_2Q"]
            res *= specific_fidelity
    return res


def calc_expected_fidelity_ionq(qc: QuantumCircuit, device_name: str) -> float:
    if device_name == "ionq_harmony":
        calibration_data = Calibration.Calibration().ionq_harmony_calibration
    elif device_name == "ionq_aria1":
        calibration_data = Calibration.Calibration().ionq_aria1_calibration
    else:
        msg = "Device not supported"
        raise ValueError(msg)

    res = 1.0
    for instruction, qargs, _cargs in qc.data:
        gate_type = instruction.name

        assert gate_type in ["rxx", "rz", "ry", "rx", "measure", "barrier"]
        if gate_type != "barrier":
            assert len(qargs) in [1, 2]
            if len(qargs) == 1:
                specific_fidelity = calibration_data["avg_1Q"]
            elif len(qargs) == 2:
                specific_fidelity = calibration_data["avg_2Q"]
            res *= specific_fidelity
    return res


def calc_expected_fidelity_oqc_lucy(qc: QuantumCircuit) -> float:
    res = 1.0
    calibration = Calibration.Calibration().oqc_lucy_calibration
    for instruction, qargs, _cargs in qc.data:
        gate_type = instruction.name

        assert gate_type in ["rz", "sx", "x", "ecr", "measure", "barrier"]
        if gate_type != "barrier":
            assert len(qargs) in [1, 2]
            first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
            if len(qargs) == 1 and gate_type != "measure":
                specific_fidelity = calibration["fid_1Q"][str(first_qubit)]
            elif len(qargs) == 1 and gate_type == "measure":
                specific_fidelity = calibration["fid_1Q_readout"][str(first_qubit)]
            elif len(qargs) == 2:
                second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                tmp = str(first_qubit) + "-" + str(second_qubit)
                if calibration["fid_2Q"].get(tmp) is None:
                    specific_fidelity = calibration["avg_2Q"]
                else:
                    specific_fidelity = calibration["fid_2Q"][tmp]

            res *= specific_fidelity
    return res


def calc_expected_fidelity_ibm(qc: QuantumCircuit, device_name: str) -> float:
    if device_name == "ibm_montreal":
        calibration = Calibration.Calibration().ibm_montreal_calibration
    elif device_name == "ibm_washington":
        calibration = Calibration.Calibration().ibm_washington_calibration
    else:
        msg = "Device not supported"
        raise ValueError(msg)

    res = 1.0
    for instruction, qargs, _cargs in qc.data:
        gate_type = instruction.name

        assert gate_type in ["rz", "sx", "x", "cx", "measure", "barrier"]

        if gate_type != "barrier":
            assert len(qargs) in [1, 2]
            first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
            if len(qargs) == 1:
                try:
                    if gate_type == "measure":
                        specific_error: float = calibration.readout_error(first_qubit)
                    else:
                        specific_error = calibration.gate_error(gate_type, [first_qubit])
                except Exception as e:
                    raise RuntimeError(
                        "Error in IBM backend.gate_error(): "
                        + str(e)
                        + ", "
                        + device_name
                        + ", "
                        + first_qubit
                        + ", "
                        + instruction
                        + ", "
                        + qargs
                    ) from None
            else:
                second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
                try:
                    specific_error = calibration.gate_error(gate_type, [first_qubit, second_qubit])
                    if specific_error == 1:
                        logger.warning(
                            "Gate error is 1.0 for: "
                            + device_name
                            + ", "
                            + gate_type
                            + ", "
                            + str(first_qubit)
                            + ", "
                            + str(second_qubit),
                            "mean error is used instead",
                        )
                        if device_name == "ibm_washington":
                            specific_error = calibration.ibm_washington_cx_mean_error
                        elif device_name == "ibm_montreal":
                            specific_error = calibration.ibm_montreal_cx_mean_error
                except Exception as e:
                    raise RuntimeError(
                        "Error in IBM backend.gate_error(): "
                        + str(e)
                        + ", "
                        + device_name
                        + ", "
                        + first_qubit
                        + ", "
                        + second_qubit
                        + ", "
                        + instruction
                        + ", "
                        + qargs
                    ) from None

            res *= 1 - specific_error
    return res
