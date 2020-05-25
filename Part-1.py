import cv2
import pytesseract
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('my adhaar.PNG')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
boxes = pytesseract.image_to_data(img,config='-psm 6',lang='eng') #Finding words in image using Tesseract
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
        if re.match("^[0-9 ]+$", word[-1]):
            wordsmatching.append(word)
for approword in approwords:
    print(approword)
uniquelines=[]          #storing all the words lying in same line which matched in regex
for wmatch in wordsmatching:
    if wmatch[7] not in uniquelines:
        uniquelines.append(wmatch[7])
for i in uniquelines:
    allAdhaarwords=[]       #allAdhaarwords represent findings of all adhaar numbers in adhaar card
    count=0
    adhaarwords=[]          #adhaarwords are stored in this list
    for wmatch in wordsmatching:
        #finding all the words which lie on the the same line
        if int(i)>int(wmatch[7])-5 and int(i)<int(wmatch[7])+5:
            count+=1
            adhaarwords.append(wmatch)
    #if we found proper adhaar number append to allAdhaarwords list
    if count>=3:
        allAdhaarwords.append(adhaarwords)
        adhaarwords=[]
        break
#print adhaar number
print("-------adhaar number--------")
adhaar_num=''
for adhaarword in allAdhaarwords:
    for i in adhaarword:
        adhaar_num+=i[-1]
print(adhaar_num)
#
# img=cv2.resize(img,(640,640))
cv2.imshow('img', img)
cv2.waitKey(0)