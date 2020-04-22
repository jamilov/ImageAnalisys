import math

from PIL import ImageFilter
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from dialog import message


def loadImage(string):
    global pix
    global width, height, draw, image, filepath
    image = Image.open(string)
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    filepath = string


num = 0


def saveImage():
    global image, num
    try:
        image.save('Image_' + str(num) + '.png')
        num += 1
        message("Сохранение", "Изображение сохранено")
    except NameError:
        message("Ошибка сохранения", "Изображение не создано!")


def isGray():
    global width, height, draw, image, pix
    for x in range(width):
        for y in range(height):
            if pix[x, y][0] != pix[x, y][1] and pix[x, y][0] != pix[x, y][2]:
                return False
    return True


# Усреднение
def average():
    global pix, width, height, draw, image
    for x in range(width):
        for y in range(height):
            r = pix[x, y][0]
            g = pix[x, y][1]
            b = pix[x, y][2]
            sr = (r + g + b) // 3
            image.putpixel((x, y), (sr, sr, sr))
    return ImageQt(image)


# Мера размытости
def firstblur():
    if isGray():
        blur = image.filter(ImageFilter.BLUR)
        bpix = blur.load()

        Dver_sum = 0
        Dhor_sum = 0
        Vver_sum = 0
        Vhor_sum = 0

        Dver = [[0 for j in range(height)] for i in range(width)]
        Dhor = [[0 for j in range(height)] for i in range(width)]
        DBver = [[0 for j in range(height)] for i in range(width)]
        DBhor = [[0 for j in range(height)] for i in range(width)]
        Vver = [[0 for j in range(height)] for i in range(width)]
        Vhor = [[0 for j in range(height)] for i in range(width)]

        for x in range(width):
            for y in range(height):
                if (x > 1):
                    Dver[x][y] = abs(pix[x, y][0] - pix[x - 1, y][0])
                    DBver[x][y] = abs(bpix[x, y][0] - bpix[x - 1, y][0])
                    Vver[x][y] = max(0, Dver[x][y] - DBver[x][y])
                    Dver_sum += Dver[x][y]
                    Vver_sum += Vver[x][y]
                if (y > 1):
                    Dhor[x][y] = abs(pix[x, y - 1][0] - pix[x, y][0])
                    DBhor[x][y] = abs(bpix[x, y - 1][0] - bpix[x, y][0])
                    Vhor[x][y] = max(0, Dhor[x][y] - DBhor[x][y])
                    Dhor_sum += Dhor[x][y]
                    Vhor_sum += Vhor[x][y]
        Fver = (Dver_sum - Vver_sum) / Dver_sum
        Fhor = (Dhor_sum - Vhor_sum) / Dhor_sum
        Fblur = max(Fver, Fhor)
        return Fblur
    else:
        return -1


def secondblur():
    if isGray():
        horSum = 0
        verSum = 0
        bsum = 0
        esum = 0
        B = [[0 for j in range(height)] for i in range(width)]
        Enew = [[0 for j in range(height)] for i in range(width)]
        Dver = [[0 for j in range(height)] for i in range(width)]
        Dhor = [[0 for j in range(height)] for i in range(width)]
        Chor = [[0 for j in range(height)] for i in range(width)]
        Cver = [[0 for j in range(height)] for i in range(width)]
        Ehor = [[0 for j in range(height)] for i in range(width)]
        Ever = [[0 for j in range(height)] for i in range(width)]
        blurHor = [[0 for j in range(height)] for i in range(width)]
        blurVer = [[0 for j in range(height)] for i in range(width)]
        for x in range(1, width):
            for y in range(1, height):
                if 1 < x < width - 1:
                    Dver[x][y] = abs(pix[x - 1, y][0] - pix[x + 1, y][0])
                    verSum += Dver[x][y]
                if 1 < y < height - 1:
                    Dhor[x][y] = abs(pix[x, y - 1][0] - pix[x, y + 1][0])
                    horSum += Dhor[x][y]
        DhorMean = horSum / (width * height)
        DverMean = verSum / (width * height)
        for x in range(1, width):
            for y in range(1, height):
                Chor[x][y] = Dhor[x][y] if Dhor[x][y] > DhorMean else 0
                Cver[x][y] = Dver[x][y] if Dver[x][y] > DverMean else 0
                if 1 < x < width - 1:
                    try:
                        Ever[x][y] = 1 if Cver[x][y] > max(Cver[x - 1][y], Cver[x + 1][y]) else 0
                        blurVer[x][y] = 2 * abs(pix[x, y][0] - (pix[x + 1, y][0] + pix[x - 1, y][0]) / 2) / (
                                pix[x + 1, y][0] + pix[x - 1, y][0])
                    except ZeroDivisionError:
                        pass
                if 1 < y < height - 1:
                    try:
                        Ehor[x][y] = 1 if Chor[x][y] > max(Chor[x][y - 1], Chor[x][y + 1]) else 0
                        blurHor[x][y] = 2 * abs(pix[x, y][0] - (pix[x, y + 1][0] + pix[x, y - 1][0]) / 2) / (
                                pix[x, y + 1][0] + pix[x, y - 1][0])
                    except ZeroDivisionError:
                        pass
                B[x][y] = 1 if max(blurHor[x][y], blurVer[x][y]) > 0.1 else 0
                Enew[x][y] = max(Ever[x][y], Ehor[x][y])
                esum += Enew[x][y]
                bsum += B[x][y]
        Fblur = 1 - (bsum / esum)
        return Fblur
    else:
        return -1


# Мера энтропии
def enthropy():
    hist = [0] * 256
    for x in range(width):
        for y in range(height):
            hist[pix[x, y][0]] += 1
    k = width * height
    sum = 0
    for i in range(256):
        hist[i] /= k
        try:
            sum += hist[i] * math.log2(hist[i])
        except ValueError:
            pass
    return -sum


# Мера сегментации
def segmentation():
    if isGray():
        Useg = [[0 for j in range(height)] for i in range(width)]
        Nseg1 = 0
        Nseg2 = 0
        avg = 0
        for x in range(width):
            for y in range(height):
                avg += pix[x, y][0]
        avg /= width * height

        for x in range(1, width - 1, 3):
            for y in range(1, height - 1, 3):
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        Useg[x][y] += pow(pix[x, y][0] - pix[x - n, y - m][0], 2)

        sum1 = 0
        sum2 = 0
        for x in range(width):
            for y in range(height):
                if pix[x, y][0] > avg:
                    Nseg1 += 1
                    sum1 += Useg[x][y]
                else:
                    Nseg2 += 1
                    sum2 += Useg[x][y]
        W = sum1 / Nseg1 + sum2 / Nseg2
        B = pow((sum1 / Nseg1 - sum2 / Nseg2), -2)
        Fsep = 1000 * W + B
        return round(Fsep, 5)
    else:
        return -1


# Мера резкости
def sharpness():
    if isGray():
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        NSver = 0
        NShor = 0
        D1 = [[0 for j in range(height)] for i in range(width)]
        D2 = [[0 for j in range(height)] for i in range(width)]
        Sver = [[0 for j in range(height)] for i in range(width)]
        Shor = [[0 for j in range(height)] for i in range(width)]
        median = image.filter(ImageFilter.MedianFilter)
        pixels = median.load()
        for x in range(width):
            for y in range(height):
                if 1 < x < width - 2:
                    D2[x][y] = math.trunc(pixels[x + 2, y][0] - pixels[x, y][0]) - math.trunc(
                        pixels[x, y][0] - pixels[x - 2, y][0])
                if 1 < y < height - 2:
                    D1[x][y] = math.trunc(pixels[x, y + 2][0] - pixels[x, y][0]) - math.trunc(
                        pixels[x, y][0] - pixels[x, y - 2][0])
        for x in range(width):
            for y in range(height):
                if 1 < x < width - 2:
                    for i in range(x - 1, x + 2):
                        sum1 += abs(D2[i][y])
                        sum2 += abs(pixels[i, y][0] - pixels[i - 1, y][0])
                        Sver[x][y] = sum1 / sum2 if sum2 != 0 else 0
                if 1 < y < height - 2:
                    for j in range(y - 1, y + 2):
                        sum3 += abs(D1[x][j])
                        sum4 += abs(pixels[x, j][0] - pixels[x, j - 1][0])
                        Shor[x][y] = sum3 / sum4 if sum4 != 0 else 0
                if Shor[x][y] > 0.0001: NShor += 1
                if Sver[x][y] > 0.0001: NSver += 1
        imageWithEdges = image.filter(ImageFilter.FIND_EDGES)
        kol = 0
        pixels = imageWithEdges.load()
        for x in range(imageWithEdges.size[0]):
            for y in range(imageWithEdges.size[1]):
                if pixels[x, y][0] != 0:
                    kol += 1
        Fsharp = math.sqrt(pow(NShor / kol, 2) + pow(NSver / kol, 2))
        return Fsharp
    else:
        return -1


def sharpness2():
    if isGray():
        maxi = 0
        sum = 0
        for x in range(width):
            for y in range(height):
                maxi = max(pix[x, y][0], maxi)
        maxi /= 2
        for x in range(width):
            for y in range(height):
                if 0 < x < width - 1 and 0 < y < height - 1:
                    sum += pow((abs(pix[x, y][0] - pix[x - 1, y][0]) + abs(pix[x, y][0] - pix[x, y - 1][0])), 2)
        sum /= (height - 1) * (width - 1)
        RQ = sum / maxi
        blur = image.filter(ImageFilter.MedianFilter(5))
        bp = blur.load()
        blur.show()
        #blur.save("blur.png")
        blur2 = blur.filter(ImageFilter.MedianFilter(9))
        bp2 = blur2.load()
        blur2.show()
        #blur2.save("blur2.png")
        sum = 0
        for x in range(width):
            for y in range(height):
                sum += bp[x, y][0] - bp2[x, y][0]
        C = sum / (width * height)
        return round(RQ, 5), round(C, 5)
    else:
        return -1
