import math
import matplotlib.pyplot as plt

from matplotlib.colors import NoNorm, Normalize

from improutils.other import *
from improutils.acquisition.img_io import copy_to
from improutils.preprocessing.preprocessing import rotate


def plot_images(*imgs, titles=[], channels='bgr', normalize=False, ticks_off=True, title_size=32):
    assert channels.lower() in ['bgr', 'rgb', 'mono'], 'Possible values for channels are: bgr, rgb or mono!'

    #     f = plt.figure(figsize=(30, 20))
    width_def = 60
    height_def = 60

    width = math.ceil(math.sqrt(len(imgs)))
    height = math.ceil(len(imgs) / width)

    height_def = height_def / 5 * width
    #     print(height_def)
    if height_def > 65:
        height_def = 65

    f = plt.figure(figsize=(width_def, height_def))

    #     print(str(width) + ' , ' + str(height))
    for i, img in enumerate(imgs, 1):
        ax = f.add_subplot(height, width, i)
        if ticks_off:
            ax.axis('off')

        if len(titles) != 0:
            if len(imgs) != len(titles):
                print('WARNING titles length is not the same as images length!')

            try:
                ax.set_title(str(titles[i - 1]), fontdict={'fontsize': title_size, 'fontweight': 'medium'})
            except:
                pass

        if channels.lower() == 'mono' or img.ndim == 2:
            if normalize:
                norm = Normalize()
            else:
                norm = NoNorm()
            ax.imshow(img, cmap=plt.get_cmap('gray'), norm=norm)
        elif channels.lower() == 'rgb':
            ax.imshow(img)
        else:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def show_images(*imgs, scale=1, window_name='Image preview'):
    """ Opens multiple image previews depending on the length of the input *imgs list.
    The preview is terminated by pressing the 'q' key.

    Parameters
    ----------
    *imgs : list
        Multiple input images which have to be shown.
    scale : double
        Scale of shown image window.
    window_name : Optional[string]
        An optional window name.
    Returns
    -------
    None

    See known bug for Mac users
    ---------------------------
    https://gitlab.fit.cvut.cz/bi-svz/bi-svz/issues/13
    """

    def print_xy(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            print('x = %d, y = %d' % (x, y))

    for i, img in enumerate(imgs, 1):
        h, w = img.shape[:2]
        window_name_id = window_name + ' ' + str(i)
        cv2.namedWindow(window_name_id, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(window_name_id, int(w * scale), int(h * scale))
        cv2.setMouseCallback(window_name_id, print_xy)
        cv2.moveWindow(window_name_id, (i - 1) * int(w * scale), 0)

    while 1:
        for i, img in enumerate(imgs, 1):
            cv2.imshow(window_name + ' ' + str(i), img)

        k = cv2.waitKey(0)

        if k == ord('q') or k == ord('Q') or k == 27:
            break

    cv2.destroyAllWindows()


def show_camera_window(*imgs, scale=1):
    def print_xy(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            print('x = %d, y = %d' % (x, y))

    for i, img in enumerate(imgs, 1):
        window_name_id = 'Camera capture' + ' ' + str(i)

        h, w = img.shape[:2]
        cv2.namedWindow(window_name_id, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(window_name_id, int(w * scale), int(h * scale))
        cv2.setMouseCallback(window_name_id, print_xy)
        if len(imgs) > 1:
            cv2.moveWindow(window_name_id, (i - 1) * int(w * scale), 0)
        cv2.imshow(window_name_id, img)


def rotated_rectangle(image, idx):
    ''' Draws rotated rectangle into the image from indexes of binary image.
    You can get the indexes of objects from binary image using cv2.findNonZero().
    Input image is not modified.
    '''
    res = image.copy()
    rect = cv2.minAreaRect(idx)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(res, [box], -1, (255, 255, 255), 1)
    return res, rect


def draw_rotated_text(img, text, point, angle, text_scale, text_color, text_thickness):
    img_filled = np.full(img.shape, text_color, dtype=np.uint8)
    # create rotated text mask
    text_mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    cv2.putText(text_mask, "{:.2f} cm".format(text), point, 0, text_scale, (255, 255, 255), text_thickness)
    if angle > 0:
        angle = -angle + 90
    elif angle < 0:
        angle = angle + 90
    text_mask = rotate(text_mask, -angle, point)
    result = copy_to(img_filled, img.copy(), text_mask)
    return result


def draw_real_sizes(img, rect, width_text, height_text, lbl_size_scale=2, lbl_color=(0, 0, 255), lbl_thickness=8):
    tl, tr, br, bl = order_points(cv2.boxPoints(rect))
    mid_pt_width = midpoint(tl, tr)
    mid_pt_height = midpoint(tr, br)

    # bottom-left points where labels are drawn
    pt_label_first = (int(mid_pt_width[0] - 10), int(mid_pt_width[1] - 10))
    pt_label_second = (int(mid_pt_height[0] + 10), int(mid_pt_height[1]))

    result = draw_rotated_text(img, width_text, pt_label_first, rect[2], lbl_size_scale, lbl_color, lbl_thickness)
    result = draw_rotated_text(result, height_text, pt_label_second, rect[2], lbl_size_scale, lbl_color, lbl_thickness)
    return result
