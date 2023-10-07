from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class RequestTemplateV1Doc:
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
                "Template - List All",
                value=[
                    {
                        "identifier": "REQ_TEMPLATE=Pipedream",
                        "name": "Pipedream",
                        "headers": ["NAME=Pipedream,HEADER=X-Server-Key"],
                        "params": ["NAME=Pipedream,PARAM=category"],
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
                        "Template - Get",
                        summary="Template Identifier",
                        description="Template - Get",
                        value="REQ_TEMPLATE=Pipedream",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Template - Get",
                value={
                    "identifier": "REQ_TEMPLATE=Pipedream",
                    "name": "Pipedream",
                    "headers": ["NAME=Pipedream,HEADER=X-Server-Key"],
                    "params": ["NAME=Pipedream,PARAM=category"],
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Template - Create",
                value={
                    "name": "Pipedream",
                    "headers": ["NAME=Pipedream,HEADER=X-Server-Key"],
                    "params": ["NAME=Pipedream,PARAM=category"],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Template - Create",
                value={
                    "identifier": "REQ_TEMPLATE=Pipedream",
                    "name": "Pipedream",
                    "headers": ["NAME=Pipedream,HEADER=X-Server-Key"],
                    "params": ["NAME=Pipedream,PARAM=category"],
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
                        "Template - Delete",
                        summary="Template Identifier",
                        description="Template - Delete",
                        value="REQ_TEMPLATE=Pipedream",
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
                        "Template - Patch",
                        summary="Template Identifier",
                        description="Template - Patch",
                        value="REQ_TEMPLATE=Pipedream",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Template - Patch",
                value={
                    "name": "Pipedream",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Template - Patch",
                value={
                    "identifier": "REQ_TEMPLATE=Pipedream",
                    "name": "Pipedream",
                    "headers": ["NAME=Pipedream,HEADER=X-Server-Key"],
                    "params": ["NAME=Pipedream,PARAM=category"],
                },
                request_only=False,
                response_only=True,
            ),
        ]
