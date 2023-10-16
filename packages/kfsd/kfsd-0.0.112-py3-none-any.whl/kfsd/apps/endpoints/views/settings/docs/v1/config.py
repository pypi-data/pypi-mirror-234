from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class ConfigV1Doc:
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
                "Config - List All",
                value=[
                    {
                        "identifier": "CONFIG=Production,VERSION=0.0.1",
                        "name": "Production",
                        "version": "0.0.1",
                        "is_local_config": True,
                        "lookup_dimension_keys": ["env"],
                        "local_config": [
                            {
                                "setting": ["master"],
                                "app": "app_api_utils_as_a_service",
                            },
                            {
                                "setting": ["dev"],
                                "app": "app_api_utils_as_a_service_dev",
                            },
                        ],
                        "remote_config_link": "",
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
                        "Config - Get",
                        summary="Config Identifier",
                        description="Config - Get",
                        value="CONFIG=Production,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Config - Get",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": True,
                    "lookup_dimension_keys": ["env"],
                    "local_config": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                    "remote_config_link": "",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Config - Create (Local)",
                value={
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": True,
                    "lookup_dimension_keys": ["env"],
                    "local_config": [
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
                "Config - Create (Remote)",
                value={
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": False,
                    "lookup_dimension_keys": ["env"],
                    "remote_config_link": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Config - Create (Local)",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": True,
                    "lookup_dimension_keys": ["env"],
                    "local_config": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev",
                        },
                    ],
                    "remote_config_link": "",
                },
                request_only=False,
                response_only=True,
            ),
            OpenApiExample(
                "Config - Create (Remote)",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": True,
                    "lookup_dimension_keys": ["env"],
                    "remote_config_link": "https://5ab2a9578da0281e7eeec323a4f972c0.m.pipedream.net",
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
                        "Config - Delete",
                        summary="Config Identifier",
                        description="Config - Delete",
                        value="CONFIG=Production,VERSION=0.0.1",
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
                        "Config - Patch",
                        summary="Config Identifier",
                        description="Config - Patch",
                        value="CONFIG=Production,VERSION=0.0.1",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Config - Patch",
                value={
                    "local_config": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev_1",
                        },
                    ],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Config - Patch",
                value={
                    "identifier": "CONFIG=Production,VERSION=0.0.1",
                    "name": "Production",
                    "version": "0.0.1",
                    "is_local_config": True,
                    "lookup_dimension_keys": ["env"],
                    "local_config": [
                        {
                            "setting": ["master"],
                            "app": "app_api_utils_as_a_service",
                        },
                        {
                            "setting": ["dev"],
                            "app": "app_api_utils_as_a_service_dev_1",
                        },
                    ],
                    "remote_config_link": "",
                },
                request_only=False,
                response_only=True,
            ),
        ]
