import cv2
import numpy as np
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
img=cv2.imread('hello.TIF',0)
#histogram Equalisation
print(img)
oimg=cv2.imread('hey1.PNG')
# num_rows, num_cols = img.shape[:2]
# rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 180, 1)
# img_rotation = cv2.warpAffine(img, rotation_matrix, (num_cols, num_rows))
cv2.imshow('Rotation', img)
cv2.waitKey()
#dst = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
kernel = np.ones((1,1), np.uint8)
th3 = cv2.erode(th3, kernel, iterations=3)
th3 = cv2.bilateralFilter(th3,9,150,75)
blur = cv2.GaussianBlur(th3,(3,3),0)
cv2.imshow("hello",th3)
cv2.waitKey(0)
def aadharNumVerify(adharNum: str) -> bool:
    """
    Takes a N digit aadhar number and
    returns a boolean value whether that is Correct or Not
    """
    verhoeff_table_d = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

    verhoeff_table_p = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

    # verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def checksum(s: str) -> int:
        """For a given number generates a Verhoeff digit and
        returns number + digit"""
        c = 0
        for i, item in enumerate(reversed(s)):
            c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
        return c

    # Validate Verhoeff checksum
    return checksum(adharNum) == 0 and len(adharNum) == 12
def extract_text(th3):
    img1 = th3
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img1,config='-psm 6',lang='eng') #Finding words in image using Tesseract
    words=[]        #storing all words in words list
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                words.append(b)
    print(words)
    approwords=[]
    wordsmatching=[]    #storing all words matching the regex in wordsmatching list
    for word in words:
        if len(word[-1])>1 and len(word[-1])<5:
            approwords.append(word)
            if re.match("^[0-9]+$", word[-1]):
                wordsmatching.append(word)
    resized = cv2.resize(img, (img.shape[0]//2,img.shape[1]//2), interpolation=cv2.INTER_AREA)
    cv2.imshow('Result', resized)
    cv2.waitKey(0)
    uniquelines=[]          #storing all the words lying in same line which matched in regex
    for wmatch in wordsmatching:
        if wmatch[7] not in uniquelines:
            uniquelines.append(wmatch[7])
    allAdhaarwords = []
    uniquewords=[]
    for i in uniquelines:
        print(i)
        #allAdhaarwords represent findings of all adhaar numbers in adhaar card
        count=0
        adhaarwords=[]          #adhaarwords are stored in this list
        if  i not in uniquewords:
            for wmatch in wordsmatching:
                #finding all the words which lie on the the same line
                if int(i)>int(wmatch[7])-10 and int(i)<int(wmatch[7])+10:
                    count+=1
                    uniquewords.append(wmatch[7])
                    adhaarwords.append(wmatch)
            #if we found proper adhaar number append to allAdhaarwords list
        if count>=3:
            allAdhaarwords.append(adhaarwords)
    #print adhaar number
    print("-------adhaar number--------")
    adhaar_num=[]
    k=0
    for adhaarword in allAdhaarwords:
        print(adhaarword)
        widt=0
        x = int(adhaarword[0][6])
        y = int(adhaarword[0][7])
        h = int(adhaarword[0][9])
        adhaar_num.append('')
        for i in adhaarword:
            adhaar_num[k]+=i[-1]
            las=int(i[8])
            widt += int(i[8])
        if k==1:
            widt-=las
        k+=1
        if aadharNumVerify(adhaar_num[k]):
            cv2.rectangle(oimg, (x, y), (x + widt+20, y + h), (0,0,0), cv2.FILLED)
            resized = cv2.resize(oimg, (img.shape[0]//2 , img.shape[1]//2), interpolation=cv2.INTER_AREA)
            cv2.imshow('Result', resized)
            cv2.waitKey(0)
        else:
            adhaar_num[k]=''
    print(adhaar_num)
    return adhaar_num
adhaar1=extract_text(th3)
adhaar2=extract_text(blur)
#img=cv2.resize(img,(640,640))
print(adhaar1[0])
cv2.waitKey(0)
