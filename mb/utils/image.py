from .check_package import check_package

__all__ = ['convert_webp_to_jpg']

def convert_webp_to_jpg(image_path: str, output_path: str, crop_shape = None):
    """
    Convert a WebP image to JPG format. With 4th channel being alpha. Apply alpha channel as mask to RGB channels, then save as JPG.

    Args:
        image_path (str): Path to the input WebP image.
        output_path (str): Path to save the converted format.
        crop_shape (tuple): Optional_croping. (h1,h2,w1,w2). If provided, the image will be cropped to this shape before saving.

    Raises:
        ImportError: If the Pillow library is not installed.
        FileNotFoundError: If the input image file does not exist.
        Exception: If there is an error during conversion.
    """
    if not check_package("PIL", "Pillow is required to convert images."):
        raise ImportError("Pillow library is required to convert images. Please install it using 'pip install Pillow'.")
    from PIL import Image
    import numpy as np
    import os

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Input image file '{image_path}' does not exist.")

    try:
        with Image.open(image_path) as img:
            img_np = np.array(img)

            # If image has alpha channel (RGBA)
            if img_np.ndim == 3 and img_np.shape[2] == 4:
                alpha_channel = img_np[:, :, 3] / 255.0  # Normalize alpha
                rgb_channels = img_np[:, :, :3] * alpha_channel[:, :, np.newaxis]
                rgb_channels = rgb_channels.astype(np.uint8)

            # If image is already RGB (3 channels)
            elif img_np.ndim == 3 and img_np.shape[2] == 3:
                rgb_channels = img_np

            else:
                raise Exception(
                    f"Unsupported image format for '{image_path}'. "
                    f"Expected 3 (RGB) or 4 (RGBA) channels, got shape {img_np.shape}"
                )

            if crop_shape is not None:
                rgb_channels = rgb_channels[
                    crop_shape[0]:crop_shape[1],
                    crop_shape[2]:crop_shape[3],
                    :
                ]

            output_image = Image.fromarray(rgb_channels)
            output_image.save(output_path)

    except Exception as e:
        raise Exception(f"Error converting '{image_path}' to '{output_path}': {e}")