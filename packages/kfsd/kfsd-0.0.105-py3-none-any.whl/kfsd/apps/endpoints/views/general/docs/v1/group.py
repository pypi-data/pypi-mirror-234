from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class GroupV1Doc:
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
                "Group - List All",
                value=[
                    {
                        "identifier": "TYPE=Org,NAME=Kubefacets",
                        "name": "Kubefacets",
                        "type": "Org",
                        "parent": None,
                        "media": ["TYPE=WEBSITE,SOURCE=Facebook"],
                        "members": ["USER=admin"],
                        "groups": ["PARENT=TYPE=Org,NAME=Kubefacets,CHILD=Team,FE"],
                        "slug": "kubefacets",
                        "description": "Kubefacets Org",
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
                        "Group - Get",
                        summary="Group Identifier",
                        description="Group - Get",
                        value="TYPE=Org,NAME=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Group - Get",
                value={
                    "identifier": "TYPE=Org,NAME=Kubefacets",
                    "name": "Kubefacets",
                    "type": "Org",
                    "parent": None,
                    "media": ["TYPE=WEBSITE,SOURCE=Facebook"],
                    "members": ["USER=admin"],
                    "groups": ["PARENT=TYPE=Org,NAME=Kubefacets,CHILD=Team,FE"],
                    "slug": "kubefacets",
                    "description": "Kubefacets Org",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Group - Create",
                value={
                    "media": ["TYPE=WEBSITE,SOURCE=Facebook"],
                    "name": "Kubefacets",
                    "type": "Org",
                    "members": ["USER=admin"],
                    "groups": ["PARENT=TYPE=Org,NAME=Kubefacets,CHILD=Team,FE"],
                    "slug": "kubefacets",
                    "description": "Kubefacets Org",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Group - Create",
                value={
                    "identifier": "TYPE=Org,NAME=Kubefacets",
                    "parent": None,
                    "media": ["TYPE=WEBSITE,SOURCE=Facebook"],
                    "members": ["USER=admin"],
                    "groups": ["PARENT=TYPE=Org,NAME=Kubefacets,CHILD=Team,FE"],
                    "slug": "kubefacets",
                    "description": "Kubefacets Org",
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
                        "Group - Delete",
                        summary="Group Identifier",
                        description="Group - Delete",
                        value="TYPE=Org,NAME=Kubefacets",
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
                        "Group - Patch",
                        summary="Group Identifier",
                        description="Group - Patch",
                        value="TYPE=Org,NAME=Kubefacets",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Group - Patch",
                value={"media": ["TYPE=WEBSITE,SOURCE=Facebook"]},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Group - Patch",
                value={
                    "identifier": "TYPE=Org,NAME=Kubefacets",
                    "parent": None,
                    "media": ["TYPE=WEBSITE,SOURCE=Facebook"],
                    "members": ["USER=admin"],
                    "groups": ["PARENT=TYPE=Org,NAME=Kubefacets,CHILD=Team,FE"],
                    "slug": "kubefacets",
                    "description": "Kubefacets Org",
                },
                request_only=False,
                response_only=True,
            ),
        ]
