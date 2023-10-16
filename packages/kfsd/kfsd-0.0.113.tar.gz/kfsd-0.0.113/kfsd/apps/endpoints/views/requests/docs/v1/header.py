from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class HeaderV1Doc:
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
                "Header - List All",
                value=[
                    {
                        "identifier": "NAME=Pipedream,HEADER=X-Server-Key",
                        "name": "Pipedream",
                        "key": "X-Server-Key",
                        "value": "abcde",
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
                        "Header - Get",
                        summary="Header Identifier",
                        description="Header - Get",
                        value="NAME=Pipedream,HEADER=X-Server-Key",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Header - Get",
                value={
                    "identifier": "NAME=Pipedream,HEADER=X-Server-Key",
                    "name": "Pipedream",
                    "key": "X-Server-Key",
                    "value": "abcde",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Header - Create",
                value={
                    "name": "Pipedream",
                    "key": "X-Server-Key",
                    "value": "abcde",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Header - Create",
                value={
                    "identifier": "NAME=Pipedream,HEADER=X-Server-Key",
                    "name": "Pipedream",
                    "key": "X-Server-Key",
                    "value": "abcde",
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
                        "Header - Delete",
                        summary="Header Identifier",
                        description="Header - Delete",
                        value="NAME=Pipedream,HEADER=X-Server-Key",
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
                        "Header - Patch",
                        summary="Header Identifier",
                        description="Header - Patch",
                        value="NAME=Pipedream,HEADER=X-Server-Key",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Header - Patch",
                value={
                    "value": "abcde",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Header - Patch",
                value={
                    "identifier": "NAME=Pipedream,HEADER=X-Server-Key",
                    "name": "Pipedream",
                    "key": "X-Server-Key",
                    "value": "abcde",
                },
                request_only=False,
                response_only=True,
            ),
        ]
