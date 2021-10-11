from imagekit import ImageSpec
from imagekit.processors import ResizeToFit


def create_thumbnail(image_file, height, path):
    """
    Creates thumbnail from the given image of a given height (px) and saves it to the given path.
    """

    class Thumbnail(ImageSpec):
        processors = [ResizeToFit(height=height, upscale=True)]
        format = "JPEG"
        options = {"quality": 60}

    thumbnail_generator = Thumbnail(source=image_file)
    data = thumbnail_generator.generate()

    with open(path, "wb") as thumbnail:
        thumbnail.write(data.read())
