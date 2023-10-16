import re
import traceback
from .qasm import *
from .const import Const
from typing import List, Optional, Union, Dict, Tuple


class QasmToQcis(object):
    def __init__(self):
        self.qasm_filter = ['OPENQASM', 'include', 'creg', '#', '']
        self.with_param_qcis = ['RX', 'RY', 'RZ']
        self.config_dir_json = None
        self.const = Const()

    def get_gate_by_name(self, gate_name):
        gate = globals()[gate_name]
        return gate

    def convert_qasm_to_qcis_from_file(
            self,
            qasm_file: str,
            qubit_list: Optional[List[str]] = None,
            qubit_map: Optional[Dict] = None):
        """read qasm from file and convert to qcis

        Args:
            qasm_file: qasm file name
            qubit_list: qubit list. when the value is None, based on the qubit in grep. Defaults to None.
            qubit_map: qubit map. Use this value as a qubit when it is not empty mapping.Defaults to None.

        Returns:
            str: return the converted qasm.
        """
        with open(qasm_file, 'r') as qasm_f:
            qasm = qasm_f.readlines()
        qasm = ''.join(qasm)
        return self.convert_qasm_to_qcis(qasm, qubit_list, qubit_map)

    def find_creq_by_qasm(
            self,
            measure_qasm: str):
        """find the number in creq

        Args:
            measure_qasm: measure qasm

        Returns:
            List[str]: number in creq
        """
        qubit_idx = re.findall(r'c\[(\d+)\]', measure_qasm)
        return qubit_idx

    def find_qubit_by_qasm(
            self,
            measure_qasm: str):
        """find the number in grep

        Args:
            measure_qasm: measure qasm

        Returns:
            List[str]: number in grep
        """
        qubit_idx = re.findall(r'q\[(\d+)\]', measure_qasm)
        return qubit_idx

    def convert_qasm_to_qcis(
            self,
            qasm: str,
            qubit_list: Optional[List[str]] = None,
            qubit_map: Optional[Dict] = None):
        """convert qasm to qcis

        Args:
            qasm: qasm
            qubit_list: qubit list. when the value is None, based on the qubit in grep. Defaults to None.
            qubit_map: qubit map. Use this value as a qubit when it is not empty mapping.Defaults to None.

        Returns:
            str: return the converted qcis.
        """
        qcis = ""
        measure_qcis = ""
        n_qubit = 0
        qasm_instruction_list = qasm.split('\n')
        qasm_instruction_list = [
            inst.strip() for inst in qasm_instruction_list if qasm.strip()]
        qasm_instruction_iter = iter(qasm_instruction_list)
        index = 0
        while index < len(qasm_instruction_list):
            qasm_instr = qasm_instruction_list[index]
            try:
                if '(' in qasm_instr:
                    qasm_gate = re.findall(r'(.+(?=\())', qasm_instr)[0]
                else:
                    qasm_gate = qasm_instr.split(' ')[0]
                if qasm_gate in self.qasm_filter:
                    index += 1
                    continue
                elif qasm_instr.startswith('qreg'):
                    n_qubit = re.findall(r'\d+', qasm_instr)[0]
                    n_qubit = int(n_qubit)
                    if qubit_list and len(qubit_list) != n_qubit:
                        print(f"qubit_list should have {n_qubit} indices,\
                                {len(qubit_list)} are given")
                    else:
                        qubit_list = list(range(0, n_qubit))
                    index += 1
                    continue
                elif qasm_instr.startswith('measure'):
                    measure_qcis += f'{qasm_instr}'
                    index += 1
                    continue
                if qasm_gate == 'h' and 'barrier' not in qasm_instruction_list[index+1]:
                    com_qasm = qasm_instruction_list[index: index + 3]
                    if '' not in com_qasm:
                        com_qasm_gate = '_'.join(
                            [com.split(' ')[0] for com in com_qasm])
                        com_qubit_list = [
                            re.findall(r'q\[(\d+)\]', com)[0] for com in com_qasm]
                        if len(set(com_qubit_list)) == 1 and com_qasm_gate in globals():
                            com_qasm_instr = '\n'.join(com_qasm)
                            gate = self.get_gate_by_name(com_qasm_gate)(
                                com_qasm_instr, qubit_list, qubit_map)
                            qcis += gate.__str__()
                            next(qasm_instruction_iter)
                            next(qasm_instruction_iter)
                            index += 3
                            continue
                gate = self.get_gate_by_name(qasm_gate)(
                    qasm_instr, qubit_list, qubit_map)
                qcis += gate.__str__()
                index += 1
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print('QCIS failed to be translated,' +
                      f'currect instruction is {qasm_instr}' +
                      'please check your qasm')
                return ''
        measure_idx = self.find_creq_by_qasm(measure_qcis)
        measure_dir = {idx: int(i) for idx, i in enumerate(measure_idx)}
        measure_dir = dict(sorted(measure_dir.items(), key=lambda x: x[1]))
        measure_qcis_list = measure_qcis.split(";")
        for idx in measure_dir:
            m = measure_qcis_list[idx]
            qubit_idx = self.find_qubit_by_qasm(m)
            if qubit_map:
                qcis += f"M {qubit_map.get(qubit_idx[0])}\n"
            else:
                qcis += f'M Q{qubit_list[int(qubit_idx[0])]}\n'
        return qcis

    def repeat_count(self, qcis_list):
        groups = []
        for i, val in enumerate(qcis_list):
            if i == 0:
                cnt = 1
                loc = i
                last_val = val
            elif val == last_val:
                cnt += 1
            else:
                groups.append((cnt, last_val, loc))
                cnt = 1
                loc = i
                last_val = val
        repeat_groups = groups.copy()
        for g in groups:
            if g[0] == 1:
                repeat_groups.remove(g)
        return repeat_groups

    def json_file(self):
        return self.const.qasm2qcis

    def repeat(self, qcis_instruction_list, circuit_simplify):
        index_to_delete = []
        qcis_list_copy = qcis_instruction_list.copy()
        for index, qcis in enumerate(qcis_instruction_list):
            if any(p if p in qcis else False for p in self.with_param_qcis):
                qcis_list_copy[index] = ' '.join(qcis.split(' ')[:2])

        groups = self.repeat_count(qcis_list_copy)
        repeat = circuit_simplify.get('repeat')
        for group in groups:
            num, _qcis, index = group
            if num == 1:
                continue
            is_param_qcis = any(
                p if p in _qcis else False for p in self.with_param_qcis)
            com_qcis = _qcis.split(' ')[0]
            repeat_qubit = _qcis.split(' ')[1]
            if com_qcis not in repeat:
                continue
            repeat_info = repeat.get(com_qcis)
            if isinstance(repeat_info, list):
                repeat_num = repeat_info[0]
                repeat_qcis = repeat_info[1]
                if is_param_qcis:
                    num = num if repeat_num == 'n' else 2
                    param_qcis_list = qcis_instruction_list[index: index + num]
                    params = sum(
                        [float(re.findall(r'\s([+-]?[0-9]\d*\.?\d*|0\.\d*[1-9])', r)[0]) for r in param_qcis_list])
                    qcis_instruction_list[index] = f'{repeat_qcis} {repeat_qubit} {params}'
                    index_to_delete.extend([index + i for i in range(1, num)])
            else:
                num_range = num // 2
                if num_range > 1:
                    for i in range(num_range):
                        if repeat_info != 'I':
                            qcis_instruction_list[index +
                                                  (i * 2)] = f'{repeat_info} {repeat_qubit}'
                        index_to_delete.extend([index + (i * 2) + 1])
                else:
                    if repeat_info != 'I':
                        qcis_instruction_list[index] = f'{repeat_info} {repeat_qubit}'
                    index_to_delete.extend([index + 1])
        return index_to_delete

    def simplify(
            self,
            qcis_raw: str):
        """qcis line optimization

        Args:
            qcis_raw: qics

        Returns:
            str: return the optimized qcis.
        """
        qcis_instruction_list = qcis_raw.split('\n')
        circuit_simplify = self.json_file().get('circuit_simplify')
        index_to_delete = []
        for k, v in circuit_simplify.items():
            to_delete = getattr(self, k)(
                qcis_instruction_list, circuit_simplify)
            index_to_delete.extend(to_delete)

        qcis_instruction_list = [qcis_instruction_list[i] for i in range(
            0, len(qcis_instruction_list), 1) if i not in index_to_delete]
        return '\n'.join(qcis_instruction_list)
