from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class OutboundV1Doc:
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
                "Outbound - List All",
                value=[
                    {
                        "identifier": "abcde",
                        "name": "TBL_UPSERT",
                        "data": {
                            "action": "TBL_UPSERT",
                            "data": {
                                "op": "CREATE",
                                "service_id": "utils_api",
                                "tbl": "Inbound",
                            },
                        },
                        "status": "IN-PROGRESS",
                        "attempts": 0,
                        "debug_info": {},
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
                        "Outbound - Get",
                        summary="Outbound Identifier",
                        description="Outbound - Get",
                        value="abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Outbound - Get",
                value={
                    "identifier": "abcde",
                    "name": "TBL_UPSERT",
                    "data": {
                        "action": "TBL_UPSERT",
                        "data": {
                            "op": "CREATE",
                            "service_id": "utils_api",
                            "tbl": "Inbound",
                        },
                    },
                    "status": "IN-PROGRESS",
                    "attempts": 0,
                    "debug_info": {},
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Outbound - Create",
                value={
                    "name": "TBL_UPSERT",
                    "data": {
                        "action": "TBL_UPSERT",
                        "data": {
                            "op": "CREATE",
                            "service_id": "utils_api",
                            "tbl": "Inbound",
                        },
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Outbound - Create",
                value={
                    "identifier": "abcde",
                    "name": "TBL_UPSERT",
                    "data": {
                        "action": "TBL_UPSERT",
                        "data": {
                            "op": "CREATE",
                            "service_id": "utils_api",
                            "tbl": "Inbound",
                        },
                    },
                    "status": "IN-PROGRESS",
                    "attempts": 0,
                    "debug_info": {},
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
                        "Outbound - Delete",
                        summary="Outbound Identifier",
                        description="Outbound - Delete",
                        value="abcde",
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
                        "Outbound - Patch",
                        summary="Outbound Identifier",
                        description="Outbound - Patch",
                        value="abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Outbound - Patch",
                value={"name": "TBL_UPSERT"},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Outbound - Patch",
                value={
                    "identifier": "abcde",
                    "name": "TBL_UPSERT",
                    "data": {
                        "action": "TBL_UPSERT",
                        "data": {
                            "op": "CREATE",
                            "service_id": "utils_api",
                            "tbl": "Inbound",
                        },
                    },
                    "status": "IN-PROGRESS",
                    "attempts": 0,
                    "debug_info": {},
                },
                request_only=False,
                response_only=True,
            ),
        ]
