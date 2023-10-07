from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class LocalV1Doc:
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
                "Local - List All",
                value=[
                    {
                        "identifier": "CONFIG=Production,VERSION=0.0.1",
                        "config": "CONFIG=Production,VERSION=0.0.1",
                        "data": [
                            {
                                "setting": ["master"],
                                "app": "app_api_utils_as_a_service",
                            },
                            {
                                "setting": ["dev"],
                                "app": "app_api_utils_as_a_service_dev",
                            },
                        ],
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
                        "Local - Get",
                        summary="Local Identifier",
                        description="Local - Get",
                        value="CONFIG=Production,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Local - Get",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "config": "CONFIG=Production,VERSION=0.0.1",
                    "data": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Local - Create",
                value={
                    "config": "CONFIG=Production,VERSION=0.0.1",
                    "data": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Local - Create",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "config": "CONFIG=Production,VERSION=0.0.1",
                    "data": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
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
                        "Local - Delete",
                        summary="Local Identifier",
                        description="Local - Delete",
                        value="CONFIG=Production,VERSION=0.0.1",
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
                        "Local - Exec",
                        summary="Local Identifier",
                        description="Local - Exec",
                        value="CONFIG=Production NoAuth,VERSION=0.0.1",
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
                        "Local - Patch",
                        summary="Local Identifier",
                        description="Local - Patch",
                        value="CONFIG=Production,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Local - Patch",
                value={
                    "data": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Local - Patch",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "config": "CONFIG=Production,VERSION=0.0.1",
                    "data": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Local - Exec",
                value={"dimensions": {"env": "dev"}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Local - Exec",
                value={
                    "app": "app_api_utils_as_a_service",
                    "services": {
                        "features_enabled": {"auth": True, "rabbitmq": False},
                        "api_key": "9a02f7923aa22e69e0e2858d682a0c227ae0f3ce125a41c61d",
                        "sso_fe": {
                            "signin_uri": "accounts/signin/",
                            "email_verify_uri": "accounts/register/email/",
                            "host": "http://localhost:8000",
                        },
                        "gateway_api": {
                            "sso": {"verify_tokens_uri": "sso/cookies/verify/"},
                            "core": {"common_config_uri": "core/config/common/"},
                            "host": "http://localhost:8002/apis",
                        },
                        "rabbitmq": {
                            "connect": {
                                "credentials": {"username": "guest", "pwd": "guest"},
                                "heartbeat": 5,
                                "host": "localhost",
                                "port": 5672,
                            },
                        },
                        "default_signedin_url": "http://localhost:8000/accounts/index/",
                    },
                },
                request_only=False,
                response_only=True,
            ),
        ]
