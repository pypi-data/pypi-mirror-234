from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class SourceV1Doc:
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
                "Source - List All",
                value=[
                    {
                        "identifier": "TYPE=Social,SOURCE=Facebook",
                        "name": "Facebook",
                        "type": "Social",
                        "slug": "facebook",
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
                        "Source - Get",
                        summary="Source Identifier",
                        description="Source - Get",
                        value="TYPE=Social,SOURCE=Facebook",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Source - Get",
                value={
                    "identifier": "TYPE=Social,SOURCE=Facebook",
                    "name": "Facebook",
                    "type": "Social",
                    "slug": "facebook",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Source - Create",
                value={
                    "name": "Facebook",
                    "type": "Social",
                    "slug": "facebook",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Source - Create",
                value={
                    "identifier": "TYPE=Social,SOURCE=Facebook",
                    "name": "Facebook",
                    "type": "Social",
                    "slug": "facebook",
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
                        "Source - Delete",
                        summary="Source Identifier",
                        description="Source - Delete",
                        value="TYPE=Social,SOURCE=Facebook",
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
                        "Source - Patch",
                        summary="Source Identifier",
                        description="Source - Patch",
                        value="TYPE=Social,SOURCE=Facebook",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Source - Patch",
                value={
                    "name": "Facebook 123",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Source - Patch",
                value={
                    "identifier": "TYPE=Social,SOURCE=Facebook 123",
                    "name": "Facebook 123",
                    "type": "Social",
                    "slug": "facebook-123",
                },
                request_only=False,
                response_only=True,
            ),
        ]
