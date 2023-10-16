#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-05-19 10:40
#
import cv2


# 漫画风格
def comics():
    img_rgb = cv2.imread(r"D:\Programs\Python\Jasonqwu\Packages\aaa.jpg",
                         cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_edge = cv2.adaptiveThreshold(img_gray,
                                     255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=3,
                                     C=2)
    # cv2.imshow("img_blur", img_edge)
    # cv2.waitKey(0)
    cv2.imwrite(r"D:\Programs\Python\Jasonqwu\Packages\bbb.jpg", img_gray)
    cv2.imwrite(r"D:\Programs\Python\Jasonqwu\Packages\ccc.jpg", img_edge)


# 写实风格
def realistic():
    img_rgb = cv2.imread(r"D:\Programs\Python\Jasonqwu\Packages\aaa.jpg",
                         cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, ksize=(21, 21), sigmaX=0, sigmaY=0)
    # cv2.imshow("img_blur", img_blur)
    # cv2.waitKey(0)
    img_blend = cv2.divide(img_gray, img_blur, scale=255)
    cv2.imwrite(r"D:\Programs\Python\Jasonqwu\Packages\ddd.jpg", img_blur)
    cv2.imwrite(r"D:\Programs\Python\Jasonqwu\Packages\eee.jpg", img_blend)


if __name__ == '__main__':
    comics()
    realistic()