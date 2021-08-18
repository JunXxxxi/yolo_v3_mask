import sys
import argparse

import cv2

from yolo import YOLO, detect_video1, detect_video2
import numpy as np
from PIL import Image

def detect_img(yolo):
    n = input('请输入编号（1.人脸口罩检测；2.口罩规范佩戴识别）：')
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            if n == '1':
                r_image,hm,nm = yolo.detect_image2(image)
                hm_text = 'number of have_mask: ' + str(hm)
                nm_text = 'number of no_mask: ' + str(nm)
                # result = np.asarray(image)
                width, height = r_image.size
                data = np.asarray(r_image)
                cv2.putText(data, text=hm_text, org=(3, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.8, color=(0, 255, 0), thickness=2)
                cv2.putText(data, text=nm_text, org=(3, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.8, color=(255, 0, 0), thickness=2)
                result_ = np.reshape(data, (height, width, 3))
                img = Image.fromarray(result_)
                img.show()
            elif n == '2':
                r_image = yolo.detect_image(image)
                r_image.show()
    yolo.close_session()



FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )


    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        while 1:
            detect_video1(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
