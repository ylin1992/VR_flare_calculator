# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 10:07:01 2020

@author: Ewan Yeh Lin
"""
# =============================================================================
# The program evaluates flare effect based on stadardized specification
# 18844, in which a normal exposured image (IM1, with 225 grey level), a plane
# black image (IM2) captured with the same exposure value as IM1 and an over-
# exposured (normally 8x) image are fed.
# A map (cnt_mtx) is generated and a result image (rgb_img) is saved to the 
# root file.
# =============================================================================
import numpy as np
import cv2
from . import filter as blm

RATIO_E1_E3 = 8 
RATIO_CONTOUR_REGION = 50/70
THRESHOLD = 0.1
NUM_H, NUM_W = 7, 7
VISUALIZATION_ON = False
contour_x_limit = [800,3200]
contour_y_limit = [400,2800]

def find_avg_intensity_in_contour(img, cnt):
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    tmp_mask = np.zeros_like(img)
    r = (cv2.contourArea(cnt) / np.pi)**0.5 * RATIO_CONTOUR_REGION
    tmp_mask = cv2.circle(tmp_mask,(cX,cY),int(r),255,-1)
    return np.sum(img[tmp_mask>0]) / (np.pi*r**2), tmp_mask

def find_avg_intensity_around_contour(img, cnt):
# =============================================================================
# The function calculates average intensity around a found contour in a 
# given image
# img: input image
# cnt: contour array
# return: float 
# =============================================================================
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    r = (cv2.contourArea(cnt) / np.pi)**0.5
    d = int((1 + RATIO_CONTOUR_REGION) * r)
    tmp_mask = np.zeros_like(img)
    tmp_mask = cv2.circle(tmp_mask,(cX - d,cY),int(r * RATIO_CONTOUR_REGION),255,-1)
    tmp_mask = cv2.circle(tmp_mask,(cX + d,cY),int(r * RATIO_CONTOUR_REGION),255,-1)
    tmp_mask = cv2.circle(tmp_mask,(cX,cY - d),int(r * RATIO_CONTOUR_REGION),255,-1)
    tmp_mask = cv2.circle(tmp_mask,(cX,cY + d),int(r * RATIO_CONTOUR_REGION),255,-1)

    return np.sum(img[tmp_mask>0]) / (np.pi*r**2) / 4, tmp_mask

def run(imWhite_1x, imBlack_1x, imWhite_8x):
    result_img = imWhite_1x.copy()

    imWhite_1x = cv2.cvtColor(imWhite_1x, cv2.COLOR_BGR2GRAY)
    imBlack_1x = cv2.cvtColor(imBlack_1x, cv2.COLOR_BGR2GRAY)
    imWhite_8x = cv2.cvtColor(imWhite_8x, cv2.COLOR_BGR2GRAY)


    filt_img = blm.clc_blm(imWhite_1x,0.01,0.2)
    thr_tst = np.zeros_like(imWhite_1x)
    thr_tst[filt_img>THRESHOLD] = 255

    ret, thr_imWhite_1x = cv2.threshold(imWhite_1x,THRESHOLD,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thr_tst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cnt_list = []
    cnt_center_list = np.array((0,0))
    mask = np.zeros_like(imWhite_1x)
    ### Check performance of coontour-finding process
    ### TODO: Exception for contours noise within
    for c in contours:
        if cv2.contourArea(c) > 5000 and cv2.contourArea(c) < 12000 and c[0][0][1] > contour_y_limit[0] and c[0][0][1] < contour_y_limit[1] and c[0][0][0] > contour_x_limit[0] and c[0][0][0] < contour_x_limit[1]: # c[0][0][0]>150 -> temporal solution
            cv2.drawContours(mask, [c], -1, 255, -1)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cnt_center_list = np.c_[cnt_center_list,np.array((cX,cY))]
            cnt_list.append(c)
    cnt_center_list =cnt_center_list.transpose((1,0))[1::,:]

    ### Calculate average intensity within each contour

    cnt_info_list = []
    for c in cnt_list:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        yb3,_ = find_avg_intensity_in_contour(imWhite_8x, c)
        yb2, mask_b = find_avg_intensity_in_contour(imBlack_1x, c)
        yw1, mask_w = find_avg_intensity_around_contour(imWhite_1x, c)
        f = (yb3 / RATIO_E1_E3 - yb2) / yw1 * 100
        cnt_info_list.append([cX,cY,f])
        result_img[mask_b>0,2] = 255
        result_img[mask_w>0,0] = 255
        cv2.putText(result_img, str(np.round(f,2)), (c[0][0][0],c[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 1, cv2.LINE_AA)



    ### sorting
    cnt_mtx = np.zeros((NUM_H,NUM_H))
    for i in range(0,NUM_H):
        tmp_arr = np.array(cnt_info_list[i*NUM_H:(i+1)*NUM_H])

        arg = np.argsort((tmp_arr[:,0]))
        # print (arg)
        # print (tmp_arr)
        c = 0
        for idx in arg:
            cnt_mtx[NUM_H - i -1,c] = tmp_arr[idx,2]
            c += 1
    print (np.mean(cnt_mtx))

    return np.mean(cnt_mtx), result_img



if __name__ == '__main__':
    res, result_im = run(
        cv2.imread('white_1x.png'),
        cv2.imread('white_8x.png'),
        cv2.imread('blk_1x.png')
    )
