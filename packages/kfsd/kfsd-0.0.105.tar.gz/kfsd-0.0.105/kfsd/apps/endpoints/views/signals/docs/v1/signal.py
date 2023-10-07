from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class SignalV1Doc:
    @staticmethod
    def exec_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Signal - Exec",
                        summary="Signal Identifier",
                        description="Signal - Exec",
                        value="SIGNAL=TBL_UPSERT",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Signal - Exec",
                value={
                    "event": {
                        "link": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Signal - Exec",
                value={"detail": "success"},
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_list_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.QUERY,
                name="page",
                required=False,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample("Example 1", summary="Pagination", value=1),
                    OpenApiExample("Example 2", summary="Pagination", value=2),
                ],
            )
        ]

    @staticmethod
    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "Signal - List All",
                value=[
                    {
                        "identifier": "SIGNAL=TBL_UPSERT",
                        "name": "TBL_UPSERT",
                        "delivery": "MSMQ",
                        "is_retain": False,
                    }
                ],
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Signal - Get",
                        summary="Signal Identifier",
                        description="Signal - Get",
                        value="SIGNAL=TBL_UPSERT",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Signal - Get",
                value={
                    "identifier": "SIGNAL=TBL_UPSERT",
                    "name": "TBL_UPSERT",
                    "delivery": "MSMQ",
                    "is_retain": False,
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Signal - Create",
                value={
                    "name": "TBL_UPSERT",
                    "delivery": "MSMQ",
                    "is_retain": False,
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Signal - Create",
                value={
                    "identifier": "SIGNAL=TBL_UPSERT",
                    "name": "TBL_UPSERT",
                    "delivery": "MSMQ",
                    "is_retain": False,
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Signal - Delete",
                        summary="Signal Identifier",
                        description="Signal - Delete",
                        value="SIGNAL=TBL_UPSERT",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Signal - Patch",
                        summary="Signal Identifier",
                        description="Signal - Patch",
                        value="SIGNAL=TBL_UPSERT",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Signal - Patch",
                value={
                    "is_retain": True,
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Signal - Patch",
                value={
                    "identifier": "SIGNAL=TBL_UPSERT",
                    "name": "TBL_UPSERT",
                    "delivery": "MSMQ",
                    "is_retain": True,
                },
                request_only=False,
                response_only=True,
            ),
        ]
