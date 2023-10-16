from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class DataV1Doc:
    @staticmethod
    def body_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Data - Body",
                        summary="Data Identifier",
                        description="Data - Get",
                        value="DATA=JSON Template File",
                    )
                ],
            )
        ]

    @staticmethod
    def body_view_examples():
        return [
            OpenApiExample(
                "Data - Body",
                value={"first_name": "Gokul Nathan", "app_name": "Utils"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Data - Body",
                value={
                    "app": "Utils",
                    "first_name": "Gokul Nathan",
                    "dimensions": ["env:dev"],
                },
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
                "Data - List All",
                value=[
                    {
                        "identifier": "DATA=Remote Config",
                        "name": "",
                        "is_template": True,
                        "default_template_values": {"dimensions": ["env:dev"]},
                        "content_type": "JSON",
                        "source_type": "RAW",
                        "raw_json_body": {"dimensions": "{{ dimensions }}"},
                        "raw_body": None,
                        "file": None,
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
                        value="DATA=Remote Config",
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
                    "identifier": "DATA=Remote Config",
                    "name": "",
                    "is_template": True,
                    "default_template_values": {"dimensions": ["env:dev"]},
                    "content_type": "JSON",
                    "source_type": "RAW",
                    "raw_json_body": {"dimensions": "{{ dimensions }}"},
                    "raw_body": None,
                    "file": None,
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
                    "name": "",
                    "is_template": True,
                    "default_template_values": {"dimensions": ["env:dev"]},
                    "content_type": "JSON",
                    "source_type": "RAW",
                    "raw_json_body": {"dimensions": "{{ dimensions }}"},
                    "raw_body": None,
                    "file": None,
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Data - Create",
                value={
                    "identifier": "DATA=Remote Config",
                    "name": "",
                    "is_template": True,
                    "default_template_values": {"dimensions": ["env:dev"]},
                    "content_type": "JSON",
                    "source_type": "RAW",
                    "raw_json_body": {"dimensions": "{{ dimensions }}"},
                    "raw_body": None,
                    "file": None,
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
                        value="DATA=Remote Config",
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
                        value="DATA=Remote Config",
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
                    "raw_json_body": {"dimensions": "{{ dimensions }}"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Data - Patch",
                value={
                    "identifier": "DATA=Remote Config",
                    "name": "",
                    "is_template": True,
                    "default_template_values": {"dimensions": ["env:dev"]},
                    "content_type": "JSON",
                    "source_type": "RAW",
                    "raw_json_body": {"dimensions": "{{ dimensions }}"},
                    "raw_body": None,
                    "file": None,
                },
                request_only=False,
                response_only=True,
            ),
        ]
