
import cv2
import numpy as np

# convert image to canny and find contours
# count the number of contours whoes area is greater than 200


def predictDieNumber(img):
    imgCanny = cv2.Canny(img, 600, 600)
    contours, hierarchy = cv2.findContours(
        imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    n = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            n = n + 1
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
    return n


img = cv2.imread("./img.jpg")

# crop the image into number of dice
die1 = img[0:130, 0:170]
die2 = img[0:130, 170:]
die3 = img[130:, :115]
die4 = img[130:, 114:230]
die5 = img[130:, 220:]

# imgContour = die1.copy()

# get the number of contours in the image
dienum1 = predictDieNumber(die1)
dienum2 = predictDieNumber(die2)
dienum3 = predictDieNumber(die3)
dienum4 = predictDieNumber(die4)
dienum5 = predictDieNumber(die5)

# put text in the image
cv2.putText(img, "Dots:" + str(dienum1), (80, 130),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "Dots:" + str(dienum2), (200, 130),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "Dots:" + str(dienum3), (30, 260),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "Dots:" + str(dienum4), (140, 260),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "Dots:" + str(dienum5), (250, 260),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

# show image
cv2.imshow("img", img)

# write image to a file
cv2.imwrite('labelledDice.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
