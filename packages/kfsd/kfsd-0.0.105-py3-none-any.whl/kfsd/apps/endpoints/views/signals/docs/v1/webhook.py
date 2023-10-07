from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class WebhookV1Doc:
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
                "Webhook - List All",
                value=[
                    {
                        "identifier": "abcde",
                        "signal": "SIGNAL=TBL_UPSERT",
                        "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                        "uniq_id": "abcde",
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
                        "Webhook - Get",
                        summary="Webhook Identifier",
                        description="Webhook - Get",
                        value="abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Webhook - Get",
                value={
                    "identifier": "abcde",
                    "signal": "SIGNAL=TBL_UPSERT",
                    "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                    "uniq_id": "abcde",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Webhook - Create",
                value={
                    "signal": "SIGNAL=TBL_UPSERT",
                    "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                    "uniq_id": "abcde",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Webhook - Create",
                value={
                    "identifier": "abcde",
                    "signal": "SIGNAL=TBL_UPSERT",
                    "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                    "uniq_id": "abcde",
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
                        "Webhook - Delete",
                        summary="Webhook Identifier",
                        description="Webhook - Delete",
                        value="abcde",
                    )
                ],
            )
        ]

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
                        "Webhook - Exec",
                        summary="Webhook Identifier",
                        description="Webhook - Exec",
                        value="ID=abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Webhook - Exec",
                value={
                    "event": {
                        "link": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    }
                },
                request_only=True,
                response_only=False,
            ),
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
                        "Webhook - Patch",
                        summary="Webhook Identifier",
                        description="Webhook - Patch",
                        value="abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Webhook - Patch",
                value={
                    "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Webhook - Patch",
                value={
                    "identifier": "abcde",
                    "signal": "SIGNAL=TBL_UPSERT",
                    "endpoint": "ENDPOINT=Signal Webhook,METHOD=POST",
                    "uniq_id": "abcde",
                },
                request_only=False,
                response_only=True,
            ),
        ]
