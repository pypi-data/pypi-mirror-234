from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class FileDocV1:
    def file_thumbnail_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="File Identifier",
                        value="FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    )
                ],
            )
        ]

    def file_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="File Identifier",
                        value="FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    )
                ],
            )
        ]

    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "File - Create",
                value={
                    "identifier": "FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    "slug": "adminlte-min-css",
                    "name": "adminlte.min.css",
                    "file": {
                        "url": "/media/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                        "size": 1396703,
                        "extension": ".css",
                        "path": "/Users/gokul/workspace/code/app_api_file_as_a_service/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                    },
                    "uniq_id": "5733dd",
                    "is_public": True,
                    "version": "3.2.0",
                    "expiry_in_mins": 1440,
                },
                request_only=False,
                response_only=True,
            ),
        ]

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

    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "File - Create",
                value=[
                    {
                        "identifier": "FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                        "slug": "adminlte-min-css",
                        "name": "adminlte.min.css",
                        "file": {
                            "url": "/media/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                            "size": 1396703,
                            "extension": ".css",
                            "path": "/Users/gokul/workspace/code/app_api_file_as_a_service/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                        },
                        "uniq_id": "5733dd",
                        "is_public": True,
                        "version": "3.2.0",
                        "expiry_in_mins": 1440,
                    }
                ],
                request_only=False,
                response_only=True,
            ),
        ]

    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="File Identifier",
                        value="FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    )
                ],
            )
        ]

    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "File - Get",
                value={
                    "identifier": "FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    "slug": "adminlte-min-css",
                    "name": "adminlte.min.css",
                    "file": {
                        "url": "/media/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                        "size": 1396703,
                        "extension": ".css",
                        "path": "/Users/gokul/workspace/code/app_api_file_as_a_service/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                    },
                    "uniq_id": "5733dd",
                    "is_public": True,
                    "version": "3.2.0",
                    "expiry_in_mins": 1440,
                },
                request_only=False,
                response_only=True,
            ),
        ]

    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="File Identifier",
                        value="FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    )
                ],
            )
        ]

    def modelviewset_partial_update_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="File Identifier",
                        value="FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    )
                ],
            )
        ]

    def modelviewset_partial_update_examples():
        return [
            OpenApiExample(
                "File - Partial Update",
                value={
                    "identifier": "FILE=adminlte.min.css,VERSION=3.2.0,UNIQ_ID=5733dd",
                    "slug": "adminlte-min-css",
                    "name": "adminlte.min.css",
                    "file": {
                        "url": "/media/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                        "size": 1396703,
                        "extension": ".css",
                        "path": "/Users/gokul/workspace/code/app_api_file_as_a_service/uploads/sso/css/adminlte/3.2.0/adminlte.min.css",
                    },
                    "uniq_id": "5733dd",
                    "is_public": True,
                    "version": "3.2.0",
                    "expiry_in_mins": 1440,
                },
                request_only=False,
                response_only=True,
            ),
        ]
