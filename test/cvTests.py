import cv2 as cv
import numpy as np
import math
"""
steps:
1.region of interest
2.grayscale
3.maximize contrast
4.gaussian blur?
4.canny
5.houfh transform
dst
"""

def max_contrast(img):
    return (255 * ((img - img.min()) / (img.max() - img.min()))).astype(np.uint8)

if __name__ == '__main__':
    # load image
    img = cv.imread('data/road2.jpg')
    
    # resize image
    img = cv.resize(img, (img.shape[1]*2, img.shape[0]*2))
    
    # convert to grayscale
    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    cv.imshow('road', gray_img)
    cv.waitKey()
    
    # region of interest
    roi_img = gray_img[int(gray_img.shape[0] / 2) + 100:, int(gray_img.shape[1] / 2) - 170:gray_img.shape[1] - 170]
    roi_img2 = np.copy(roi_img)
    
    # maximize contrast
    contrast_img = max_contrast(roi_img)
    cv.imshow('road', contrast_img)
    cv.waitKey()
    
    # gray_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    
    # canny edge detection
    canny_img = cv.Canny(contrast_img, 100 ,200, None, 3)
    cv.imshow('road', canny_img)
    cv.waitKey()
    
    # hough transform
    """    lines = cv.HoughLines(canny_img, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(roi_img2, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    cv.imshow('road', roi_img2)
    cv.waitKey()
    """
    
    linesP = cv.HoughLinesP(canny_img, 1, np.pi / 180, 50, None, 50, 10)
  
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(roi_img, (l[0], l[1]), (l[2], l[3]), 255, 1, cv.LINE_AA)
            
    cv.imshow('road', roi_img)
    cv.waitKey()
