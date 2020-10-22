import cv2
import numpy as np

# divies the images into different pars according to identified frames
# returns lists of x-coordinate, y-coordinate , width and height of each frame


def getDie(img):

    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    objNum = len(contours)
    x, y, width, height = [], [], [], []
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 200:

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            a, b, w, h = cv2.boundingRect(approx)
            x.append(a)
            y.append(b)
            width.append(w)
            height.append(h)
            cv2.putText(imgContour, "Dots:", (a+(w//2)-10, b+h-4),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.rectangle(imgContour, (a, b),
                          (a+w, b+h), (0, 255, 0), 3)

            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
            # cv2.imshow("Contour", imgContour)

    return x, y, width, height, objNum

# calculates the number of countours in each image


def predictDie(img):
    imgCanny = cv2.Canny(img, 50, 50)

    contours, hierarchy = cv2.findContours(
        imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow("img101", imgCanny)
    n = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            n = n + 1
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
    return n


originalImage = cv2.imread("./inp1.png")
oheight = originalImage.shape[0]
owidth = originalImage.shape[1]

# increasing the height of the image because divided image is to small for a normal frame
img = cv2.resize(originalImage, (500, 500))


imgContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)


# cv2.imshow("Grey", imgGray)
# cv2.imshow("Blur", imgBlur)
# cv2.imshow("Canny", imgCanny)
x, y, width, height, objnum = getDie(imgCanny)

# crop the image into number of dice
die = []
for i in range(objnum):

    die.append(img[y[i]: y[i] + height[i], x[i]: x[i] + width[i]])
    # cv2.imshow("die"+str(i), die[i])

    n = predictDie(die[i])
    cv2.putText(img, "Dots:"+str(n), (x[i]+(width[i]//2)-50, y[i]+height[i]-4),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
imgOriginal = cv2.resize(img, (owidth, oheight))
cv2.imshow("Original", imgOriginal)

# write image to a file
cv2.imwrite('labelledDice.png', imgOriginal)

cv2.waitKey(0)
cv2.destroyAllWindows()
