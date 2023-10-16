from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class RemoteV1Doc:
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
                "Remote - List All",
                value=[
                    {
                        "identifier": "CONFIG=Remote Config,VERSION=0.0.1",
                        "config": ["CONFIG=Remote Config,VERSION=0.0.1"],
                        "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
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
                        "Remote - Get",
                        summary="Remote Identifier",
                        description="Remote - Get",
                        value="CONFIG=Remote Config,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Remote - Get",
                value={
                    "identifier": "CONFIG=Remote Config,VERSION=0.0.1",
                    "config": ["CONFIG=Remote Config,VERSION=0.0.1"],
                    "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Remote - Create",
                value={
                    "config": ["CONFIG=Remote Config,VERSION=0.0.1"],
                    "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Remote - Create",
                value={
                    "identifier": "CONFIG=Remote Config,VERSION=0.0.1",
                    "config": ["CONFIG=Remote Config,VERSION=0.0.1"],
                    "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
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
                        "Remote - Delete",
                        summary="Remote Identifier",
                        description="Remote - Delete",
                        value="CONFIG=Remote Config,VERSION=0.0.1",
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
                        "Remote - Patch",
                        summary="Remote Identifier",
                        description="Remote - Patch",
                        value="CONFIG=Remote Config,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Remote - Patch",
                value={
                    "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Remote - Patch",
                value={
                    "identifier": "CONFIG=Remote Config,VERSION=0.0.1",
                    "config": ["CONFIG=Remote Config,VERSION=0.0.1"],
                    "endpoint": ["ENDPOINT=Remote Config,METHOD=POST"],
                },
                request_only=False,
                response_only=True,
            ),
        ]
