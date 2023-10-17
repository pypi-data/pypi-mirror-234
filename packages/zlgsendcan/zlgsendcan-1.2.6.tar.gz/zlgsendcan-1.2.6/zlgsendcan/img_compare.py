from airtest.aircv.multiscale_template_matching import MultiScaleTemplateMatching
from airtest.aircv import imread
from airtest.core.api import *

def img_compare(im_search, im_source, threshold=0.8):
    img_cv = imread(im_search)
    img_cv2 = imread(im_source)
    img_obj = MultiScaleTemplateMatching(threshold=threshold, im_search=img_cv, im_source=img_cv2)
    result = img_obj.find_best_result()
    if result is None:
        return False
    else:
        return True


def qnx_assert(im_search, im_source, threshold=0.8):
    re = img_compare(im_search, im_source, threshold=threshold)
    assert_equal(re,assert_equal)
    return re


if __name__ == '__main__':
    img1 = 'D:\\bmp\search.png'
    img2 = 'D:\\bmp\QNX.bmp'
    qnx_assert(img1, img2,threshold=0.99)
