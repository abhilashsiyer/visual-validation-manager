import uuid

import cv2
import imutils
from skimage import io
from skimage import metrics

from image_kit.file_uploader import upload_image


def validate_image(file_url_as_base, file_url_for_compare):
    # load the two input images
    imageA = url_to_image(file_url_as_base)
    # imageA = cv2.imread(file_base)
    imageB = url_to_image(file_url_for_compare)

    # Match size of both images
    # Get height and width of imageA
    height = int(imageA.shape[0])
    width = int(imageA.shape[1])
    dim = (width, height)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = metrics.structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    if score == 1.0:
        return {'message': 'Validation successful with base', "validation_result": True,
                'baseImage': file_url_as_base}
    else:
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # show the output images
    diff_image_name = "diff-" + str(uuid.uuid1())
    diff_image_name_ext = diff_image_name + ".png"
    cv2.imwrite(diff_image_name_ext, imageB)
    download_url = upload_image(diff_image_name_ext, diff_image_name)

    import os
    if os.path.exists(diff_image_name_ext):
        os.remove(diff_image_name_ext)
    else:
        print("The file does not exist")

    return {'message': 'Validation failed with base', "validationResult": False,
            'imageDiffResult': download_url, 'baseImage': file_url_as_base}


def url_to_image(url):
    image = io.imread(url)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_bgr


# image_to_compare = upload_image("uploads/Q_Emu.png","Base-Image")
# print(image_to_compare)
# result = validate_image("https://ik.imagekit.io/it41uxh5d/qantas_base_dup_PCYbGwoBJ",
#                         "https://ik.imagekit.io/it41uxh5d/Base-Image_gZ56WVj7d")
# print(result)

# url_to_image("https://ik.imagekit.io/it41uxh5d/qantas_base_dup_PCYbGwoBJ")
