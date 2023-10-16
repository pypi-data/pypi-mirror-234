from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class ReferenceV1Doc:
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
                "Reference - List All",
                value=[
                    {
                        "identifier": "ORG=Kubefacets",
                        "type": "ORG",
                        "attrs": {"name": "Kubefacets Inc", "slug": "kubefacets-inc"},
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
                        "Reference - Get",
                        summary="Reference Identifier",
                        description="Reference - Get",
                        value="ORG=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Reference - Get",
                value={
                    "identifier": "ORG=Kubefacets",
                    "type": "ORG",
                    "attrs": {"name": "Kubefacets Inc", "slug": "kubefacets-inc"},
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Reference - Create (Org)",
                value={
                    "identifier": "ORG=Kubefacets",
                    "type": "ORG",
                    "attrs": {"name": "Kubefacets Inc", "slug": "kubefacets-inc"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Reference - Create (User)",
                value={
                    "identifier": "USER=admin",
                    "type": "USER",
                    "attrs": {
                        "identifier": "USER=admin",
                        "first_name": "Gokul Nathan",
                        "last_name": "Chandran",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Reference - Create",
                value={
                    "identifier": "ORG=Kubefacets",
                    "type": "ORG",
                    "attrs": {"name": "Kubefacets Inc", "slug": "kubefacets-inc"},
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
                        "Reference - Delete",
                        summary="Reference Identifier",
                        description="Reference - Delete",
                        value="ORG=Kubefacets",
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
                        "Reference - Patch",
                        summary="Reference Identifier",
                        description="Reference - Patch",
                        value="ORG=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Reference - Patch",
                value={
                    "attrs": {"name": "Kubefacets", "slug": "kubefacets"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Reference - Patch",
                value={
                    "identifier": "ORG=Kubefacets",
                    "type": "ORG",
                    "attrs": {"name": "Kubefacets", "slug": "kubefacets"},
                },
                request_only=False,
                response_only=True,
            ),
        ]
