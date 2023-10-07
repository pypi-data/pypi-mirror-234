from drf_spectacular.utils import OpenApiExample


class UtilsV1Doc:
    @staticmethod
    def attr_examples():
        return [
            OpenApiExample(
                "EXPR",
                media_type="application/json",
                value={
                    "op": "EXPR",
                    "input": {
                        "dict": {"id": 1, "age": 41, "bio": {"address": "Bangalore"}},
                        "expr": "request.bio.address",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "EXPR",
                media_type="application/json",
                value={"output": {"value": "Bangalore"}, "op": "EXPR"},
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def status_examples():
        return [
            OpenApiExample(
                "CONFIG",
                media_type="application/json",
                value={"detail": "status_ok", "code": 200},
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def config_examples():
        return [
            OpenApiExample(
                "CONFIG",
                media_type="application/json",
                value={
                    "output": {
                        "value": {
                            "templates": [
                                {
                                    "template": "istio/networking.istio.io/v1alpha3/gateway.json",
                                    "dimensions": [],
                                    "globalvars": {"__TEMPLATE_ID__": "gateway"},
                                }
                            ],
                            "overrides": {
                                "gateway": {
                                    "spec": {
                                        "servers": [
                                            {
                                                "port": "{{ values.gateway.virtualhost0.listen }}",
                                                "hosts": "{{ values.gateway.virtualhost0.hosts }}",
                                            }
                                        ]
                                    }
                                }
                            },
                            "values": {
                                "gateway": {
                                    "metadata": {
                                        "name": "istio-gateway",
                                        "namespace": "istio-system",
                                    },
                                    "virtualhost0": {
                                        "listen": {
                                            "number": 80,
                                            "name": "http-snappyguide",
                                            "protocol": "HTTP",
                                        },
                                        "hosts": [
                                            "dev.snappyguide.com",
                                            "dev.accounts.snappyguide.com",
                                        ],
                                    },
                                }
                            },
                        }
                    },
                    "op": "CONFIG",
                },
                request_only=False,
                response_only=False,
            ),
            OpenApiExample(
                "CONFIG",
                media_type="application/json",
                value={
                    "op": "CONFIG",
                    "input": {
                        "dimensions": {
                            "environment": "k8s",
                            "cluster": "mac",
                            "type": "dev",
                        },
                        "raw_config": [
                            {
                                "setting": ["master"],
                                "templates": [
                                    {
                                        "template": "istio/networking.istio.io/v1alpha3/gateway.json",
                                        "dimensions": [],
                                        "globalvars": {"__TEMPLATE_ID__": "gateway"},
                                    }
                                ],
                                "overrides": {
                                    "gateway": {
                                        "spec": {
                                            "servers": [
                                                {
                                                    "port": "{{ values.gateway.virtualhost0.listen }}",
                                                    "hosts": "{{ values.gateway.virtualhost0.hosts }}",
                                                }
                                            ]
                                        }
                                    }
                                },
                                "values": {
                                    "gateway": {
                                        "metadata": {
                                            "name": "istio-gateway",
                                            "namespace": "istio-system",
                                        },
                                        "virtualhost0": {
                                            "listen": {
                                                "number": 80,
                                                "name": "http-snappyguide",
                                                "protocol": "HTTP",
                                            }
                                        },
                                    }
                                },
                            },
                            {
                                "setting": [
                                    "environment:k8s",
                                    "cluster:mac",
                                    "type:dev",
                                ],
                                "values": {
                                    "gateway": {
                                        "virtualhost0": {
                                            "hosts": [
                                                "dev.snappyguide.com",
                                                "dev.accounts.snappyguide.com",
                                            ]
                                        }
                                    }
                                },
                            },
                            {
                                "setting": [
                                    "environment:k8s",
                                    "cluster:inhouse",
                                    "type:prod",
                                ],
                                "values": {
                                    "gateway": {
                                        "virtualhost0": {
                                            "hosts": [
                                                "snappyguide.com",
                                                "accounts.snappyguide.com",
                                            ]
                                        }
                                    }
                                },
                            },
                        ],
                    },
                },
                request_only=True,
                response_only=False,
            ),
        ]

    @staticmethod
    def arr_examples():
        return [
            OpenApiExample(
                "MERGE (Arr of Dicts)",
                media_type="application/json",
                value={
                    "op": "MERGE",
                    "input": {
                        "lookup_key": "id",
                        "arr1": [
                            {"id": 1, "name": "Gokul"},
                            {"id": 2, "name": "Lavanya"},
                            {"id": 4, "name": "Sana"},
                            {"id": 5, "name": "Cat"},
                        ],
                        "arr2": [
                            {"id": 1, "age": 41},
                            {"id": 2, "age": 36},
                            {"id": 3, "age": 13},
                            {"id": 3, "age": 13},
                            {"id": 5, "name": "Dog"},
                        ],
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "MERGE (Arr of Dicts)",
                media_type="application/json",
                value={
                    "output": {
                        "value": [
                            {"id": 1, "name": "Gokul", "age": 41},
                            {"id": 2, "name": "Lavanya", "age": 36},
                            {"id": 4, "name": "Sana"},
                            {"id": 5, "name": "Dog"},
                            {"id": 3, "age": 13},
                        ]
                    },
                    "op": "MERGE",
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "MERGE",
                media_type="application/json",
                value={
                    "op": "MERGE",
                    "input": {
                        "is_uniq": False,
                        "arr1": ["gokul", "lavanya"],
                        "arr2": ["lavanya", "diya", "sana"],
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "MERGE",
                media_type="application/json",
                value={
                    "op": "MERGE",
                    "output": {
                        "value": ["gokul", "lavanya", "lavanya", "diya", "sana"]
                    },
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "MERGE (Uniq)",
                media_type="application/json",
                value={
                    "op": "MERGE",
                    "input": {
                        "is_uniq": True,
                        "arr1": ["gokul", "lavanya"],
                        "arr2": ["lavanya", "diya", "sana"],
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "MERGE (Uniq)",
                media_type="application/json",
                value={
                    "op": "MERGE",
                    "output": {"value": ["gokul", "lavanya", "diya", "sana"]},
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "INTERSECTION",
                media_type="application/json",
                value={
                    "op": "INTERSECTION",
                    "input": {
                        "arr1": ["gokul", "lavanya"],
                        "arr2": ["lavanya", "diya", "sana"],
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "INTERSECTION",
                media_type="application/json",
                value={"op": "INTERSECTION", "output": {"value": ["lavanya"]}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "JOIN",
                media_type="application/json",
                value={"op": "JOIN", "input": {"arr": ["gokul", "nathan"], "str": ","}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "JOIN",
                media_type="application/json",
                value={"op": "JOIN", "output": {"value": "gokul,nathan"}},
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def system_examples():
        return [
            OpenApiExample(
                "CHECKSUM ( Str )",
                media_type="application/json",
                value={"op": "CHECKSUM", "input": {"data": "gokul"}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "CHECKSUM ( Dict )",
                media_type="application/json",
                value={"op": "CHECKSUM", "input": {"data": {"key": "value"}}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "UUID",
                media_type="application/json",
                value={"op": "UUID", "input": {"len": 32}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "SECRET",
                media_type="application/json",
                value={"op": "SECRET", "input": {"len": 32}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "KEY",
                media_type="application/json",
                value={"op": "KEY", "input": {"len": 10}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "ENCRYPT_KEY",
                media_type="application/json",
                value={"op": "ENCRYPT_KEY", "input": {"key": "gokul"}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "OS_ARCH",
                media_type="application/json",
                value={"op": "OS_ARCH"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "HOST_IP",
                media_type="application/json",
                value={"op": "HOST_IP"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "NIC",
                media_type="application/json",
                value={"op": "NIC"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "HOSTNAME",
                media_type="application/json",
                value={"op": "HOSTNAME"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "OS",
                media_type="application/json",
                value={"op": "OS"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "CHECKSUM",
                media_type="application/json",
                value={"op": "CHECKSUM", "output": {"value": 106627619}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "UUID",
                media_type="application/json",
                value={
                    "op": "UUID",
                    "output": {"value": "ad2c18417cecc9b167c9b19ad52dfdc1"},
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "SECRET",
                media_type="application/json",
                value={
                    "op": "SECRET",
                    "output": {"value": "P9gOT1OkxSFx2EXUL-fEr6qLoPB8awJuMQiaMI9ObEE"},
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "KEY",
                media_type="application/json",
                value={"op": "KEY", "output": {"value": "46e2f9bf60"}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "ENCRYPT_KEY",
                media_type="application/json",
                value={"op": "ENCRYPT_KEY", "output": {"value": "Z29rdWwK"}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "HOST_IP",
                media_type="application/json",
                value={"op": "HOST_IP", "output": {"value": "192.168.2.10"}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "NIC",
                media_type="application/json",
                value={"op": "NIC", "output": {"value": "en0"}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "HOSTNAME",
                media_type="application/json",
                value={"op": "HOSTNAME", "output": {"value": "localhost"}},
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "OS",
                media_type="application/json",
                value={"op": "OS", "output": {"value": "Darwin"}},
                request_only=False,
                response_only=True,
            ),
        ]
