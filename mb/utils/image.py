from .check_package import check_package

__all__ = ['convert_webp_to_jpg']

def convert_webp_to_jpg(image_path: str, output_path: str, format: str = 'JPG', crop_shape = None):
    """
    Convert a WebP image to JPG format. With 4th channel being alpha. Apply alpha channel as mask to RGB channels, then save as JPG.

    Args:
        image_path (str): Path to the input WebP image.
        output_path (str): Path to save the converted format.
        format (str): Output image format. Default is 'JPG'.
        crop_shape (tuple): Optional_croping. (width, height,3). If provided, the image will be cropped to this shape before saving.

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
            if img_np.shape[2] == 4:  # Check if image has alpha
                alpha_channel = img_np[:, :, 3] / 255.0  # Normalize alpha to [0, 1]
                rgb_channels = img_np[:, :, :3] * alpha_channel[:, :, np.newaxis]  # Apply alpha as mask
                rgb_channels = rgb_channels.astype(np.uint8)  # Convert back to uint8

                if crop_shape is not None:
                    width, height, _ = crop_shape
                    rgb_channels = rgb_channels[:height, :width]

                output_image = Image.fromarray(rgb_channels)
                output_image.save(output_path, format=format)
            else:
                raise Exception(f"Input image '{image_path}' does not have an alpha channel. Expected a WebP image with RGBA channels.")
    except Exception as e:
        raise Exception(f"Error converting '{image_path}' to {format}: {e}")