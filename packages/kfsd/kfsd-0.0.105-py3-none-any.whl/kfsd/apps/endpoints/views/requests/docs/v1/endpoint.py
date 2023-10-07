from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class EndpointV1Doc:
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
                "Endpoint - List All",
                value=[
                    {
                        "identifier": "ENDPOINT=Remote Config,METHOD=POST",
                        "name": "Remote Config",
                        "request_template": "REQ_TEMPLATE=Remote Config",
                        "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                        "method": "POST",
                        "body": "DATA=Remote Config",
                        "success_code": 200,
                    },
                    {
                        "identifier": "ENDPOINT=HTML,METHOD=POST",
                        "name": "HTML",
                        "request_template": "",
                        "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                        "method": "POST",
                        "body": "DATA=HTML Data",
                        "success_code": 200,
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
                        "Endpoint - Get",
                        summary="Endpoint Identifier",
                        description="Endpoint - Get",
                        value="ENDPOINT=Remote Config,METHOD=POST",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Endpoint - Get",
                value={
                    "identifier": "ENDPOINT=Remote Config,METHOD=POST",
                    "name": "Remote Config",
                    "request_template": "REQ_TEMPLATE=Remote Config",
                    "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    "method": "POST",
                    "body": "DATA=Remote Config",
                    "success_code": 200,
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Endpoint - Create",
                value={
                    "name": "Remote Config",
                    "request_template": "REQ_TEMPLATE=Remote Config",
                    "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    "method": "POST",
                    "body": "DATA=Remote Config",
                    "success_code": 200,
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Endpoint - Create",
                value={
                    "identifier": "ENDPOINT=Remote Config,METHOD=POST",
                    "name": "Remote Config",
                    "request_template": "REQ_TEMPLATE=Remote Config",
                    "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    "method": "POST",
                    "body": "DATA=Remote Config",
                    "success_code": 200,
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
                        "Endpoint - Delete",
                        summary="Endpoint Identifier",
                        description="Endpoint - Delete",
                        value="ENDPOINT=Remote Config,METHOD=POST",
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
                        "Endpoint - Exec",
                        summary="Endpoint Identifier",
                        description="Endpoint - Exec",
                        value="ENDPOINT=Remote Config,METHOD=POST",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Endpoint - Exec",
                value={"dimensions": ["env:dev"]},
                request_only=True,
                response_only=False,
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
                        "Endpoint - Patch",
                        summary="Endpoint Identifier",
                        description="Endpoint - Patch",
                        value="ENDPOINT=Remote Config,METHOD=POST",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Endpoint - Patch",
                value={
                    "name": "Remote Config",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Endpoint - Patch",
                value={
                    "identifier": "ENDPOINT=Remote Config,METHOD=POST",
                    "name": "Remote Config",
                    "request_template": "REQ_TEMPLATE=Remote Config",
                    "url": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                    "method": "POST",
                    "body": "DATA=Remote Config",
                    "success_code": 200,
                },
                request_only=False,
                response_only=True,
            ),
        ]
