from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class MediaV1Doc:
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
                "Media - List All",
                value=[
                    {
                        "identifier": "TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
                        "link": "https://www.facebook.com/nathangokul/",
                        "source": "TYPE=Social,PLATFORM=Facebook",
                        "media_id": "abcde",
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
                        "Media - Get",
                        summary="Media Identifier",
                        description="Media - Get",
                        value="TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Media - Get",
                value={
                    "identifier": "TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
                    "link": "https://www.facebook.com/nathangokul/",
                    "source": "TYPE=Social,SOURCE=Facebook",
                    "media_id": "abcde",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Media - Create (with platform)",
                value={
                    "link": "https://www.facebook.com/nathangokul/",
                    "source": "TYPE=Social,SOURCE=Facebook",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Media - Create (no platform)",
                value={"link": "https://www.facebook.com/nathangokul/"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Media - Create (with platform)",
                value={
                    "identifier": "TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
                    "link": "https://www.facebook.com/nathangokul/",
                    "source": "TYPE=Social,SOURCE=Facebook",
                    "media_id": "abcde",
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "Media - Create (no platform)",
                value={
                    "identifier": "MEDIA_ID=abcde",
                    "link": "https://www.facebook.com/nathangokul/",
                    "source": "",
                    "media_id": "abcde",
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
                        "Media - Delete",
                        summary="Media Identifier",
                        description="Media - Delete",
                        value="TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
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
                        "Media - Patch",
                        summary="Media Identifier",
                        description="Media - Patch",
                        value="TYPE=Social,SOURCE=Facebook,MEDIA_ID=abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Media - Patch",
                value={
                    "link": "https://www.facebook.com/nathangokul/",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Media - Patch",
                value={
                    "identifier": "TYPE=Social,PLATFORM=Facebook,MEDIA_ID=abcde",
                    "link": "https://www.facebook.com/nathangokul/",
                    "platform": "TYPE=Social,PLATFORM=Facebook",
                    "media_id": "abcde",
                },
                request_only=False,
                response_only=True,
            ),
        ]
