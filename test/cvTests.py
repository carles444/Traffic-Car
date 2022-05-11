import cv2 as cv
import numpy as np


if __name__ == '__main__':
    img = cv.imread('../../Documents/Uni/4rt/2nSem/Robotica/projecte/Traffic-Car/data/road.jpg')
    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    gray_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    gray_img = cv.Canny(gray_img, 50 ,150)
    cv.imshow('road', gray_img)
    cv.waitKey()

