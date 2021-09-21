# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:02:26 2019

@author: 10601021
"""
import numpy as np
import cv2
def butter2d_lp( shape, f, n):
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols) * cols
    y = np.linspace(-0.5, 0.5, rows) * rows
    radius = np.sqrt((x ** 2)[np.newaxis] + (y ** 2)[:, np.newaxis])
    filt = 1 / (1.0 + (radius / f) ** (2 * n))
    return filt
def butter2d_bp( shape, cutin, cutoff, n):
    return butter2d_lp(shape, cutoff, n) - butter2d_lp(shape, cutin, n)
def crop_center_and_relocate(im):
    y = len(im)
    x = len(im[0])
    im_crop = im[y//5:y*4//5,x//4:x*4//5]
    canvas = np.zeros((y,x))
    canvas[y//5:y*4//5,x//4:x*4//5] = im_crop
    return canvas
def find_sectioned_signal(im, c,delta_y):
    arr_avg = np.zeros(len(im[0]))
    for i in range(0,len(im[0])):
        temp = im[c - delta_y:c + delta_y, i]
        arr_avg[i] = np.average(temp)
    return arr_avg
def normalize_img(im):
    return (im - im.min()) * 255 / (im.max()- im.min())

def find_where_higher_than_zero(immm):
    a = []
    for x in range(0,len(immm[0])):
        for y in range(0,len(immm)):
            if immm[y,x] > 0:
                a.append((y,x))


def clc_blm(orig_image,lowf,highf):
    shape = orig_image.shape
    rows, cols = shape

    cutin = lowf * (cols / 2)
    cutoff = highf * (cols / 2)
    fft_orig = np.fft.fftshift(np.fft.fft2(orig_image))

    filt = butter2d_bp(orig_image.shape, cutin, cutoff,2)
    fft_new = fft_orig * filt * -1
    new_image = np.fft.ifft2(np.fft.ifftshift(fft_new))
    new_image = np.abs(new_image)

    norm_img = new_image / np.mean(orig_image)
    print ("Normalizing facotr: " + str(np.mean(orig_image[orig_image.shape[1]*2//5:orig_image.shape[1]*3//5,orig_image.shape[0]*2//5:orig_image.shape[0]*3//5])))
    print ("Max = " +str(norm_img.max()))

    return norm_img
