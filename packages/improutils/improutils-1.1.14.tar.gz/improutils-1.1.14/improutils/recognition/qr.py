from qreader import QReader
import cv2


def __GRAY2BGR(img):
    """ 
    If the image has shape less than 3, tries to convert it to BGR. Otherwise returns the image unchanged.

    Parameters
    ----------
    img : np.ndarray
        Input image to be converted to BGR.
        
    Returns
    -------
    img: np.ndarray
        Output image in BGR format or in the original format if the conversion failed of the shape was already 3.
    conversion_took_place: bool
        True if the conversion took place, False otherwise.
    """    
    if len(img.shape) < 3:
        try:
            img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
            return img_bgr, True
        except:
            pass
    
    return img, False
    

def qr_init_reader(model_size = 's', min_confidence = 0.5, reencode_to = 'shift_jis'):
    """
    Initializes a QR code reader. If you want to use the detect or decode QR codes on multiple occasions, it is recommended to initialize the reader once and then pass it to the functions.
    For further info refer to: https://github.com/Eric-Canas/qreader
    
    Parameters
    ----------
    model_size : str
        The size of the model to use. It can be 'n' (nano), 's' (small), 'm' (medium) or 'l' (large). Larger models are more accurate but slower. Defaults to 's'.
    min_confidence : float 
        The minimum confidence of the QR detection to be considered valid. Values closer to 0.0 can get more False Positives, while values closer to 1.0 can lose difficult QRs. Default (and recommended): 0.5.
    reencode_to : str | None 
        The encoding to reencode the utf-8 decoded QR string. 
        If None, it won't re-encode. 
        If you find some characters being decoded incorrectly, try to set a Code Page (https://learn.microsoft.com/en-us/windows/win32/intl/code-page-identifiers) that matches your specific charset. 
        Recommendations that have been found useful:
            'shift-jis' for Germanic languages
            'cp65001' for Asian languages  Defaults to 'shift_jis'.

    Returns
    -------
    reader : QReader
        Initialized QR code reader.
    """  
    return QReader(model_size = model_size, min_confidence = min_confidence, reencode_to = reencode_to)
    

def qr_detect_and_decode(img, return_detections = False, is_bgr = True, reader = qr_init_reader()):
    """
    Detects and decodes QR codes in the given image and return the decoded strings (or None, if any of them was detected but not decoded).
    For further info refer to: https://github.com/Eric-Canas/qreader
    
    Parameters
    ----------
    img : np.ndarray
        The image to be read. It is expected to be RGB or BGR (uint8). Format (HxWx3). Can also be grayscale (HxW), in which case it will be converted to BGR.
    return_detections : bool
        If True, it will return the full detection results together with the decoded QRs. If False, it will return only the decoded content of the QR codes. Defaults to False.
    is_bgr : bool
        If True, the received image is expected to be BGR instead of RGB. Defaults to True.
    reader : QReader
        Initialized QReader class, use qr_init_reader(model_size, min_confidence, reencode_to) with different parameters if you wish. Defaults to qr_init_reader().

    Returns
    -------
    detections : tuple[dict[str, np.ndarray | float | tuple[float | int, float | int]], str | None] OR decoded_strings : tuple[str | None, ...]
        If return_detections is True, it will return a tuple of tuples. Each tuple will contain the detection result (a dictionary with the keys 'confidence', 'bbox_xyxy', 'polygon_xy'...) and the decoded QR code (or None if it can not be decoded). 
        If return_detections is False, it will return a tuple of strings with the decoded QR codes (or None if it can not be decoded).
    """    
    # if the image is in grayscale, convert it to BGR
    img, converted  = __GRAY2BGR(img)  
    return reader.detect_and_decode(img, return_detections = return_detections, is_bgr = is_bgr if converted == False else True)

def qr_decode(img, detection_result, is_bgr = True, reader = qr_init_reader()):
                
    """
    Decodes a single QR code on the given image, described by a detection_result.
    For further info refer to: https://github.com/Eric-Canas/qreader
    
    Internally, this method will run the pyzbar decoder, using the information of the detection_result, to apply
    different image preprocessing techniques that heavily increase the decoding rate.

    Parameters
    ----------
    image : np.ndarray
        The image to be read. It is expected to be RGB or BGR (uint8). Format (HxWx3). Can also be grayscale (HxW), in which case it will be converted to BGR.
    detection_result : dict[str, np.ndarray|float|tuple[float|int, float|int]]
        One of the detection dicts returned by the detect method. Note that qr_detect() returns a tuple of these dicts. This method expects just one of them.
    is_bgr : bool 
        If True, the received image is expected to be BGR instead of RGB. Defaults to True.
    reader : QReader
        Initialized QReader class, use qr_init_reader(model_size, min_confidence, reencode_to) with different parameters if you wish. Defaults to qr_init_reader().
    
    Returns
    -------
    decoded_strings : str OR None 
        The decoded content of the QR code or None if it can not be read.
    """    
    # if the image is in grayscale, convert it to BGR
    img, converted = __GRAY2BGR(img)  
        
    if is_bgr or converted == True:
        # decode expects RGB images
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return reader.decode(img, detection_result)

def qr_detect(img, is_bgr = True, reader = qr_init_reader()):
    """
    Detects QR codes in the image and returns a tuple of dictionaries with all the detection information.
    For further info refer to: https://github.com/Eric-Canas/qreader

    Parameters
    ----------
    image : np.ndarray 
        The image to be read. It is expected to be RGB or BGR (uint8). Format (HxWx3).
    is_bgr : bool 
        If True, the received image is expected to be BGR instead of RGB. Defaults to True.
    reader : QReader 
        Initialized QReader class, use qr_init_reader(model_size, min_confidence, reencode_to) with different parameters if you wish. Defaults to qr_init_reader().
        
    Returns
    -------
    detections : tuple[dict[str, np.ndarray|float|tuple[float|int, float|int]]]: 
        A tuple of dictionaries containing the following keys:
            - 'confidence': float. The confidence of the detection.
            - 'bbox_xyxy': np.ndarray. The bounding box of the detection in the format [x1, y1, x2, y2].
            - 'cxcy': tuple[float, float]. The center of the bounding box in the format (x, y).
            - 'wh': tuple[float, float]. The width and height of the bounding box in the format (w, h).
            - 'polygon_xy': np.ndarray. The accurate polygon that surrounds the QR code, with shape (N, 2).
            - 'quad_xy': np.ndarray. The quadrilateral that surrounds the QR code, with shape (4, 2). Fitted from the polygon.
            - 'padded_quad_xy': np.ndarray. An expanded version of quad_xy, with shape (4, 2), that always include all the points within polygon_xy.

            All these keys (except 'confidence') have a 'n' (normalized) version. For example, 'bbox_xyxy' is the bounding box in absolute coordinates, while 'bbox_xyxyn' is the bounding box in normalized coordinates (from 0. to 1.).
    """    
    # if the image is in grayscale, convert it to BGR
    img, converted = __GRAY2BGR(img)  
    return reader.detect(img, is_bgr = is_bgr if converted == False else True)




