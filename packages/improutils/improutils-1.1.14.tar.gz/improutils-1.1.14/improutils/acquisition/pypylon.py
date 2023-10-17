from pypylon import pylon


def connect_camera(serial_number):
    """
    Connects the camera specified with its serial number

    Parameters
    ----------
    serial_number : string
        The camera's serial number.
    Returns
    -------
    camera : object
    """
    info = None
    for i in pylon.TlFactory.GetInstance().EnumerateDevices():
        if i.GetSerialNumber() == serial_number:
            info = i
            break
    else:
        print('Camera with {} serial number not found'.format(serial_number))

    # VERY IMPORTANT STEP! To use Basler PyPylon OpenCV viewer you have to call .Open() method on you camera
    if info is not None:
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(info))
        camera.Open()
        return camera
    else:
        return None
