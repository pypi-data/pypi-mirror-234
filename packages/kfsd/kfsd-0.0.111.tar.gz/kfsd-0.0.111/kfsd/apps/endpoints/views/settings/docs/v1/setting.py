from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class SettingV1Doc:
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
                "Setting - List All",
                value=[
                    {
                        "identifier": "SETTING=Kubefacets",
                        "name": "Kubefacets",
                        "config": "CONFIG=Production,VERSION=0.0.1",
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
                        "Setting - Get",
                        summary="Setting Identifier",
                        description="Setting - Get",
                        value="SETTING=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Setting - Get",
                value={
                    "identifier": "SETTING=Kubefacets",
                    "name": "Kubefacets",
                    "config": "CONFIG=Production,VERSION=0.0.1",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Setting - Create",
                value={
                    "name": "Kubefacets",
                    "config": "CONFIG=Production,VERSION=0.0.1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Setting - Create",
                value={
                    "identifier": "SETTING=Kubefacets",
                    "name": "Kubefacets",
                    "config": "CONFIG=Production,VERSION=0.0.1",
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
                        "Setting - Delete",
                        summary="Setting Identifier",
                        description="Setting - Delete",
                        value="SETTING=Kubefacets",
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
                        "Setting - Exec",
                        summary="Setting Identifier",
                        description="Setting - Exec",
                        value="SETTING=Kubefacets",
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
                        "Setting - Patch",
                        summary="Setting Identifier",
                        description="Setting - Patch",
                        value="SETTING=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Setting - Patch",
                value={
                    "config": "CONFIG=Production,VERSION=0.0.2",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Setting - Patch",
                value={
                    "identifier": "SETTING=Kubefacets",
                    "name": "Kubefacets",
                    "config": "CONFIG=Production,VERSION=0.0.2",
                },
                request_only=False,
                response_only=True,
            ),
        ]
