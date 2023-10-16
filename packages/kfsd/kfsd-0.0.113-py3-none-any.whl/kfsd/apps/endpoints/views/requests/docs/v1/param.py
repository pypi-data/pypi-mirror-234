from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class ParamV1Doc:
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
                "Param - List All",
                value=[
                    {
                        "identifier": "NAME=Pipedream,PARAM=category",
                        "name": "Pipedream",
                        "key": "category",
                        "value": "project",
                    },
                    {
                        "identifier": "NAME=Pipedream,PARAM=sort",
                        "name": "Pipedream",
                        "key": "sort",
                        "value": "recent",
                    },
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
                        "Param - Get",
                        summary="Param Identifier",
                        description="Param - Get",
                        value="NAME=Pipedream,PARAM=category",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Param - Get",
                value={
                    "identifier": "NAME=Pipedream,PARAM=category",
                    "name": "Pipedream",
                    "key": "category",
                    "value": "project",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Param - Create",
                value={
                    "name": "Pipedream",
                    "key": "category",
                    "value": "project",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Param - Create",
                value={
                    "identifier": "NAME=Pipedream,PARAM=category",
                    "name": "Pipedream",
                    "key": "category",
                    "value": "project",
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
                        "Param - Delete",
                        summary="Param Identifier",
                        description="Param - Delete",
                        value="NAME=Pipedream,PARAM=category",
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
                        "Param - Patch",
                        summary="Param Identifier",
                        description="Param - Patch",
                        value="NAME=Pipedream,PARAM=category",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Param - Patch",
                value={
                    "value": "project",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Param - Patch",
                value={
                    "identifier": "NAME=Pipedream,PARAM=category",
                    "name": "Pipedream",
                    "key": "category",
                    "value": "project",
                },
                request_only=False,
                response_only=True,
            ),
        ]
