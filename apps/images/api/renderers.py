from rest_framework import renderers


class JPEGRenderer(renderers.BaseRenderer):
    """
    Renderer for JPEG type images.
    """

    media_type = "image/jpeg"
    format = "jpg"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data


class PNGRenderer(renderers.BaseRenderer):
    """
    Renderer for PNG type images.
    """

    media_type = "image/png"
    format = "png"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data
