from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class DataV1Doc:
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
                "Data - List All",
                value=[
                    {
                        "identifier": "DATA=Kubefacets Conf",
                        "name": "Kubefacets Conf",
                        "is_template": True,
                        "default_template_values": {},
                        "content_type": "JSON",
                        "json_body": {"name": "{{name}}"},
                        "body": "",
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
                        "Data - Get",
                        summary="Data Identifier",
                        description="Data - Get",
                        value="DATA=Kubefacets Conf",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Data - Get",
                value={
                    "identifier": "DATA=Kubefacets Conf",
                    "name": "Kubefacets Conf",
                    "is_template": True,
                    "default_template_values": {},
                    "content_type": "JSON",
                    "json_body": {"name": "{{name}}"},
                    "body": "",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Data - Create",
                value={
                    "name": "Kubefacets Conf",
                    "is_template": True,
                    "content_type": "JSON",
                    "json_body": {"name": "{{name}}"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Data - Create",
                value={
                    "identifier": "DATA=Kubefacets Conf",
                    "name": "Kubefacets Conf",
                    "is_template": True,
                    "default_template_values": {},
                    "content_type": "JSON",
                    "json_body": {"name": "{{name}}"},
                    "body": "",
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
                        "Data - Delete",
                        summary="Data Identifier",
                        description="Data - Delete",
                        value="DATA=Kubefacets Conf",
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
                        "Data - Patch",
                        summary="Data Identifier",
                        description="Data - Patch",
                        value="DATA=Kubefacets Conf",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Data - Patch",
                value={
                    "json_body": {"name": "{{name}}"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Data - Patch",
                value={
                    "identifier": "DATA=Kubefacets Conf",
                    "name": "Kubefacets Conf",
                    "is_template": True,
                    "default_template_values": {},
                    "content_type": "JSON",
                    "json_body": {"name": "{{name}}"},
                    "body": "",
                },
                request_only=False,
                response_only=True,
            ),
        ]
