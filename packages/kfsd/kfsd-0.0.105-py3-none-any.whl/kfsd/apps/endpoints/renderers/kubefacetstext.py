"""
Provides TEXT rendering support.
"""
from __future__ import unicode_literals

from rest_framework.renderers import BaseRenderer


class KubefacetsTEXTRenderer(BaseRenderer):
    """
    Renderer which serializes to TEXT.
    """

    media_type = "plain/text"
    format = "text"
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):

        return data
