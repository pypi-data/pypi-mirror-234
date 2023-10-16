from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class ProducerV1Doc:
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
                        "Producer - Exec",
                        summary="Producer Identifier",
                        description="Producer - Exec",
                        value="ID=abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Producer - Exec",
                value={
                    "event": {
                        "link": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Producer - Exec",
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
                "Producer - List All",
                value=[
                    {
                        "identifier": "EXCHANGE=kubefacets.exchange",
                        "name": "kubefacets.exchange",
                        "attrs": {"durable": True, "exchange_type": "direct"},
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
                        "Producer - Get",
                        summary="Producer Identifier",
                        description="Producer - Get",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Producer - Get",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange",
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Producer - Create",
                value={
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Producer - Create",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange",
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
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
                        "Producer - Delete",
                        summary="Producer Identifier",
                        description="Producer - Delete",
                        value="EXCHANGE=kubefacets.exchange",
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
                        "Producer - Patch",
                        summary="Producer Identifier",
                        description="Producer - Patch",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Producer - Patch",
                value={
                    "name": "kubefacets.exchange.v1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Producer - Patch",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange.v1",
                    "name": "kubefacets.exchange.v1",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            ),
        ]
