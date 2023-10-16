class Const():
    qasm2qcis = {
        "single_gate": {
            "x": "X",
            "y": "Y",
            "z": "Z",
            "h": {
                "0": [
                    "Y2M",
                    "Z"
                ],
                "1": [
                    "Z",
                    "Y2P"
                ]
            },
            "sx": "X2P",
            "sxdg": "X2M",
            "h_sx_h": "Y2P",
            "h_sxdg_h": "Y2M",
            "s": "S",
            "sdg": "SD",
            "t": "T",
            "tdg": "TD",
            "rx": [
                "Y2M",
                "RZ [0]",
                "Y2P"
            ],
            "ry": [
                "X2P",
                "RZ [0]",
                "X2M"
            ],
            "rz": "RZ [0]",
            "u": [
                "RZ [1]",
                "X2P",
                "RZ [0]",
                "X2M",
                "RZ [2]"
            ],
            "u2": [
                "RZ [0]",
                "Y2P",
                "RZ [1]"
            ],
            "u1": "RZ [0]",
            "barrier": "B"
        },
        "couper_gate": {
            "cx": [
                "Y2M 1",
                "CZ 0 1",
                "Y2P 1"
            ],
            "cz": ["CZ 0 1"],
            "cy": [
                "X2P 1",
                "CZ 0 1",
                "X2M 1"
            ],
            "ch": [
                "S 1",
                {
                    "single_gate": "h 1"
                },
                "T 1",
                {
                    "couper_gate": "cx 0 1"
                },
                "TD 1",
                {
                    "single_gate": "h 1"
                },
                "SD 1"
            ],
            "swap": [
                {
                    "couper_gate": "cx 0 1"
                },
                {
                    "couper_gate": "cx 1 0"
                },
                {
                    "couper_gate": "cx 0 1"
                }
            ],
            "crz": [
                "RZ 1 [0]/2",
                {
                    "couper_gate": "cx 0 1"
                },
                "RZ 1 -[0]/2",
                {
                    "couper_gate": "cx 0 1"
                }
            ],
            "cp": [
                "RZ 0 [0]/2",
                {
                    "couper_gate": "crz([0]) 0 1"
                }
            ],
            "ccx": [
                {
                    "single_gate": "h 2"
                },
                {
                    "couper_gate": "cx 1 2"
                },
                "TD 2",
                {
                    "couper_gate": "cx 0 2"
                },
                "T 2",
                {
                    "couper_gate": "cx 1 2"
                },
                "TD 2",
                {
                    "couper_gate": "cx 0 2"
                },
                "T 1",
                "T 2",
                {
                    "single_gate": "h 2"
                },
                {
                    "couper_gate": "cx 0 1"
                },
                "T 0",
                "TD 1",
                {
                    "couper_gate": "cx 0 1"
                }
            ],
            "cu3": [
                "RZ 1 ([1]-[2])/2",
                {
                    "couper_gate": "cx 0 1"
                },
                {
                    "single_gate": "u(-[0]/2,0,-([2]+[1])/2) 1"
                },
                {
                    "couper_gate": "cx 0 1"
                },
                {
                    "single_gate": "u([0]/2,[2],0) 1"
                }
            ]
        },
        "circuit_simplify": {
            "repeat": {
                "RZ": ["n", "RZ"],
                "X": "I",
                "Y": "I",
                "Z": "I",
                "S": "Z",
                "T": "S"
            }
        }
    }
