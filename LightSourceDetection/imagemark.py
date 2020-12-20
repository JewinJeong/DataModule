from __future__ import division

# for v1 human based bbox module
from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import glob
import random

# for v1 network based bbox module
from models import *
from utils.utils import *
from utils.datasets import *
import torch
from torch.utils.data import DataLoader
import time
import cv2
import csv

from skimage.feature import greycomatrix, greycoprops
from skimage import data

imageDir = ''
imageList = []
cur = 0



bb = []
def getglcm(imaAge, x, y):  #cv2_image를 던지는 방법도 존재한다.
    PATCH_SIZE = 21
    cv2_image = cv2.imread(imaAge,cv2.IMREAD_GRAYSCALE)
    #print("cv2 img is :: " + str(cv2_image))

    A_locations = [(y, x)]
    A_patches = []
    for loc in A_locations:
        A_patches.append(cv2_image[loc[0]:loc[0] + PATCH_SIZE,
                                   loc[1]:loc[1] + PATCH_SIZE])

    contrast = []
    dissimilarity = []
    homogeneity = []
    ASM = []
    energy= []
    correlation = []
    entropy = []
    a = []

    for patch in A_patches:
        glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
        bb.append(glcm)
        contrast.append(greycoprops(glcm, 'contrast')[0, 0])
        dissimilarity.append(greycoprops(glcm, 'dissimilarity')[0, 0])
        homogeneity.append(greycoprops(glcm, 'homogeneity')[0, 0])
        ASM.append(greycoprops(glcm, 'ASM')[0, 0])
        energy.append(greycoprops(glcm, 'energy')[0, 0])
        correlation.append(greycoprops(glcm, 'correlation')[0,0])
        #print(glcm.shape)
        #a.append(greycoprops(glcm, 'corddddation'))

        #entropy.append(greycoprops(glcm, 'entropy')[0,0])







    #print(contrast)
    #print(dissimilarity)
    #print(homogeneity)
    #print(ASM)
    #print(energy)
    #print(correlation)



    tmp = []
    tmp.append(contrast[0])
    tmp.append(dissimilarity[0])
    tmp.append(homogeneity[0])
    tmp.append(ASM[0])
    tmp.append(energy[0])
    tmp.append(correlation[0])
    #tmp.append(contrast, dissimilarity, homogeneity, ASM, energy, correlation)
    #rdr.writerow(tmp)
    #print(entropy)

    #각각 아웃풋의 갯수 ---> A_location의 갯수

    return tmp





'''
extlist = ["*.jpeg", "*.jpg", "*.png", "*.bmp"]
for e in extlist:
    filelist = glob.glob(os.path.join(imageDir, e))
    imageList.extend(filelist)

f = open('lighttest.csv', 'a', encoding='utf-8', newline='')
rdr = csv.writer(f)
#wr.writerow(배열) 과 같은 식으로 edit 한다


#print(rdr)
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("마우스 이벤트 발생, x:", x ," y:", y) # 이벤트 발생한 마우스 위치 출력
        lobster(imageList[cur], x, y) #glcm 정답 레이블 저장 이벤트
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_callback)


while cur<len(imageList):


    img = cv2.imread(imageList[cur])
    cv2.imshow("image", img)

    cur =  cur+1
    k = cv2.waitKey(0)
    if k == ord('c'):
        break


f.close()

'''



