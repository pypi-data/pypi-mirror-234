import PIL
from pytesseract import pytesseract

from improutils import negative


def ocr(img_bin, config=''):
    """
    Detects text in the file.

    Parameters
    ----------
    img_bin : ndarray
        Input binary image. White objects on black background.
    config : str
        Model config, refer to: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html, https://muthu.co/all-tesseract-ocr-options/ for correct use.  Defaults to ''.
    Returns
    -------
    The recognized text in the image.
    """
    # Tesseract works with black objects on white background.
    img_bin = negative(img_bin)
    return pytesseract.image_to_string(PIL.Image.fromarray(img_bin), config=config)
