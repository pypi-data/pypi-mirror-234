import numpy as np
import re
import random
from .const import Const


class BaseUtil():
    def __init__(self, qasm, qubit_list, qubit_map=None):
        self.qasm2qcis = self.json_file()
        self.single_gate = self.qasm2qcis.get('single_gate')
        self.couper_gate = self.qasm2qcis.get('couper_gate')
        self.qasm = qasm
        self.qubit_list = qubit_list
        self.qubit_map = qubit_map

    def json_file(self):
        self.const = Const()
        return self.const.qasm2qcis

    def find_qubit_by_qasm(self):
        qubit_idx = re.findall(r'q\[(\d+)\]', self.qasm)
        if self.qubit_map is None:
            qubit_idx = [self.qubit_list[int(idx)] for idx in qubit_idx]
        else:
            qubit_idx = [self.qubit_map[idx].replace(
                'Q', '') for idx in qubit_idx]
        return qubit_idx

    def find_param_by_qasm(self):
        """qasm parameters for door operation,
           example:
            rx(0) q[0]; Find the content in parentheses ['0']
            u(0.124, 0.562. -0.86) q[0]; Find the content in parentheses ['0.124, 0.562. -0.86']

        Returns:
            list: return to Findings
        """
        param_result = re.findall(r'\((.*)\)', self.qasm)
        return param_result

    def find_param_index_by_qasm(
            self,
            single_qasm: str):
        """find the data for filling in the parameter index based on the converted qcis in JSON

           example:
            RZ [1];find the corresponding ['1']
            RZ [1] [2];find the corresponding ['1', '2']

        Args:
            single_qasm (str): qcis converted in a single JSON

        Returns:
            list: return to Findings
        """
        param_index = re.findall(r'\[(\d+)\]', single_qasm)
        return param_index

    def find_after_param_gate(self, coupler_qasm):
        gate_result = re.findall(r'(.+(?=\())', coupler_qasm)
        return gate_result

    def check_gate(self, class_name):
        if class_name in self.single_gate:
            return True
        else:
            return False

    def __str__(self):
        """process qasm conversion to qcis

        Returns:
            qics: converted qcis
        """
        qcis = ''
        class_name = self.__class__.__name__
        check_result = self.check_gate(class_name)
        param_result = self.find_param_by_qasm()
        if len(param_result) > 0:
            param_result = param_result[0].split(',')
            param_result = [str(eval(param.replace('pi', 'np.pi').strip(
            ))) if 'pi' in param else str(eval(param.strip())) for param in param_result]
        if check_result:
            qcis_gate = self.single_gate.get(class_name)
            qubit_idx = self.find_qubit_by_qasm()
            if class_name == 'barrier':
                if not qubit_idx:
                    qubit_idx = ' '.join([f'Q{i}' for i in self.qubit_list])
                else:
                    qubit_idx = ' '.join([f'Q{i}' for i in qubit_idx])
                qcis += f'''B {qubit_idx}\n'''
            elif isinstance(qcis_gate, str):
                param_index = self.find_param_index_by_qasm(qcis_gate)
                if len(param_index) > 0:
                    gate = qcis_gate.split(' ')[0]
                    qcis += f'{gate} Q{qubit_idx[0]} ' +\
                            f'{param_result[int(param_index[0])]}\n'
                else:
                    qcis += f'{qcis_gate} Q{qubit_idx[0]}\n'
            elif isinstance(qcis_gate, dict):
                new_qcis = qcis_gate.get(random.sample(qcis_gate.keys(), 1)[0])
                for q in new_qcis:
                    qcis += f'{q} Q{qubit_idx[0]}\n'
            elif isinstance(qcis_gate, list):
                for q in qcis_gate:
                    param_index = self.find_param_index_by_qasm(q)
                    if len(param_index) > 0:
                        gate = q.split(' ')[0]
                        qcis += f'{gate} Q{qubit_idx[0]} ' +\
                                f'{param_result[int(param_index[0])]}\n'
                    else:
                        qcis += f'{q} Q{qubit_idx[0]}\n'
        else:
            qcis_gate = self.couper_gate.get(class_name)
            qubit_idx = self.find_qubit_by_qasm()
            coupler_list = [f'Q{idx}' for idx in qubit_idx]
            for q in qcis_gate:
                if isinstance(q, str):
                    param_index = self.find_param_index_by_qasm(q)
                    if len(param_index) > 0:
                        q_index = q.split(' ')[1]
                        gate = q.split(' ')[0]
                        for param in param_index:
                            q = q.replace(
                                f'[{param}]', param_result[int(param)])
                        qcis_param = q.split(' ')[2]
                        qcis += f'{gate} Q{qubit_idx[int(q_index)]} ' +\
                                f'{eval(qcis_param)}\n'
                    else:
                        gate = q.split(' ')[:1]
                        idx = q.split(' ')[1:]
                        for i in idx:
                            gate.append(coupler_list[int(i)])
                        gate = ' '.join(gate)
                        qcis += f'{gate}\n'
                elif isinstance(q, dict):
                    if 'single_gate' in q:
                        qcis_gate = q.get('single_gate')
                    else:
                        qcis_gate = q.get('couper_gate')
                    param_index = self.find_param_index_by_qasm(qcis_gate)
                    if len(param_index) > 0:
                        gate = qcis_gate.split(' ')[0]
                        for param in param_index:
                            qcis_gate = qcis_gate.replace(
                                f'[{param}]', param_result[int(param)])
                        q_gate = re.findall(r'([a-z]+)', qcis_gate)[0]
                    else:
                        q_gate = qcis_gate.split(' ')[0]
                    gate = qcis_gate.split(' ')[:1]

                    idx_list = re.findall(r'q\[\d+\]', self.qasm)
                    idx = qcis_gate.split(' ')[1:]
                    for i in idx:
                        gate.append(idx_list[int(i)])
                    gate = ' '.join(gate)
                    g = globals().get(q_gate)(gate, self.qubit_list, self.qubit_map)
                    qcis += str(g)
        return qcis


def create_instruction_class(name, load_to_scope=False):
    cls = type(name, (BaseUtil,), {})
    if load_to_scope:
        scope = globals()
        if name not in scope:
            scope[name] = cls
    return cls


def load_qasm_classes():
    qcis_instructions = [
        'x', 'y', 'z', 'h', 'sx', 'sxdg', 'h_sx_h', 'h_sxdg_h',
        's', 'sdg', 't', 'tdg', 'rx', 'ry', 'rz', 'u', 'u2', 'u1',
        'cx', 'cz', 'cy', 'ch', 'swap', 'crz', 'cp', 'ccx', 'cu3', 'barrier']

    class_list = []
    for name in qcis_instructions:
        cls = create_instruction_class(name)
        class_list.append(cls)
    return class_list, qcis_instructions


(x, y, z, h, sx, sxdg,
 h_sx_h, h_sxdg_h,
 s, sdg, t, tdg,
 rx, ry, rz, u, u2, u1,
 cx, cz, cy, ch,
 swap, crz, cp, ccx, cu3, barrier), _QCIS_INSTRUCTIONS = load_qasm_classes()
