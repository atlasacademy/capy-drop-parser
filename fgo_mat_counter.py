#################################################################################
##  FGO Materials Parser/Calculator v0.191 ALPHA by Yhsa (4/8/2018)
##  Basic OpenCV Script to count and collate mat icons inside fgo screenshots
##  Free for distribution and use, please give credit where due
##  Thanks to: Officer Artoria, Yuki, Sigma, Snow and the folks of FGO Farmville for their help
#################################################################################


import cv2
import numpy as np
import os
import time
import argparse
import logging
import pytesseract
import re

LABEL = False
DEBUG = True

TRAINING_IMG_HEIGHT = 1080
TRAINING_IMG_WIDTH = 1920
TRAINING_IMG_MAT_SCALE = 0.54
MIN_DISTANCE = 50
DIGIT_MIN_DISTANCE = 9
THRESHOLD = .82
CHAR_THRESHOLD = .65
CHAR_THRESHOLD_LOOSE = .59

REFFOLDER = "ref"
MATFOLDER = "mat_templates"
CHARFOLDER = "characters"
TARGETFOLDER = "nodes"
RESULTSFOLDER = "results"
IMAGEFORMATS = ["png", "jpg"]
DROPMAP = "dropMap.txt"

SUBMISSION_SHEET = "OAs_Counterfeit_-_Submissions.xlsx"

OFFSET_HEIGHT = 75
OFFSET_WIDTH = 13
BASE_HEIGHT = 22
BASE_WIDTH = 80

MAT_CROPX = 115
MAT_CROPY = 100
MAT_CROPW = 800
MAT_CROPH = 335

DEBUG = False

def getOverlap(pt, ptList, distance=MIN_DISTANCE):
    row = pt[1]
    col = pt[0]
    for prevPt in ptList.keys():
        prevRow = prevPt[1]
        prevCol = prevPt[0]
        if(abs(prevRow - row) < distance and abs(prevCol - col) < distance):
            return prevPt
    return None

def isImage(name):
    nameArray = name.split('.')
    ext = nameArray[1]
    return (ext in IMAGEFORMATS)

def getCharTagValue(char):
    array = char.split("_")
    valueChar = array[1]
    return valueChar

def countMat(targetImg, matName, matTemplate, charImgMap, ptList):
    w, h = matTemplate.shape[:-1]
    res = cv2.matchTemplate(targetImg, matTemplate, cv2.TM_CCOEFF_NORMED)
    loc = np.asarray(res >= THRESHOLD).nonzero()

    # Reverse rows and columns of the matrix so that coordinates are relative to (0,0) [column, row] being the upper left of the image
    # instead of the traditional indexing of a multidimensional array [row, column].
    # This means that when indexing back into the res array the indexes will need to be swapped agian.
    for pt in zip(*loc[::-1]):
        score = res[pt[1]][pt[0]]
        overLapPt = getOverlap(pt, ptList)
        if(overLapPt == None):
            ptList[pt] = (matName, score)
        else:
            oldScore = ptList[overLapPt][1]
            if(score > oldScore):
                ptList[overLapPt] = (matName, score)


def getCharactersFromImage(matWindow, charImgMap, imgName, matName, pt, threshold, LABEL):
    col = pt[0]
    row = pt[1]
    charPtList = {}

    resultsImg = None

    if(LABEL):
        resultsImg = matWindow.copy()

    for char in charImgMap.keys():
        charTemplate = charImgMap[char]
        charValue = getCharTagValue(char)
        w, h = charTemplate.shape[:-1]

        charRes = cv2.matchTemplate(matWindow, charTemplate, cv2.TM_CCOEFF_NORMED)
        charLoc = np.where(charRes >= threshold)

        for cpt in zip(*charLoc[::-1]):  # Switch collumns and rows
            charScore = charRes[cpt[1]][cpt[0]]
            overlapCharPt = getOverlap(cpt, charPtList, DIGIT_MIN_DISTANCE)
            if(overlapCharPt == None):
                charPtList[cpt] = (charValue, charScore)
                if(LABEL):
                    cv2.rectangle(resultsImg, cpt, (cpt[0] + h, cpt[1] + w), (0, 0, 255), 1)
                    pass

            else:
                oldCharScore = charPtList[overlapCharPt][1]
                oldCharName = charPtList[overlapCharPt][0]
                if(charScore > oldCharScore):
                    charPtList[overlapCharPt] = (charValue, charScore)
                    #print "old -> new: %s -> %s @ %s [ %f vs %f ] " % (oldCharName, charValue, cpt, oldCharScore, charScore)
    if(LABEL):
        resultsName = "%s_%s_%d_%d_results.png" % (imgName, matName, row, col)
        cv2.imwrite(resultsName, resultsImg)

    #finished evaluating characters, construct number representation of mats
    charValPositionList = []
    for cpt in charPtList.keys():
        (charValue, charScore)  = charPtList[cpt]
        ccol = cpt[0]
        charValPositionList.append((ccol, charValue)) #sort each character img by its relative col position in the img

    charValPositionList = sorted(charValPositionList, key = lambda x: x[0])
    valueString = ""
    prevccol = -1
    for charValue  in charValPositionList:
        if(prevccol >= 0 and ccol - prevccol > DIGIT_MIN_DISTANCE):
            valueString += ' '
        valueString += charValue[1]
    return valueString

def processValueString(valueString, matEntry):
    valueString = valueString.replace('+', '(')
    valueStringArray = valueString.split('(')
    base = valueStringArray[0]
    if('x' in base):
        base = base.strip('x')
    bonus = ""
    if(len(valueStringArray) > 1):
        bonus = valueStringArray[1]
    if(len(base) > 0):
        matvalue = int(base)
        bonusValue = 0
        #if(len(bonus) > 0):
        #    bonusValue = int(bonus)  #not dealing with bonus for now
        #hack for da vinci, possibly replace with a config/collate file specified at top level
        #that lets you collapse mats into a single entry
        if(matEntry == "Manuscript (True)" or matEntry == "Manuscript (False)"):
            matEntry = "Manuscripts (T or F)"
        #line = "     -- Mat %s x%d+(%d)" % (matEntry, matvalue, bonusValue)
        #logging.debug(line)

        matEntry = "%s - %d" % (matEntry, matvalue)
    return matEntry

def checkValueString(valueString):
    #split away bonus from base
    if(len(valueString) <= 0):
        return False
    if(not 'x' in valueString):
        return False
    if(valueString.startswith('x')):
        valueString = valueString.strip('x')#cut 'x'
    if(valueString.startswith(('+', '(', ' '))):
        return False
    valueString = valueString.replace('+', '(')
    valueStringArray = valueString.split('(')
    base = valueStringArray[0]

    if(len(base) <= 0 or ' ' in base):
        return False

    return True

def truncate(f, n):
    #source: https://stackoverflow.com/questions/783897/truncating-floats-in-python
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def countMats(targetImg, matImgMap, charImgMap, params):
    offsetH, offsetW, baseH, baseW, LABEL, CHARSEARCH = params

    #Crop image to just include the mat window
    targetImg = targetImg[MAT_CROPY:MAT_CROPY + MAT_CROPH, MAT_CROPX:MAT_CROPX + MAT_CROPW]

    #search and mark target img for mat templates
    ptList = {}
    for matName in matImgMap.keys():
        matTemplate = matImgMap[matName]
        countMat(targetImg, matName, matTemplate, charImgMap, ptList)

    drops = []
    for pt in ptList.keys():
        matName = ptList[pt][0]
        nameArray = matName.split('.')
        matEntry = nameArray[0]
        # Note: For some reason round() didn't round so score is converted into a string to make testing easier.
        drop = {"item": matEntry, "x": pt[0], "y": pt[1], "score": truncate(ptList[pt][1], 8)}
        drops.append(drop)

        #TODO (red): need to investigate this for counting event currency
        if (CHARSEARCH and matName in eventMatList):
            # new mat on img
            col = pt[0]
            row = pt[1]
            # resizedImg = cv2.resize(targetImg, (0,0), fx=RESIZEY, fy=RESIZEX)
            matWindow = targetImg[row + offsetH:row + (offsetH + baseH), col + offsetW:col + (offsetW + baseW)]
            # matWindow = cv2.add(matWindow, np.array([30.0]))
            valueString = getCharactersFromImage(matWindow, charImgMap, imgName, matName, pt, CHAR_THRESHOLD, LABEL)
            # print "matEntry", matEntry, valueString, checkValueString(valueString)
            if (checkValueString(valueString)):
                matEntry = processValueString(valueString, matEntry)
                # logging.debug(matEntry)
            else:  # scan likely failed, retry with lower threshold
                valueString = getCharactersFromImage(matWindow, charImgMap, imgName, matName, pt, CHAR_THRESHOLD_LOOSE,
                                                     LABEL)
                matEntry = processValueString(valueString, matEntry)

    if len(drops) <= 0:
        logging.debug("No Mats Found.")
    else:
        logging.debug("Found mats:")
        for drop in drops:
           logging.debug(drop)

    return drops

def crop_black_edges(targetImg):
        # cut all black edges, credit https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
        grayImg = cv2.cvtColor(targetImg, cv2.COLOR_RGB2GRAY)
        if (LABEL):
            cv2.imwrite('gray.png', grayImg)
        _, thresh = cv2.threshold(grayImg, 1, 255, 0)
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width, channels = targetImg.shape
        min_x = width
        min_y = height
        max_x = 0
        max_y = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)

        targetImg = targetImg[min_y:max_x, min_x:max_x]
        if (LABEL):
            cv2.imwrite('cropped.png', targetImg)

        return targetImg

def get_qp_from_text(text):
    qp = 0
    power = 1
    # re matches left to right so reverse the list to process lower orders of magnitude first.
    for match in re.findall('[0-9]+', text)[::-1]:
        logging.debug(f"qp match: {match}")
        qp += int(match) * power
        power *= 1000

    return qp

def extract_qp_text_from_image(image):
    config = ('-l eng --oem 1 --psm 3')
    try:
        qp_gained_text, qp_total_text = pytesseract.image_to_string(image[433:433 + 104, 76:76 + 437], config=config).split('\n')
        return qp_gained_text, qp_total_text
    except ValueError:
        logging.fatal("Failed to extract qp text from image")
        raise

def get_qp(image):
    qp_gained_text, qp_total_text = extract_qp_text_from_image(image)
    logging.debug(f'QP gained text: {qp_gained_text}')
    logging.debug(f'QP total text: {qp_total_text}')
    qp_gained = get_qp_from_text(qp_gained_text)
    qp_total = get_qp_from_text(qp_total_text)

    if qp_total == 0:
        raise Exception("Failed to extract QP total from text returned by tesseract")

    return qp_gained, qp_total

def analyze_image(image_path, matImgMap, charImgMap, LABEL=False, CHARSEARCH=False):
    #make dictionary of mat templates
    totalMats = {}

    offsetH = OFFSET_HEIGHT
    offsetW = OFFSET_WIDTH
    baseH = BASE_HEIGHT
    baseW = BASE_WIDTH

    #read target image
    if(not os.path.isfile(image_path) or not isImage(image_path) or not os.path.exists(image_path)):
        line = "%s is not a valid img or path, skip." % image_path
        logging.debug(line)
        return

    targetImg = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if(targetImg is None):
        line = " %s is returns None from imread" % image_path
        logging.debug(line)
        return

    height, width, channels = targetImg.shape

    #check if image H W ratio is off
    ratio = 1.0 * width / height
    line = "ratio: ", ratio, 1.0 * TRAINING_IMG_WIDTH / TRAINING_IMG_HEIGHT
    logging.debug(line)

    if (abs(ratio - 1.0 * TRAINING_IMG_WIDTH / TRAINING_IMG_HEIGHT) > 0.25):
        targetImg = crop_black_edges(targetImg)

    # refresh channels
    height, width, channels = targetImg.shape

    #print height, width
    wscale = (1.0 * width) / TRAINING_IMG_WIDTH
    hscale = (1.0 * height) / TRAINING_IMG_HEIGHT
    scale = min(wscale, hscale)
    resizeScale = TRAINING_IMG_MAT_SCALE / scale

    if(resizeScale > 1):
        matImgResize = 1 / resizeScale
        line = "Too Small, resizing targetImg with ", matImgResize
        targetImg = cv2.resize(targetImg, (0,0), fx=resizeScale, fy=resizeScale)
        logging.debug(line)

    else:
        line = "Too big, resizing targetImage with ", resizeScale
        logging.debug(line)
        targetImg = cv2.resize(targetImg, (0,0), fx=resizeScale, fy=resizeScale)

    if(LABEL):
        cv2.imwrite('resized.png',targetImg)

    if(LABEL):
        cv2.imwrite('just_mats.png',targetImg)

    params = (offsetH, offsetW, baseH, baseW, LABEL, CHARSEARCH)
    mat_drops = countMats(targetImg, matImgMap, charImgMap, params)
    qp_gained, qp_total = get_qp(targetImg)
    return { "qp_gained": qp_gained, "qp_total": qp_total, "drops": mat_drops }

def setup_template_images():
    matImgMap = {}
    nodeMatFolderPath = os.path.join(REFFOLDER, MATFOLDER)
    matList = os.listdir(nodeMatFolderPath)
    for matName in matList:
        matpath = os.path.join(nodeMatFolderPath, matName)

        if not os.path.exists(matpath) or not isImage(matName):
            line = "%s is not a valid img/path, skip." % matpath
            raise Exception(f'{matpath} is not a valid path or is not an image.')

        mat_img = cv2.imread(matpath, cv2.IMREAD_COLOR)
        matImgMap[matName] = mat_img

    return matImgMap

def run(image, debug=False, label=False, nocharSearch=False):
    start = time.time()

    global LABEL
    global DEBUG
    LABEL = label
    DEBUG = debug

    logging.basicConfig(format='%(relativeCreated)6d %(threadName)s %(message)s', level=logging.DEBUG,
                filename='logfile.log',
                filemode='w')

    if debug:
        iolog = logging.StreamHandler()
        iolog.setLevel(logging.DEBUG)
        # tell the handler to use this format
        logging.getLogger('').addHandler(iolog)

    #read all mats
    matImgMap = setup_template_images()

    #make common character set
    charImgMap = {}
    charFolderPath = os.path.join(REFFOLDER, CHARFOLDER)
    charList = os.listdir(charFolderPath)
    for charName in charList:
        charpath = os.path.join(charFolderPath, charName)

        if(not isImage(charName) or not os.path.exists(charpath)):
            line = "%s is not a valid img/path, skip." % charpath
            logging.debug(line)
            continue

        char_img = cv2.imread(charpath, cv2.IMREAD_COLOR)
        charImgMap[charName] = char_img


    #get list of nodes to process
    print("Running...")
    results = analyze_image(image, matImgMap, charImgMap, label, nocharSearch)

    end = time.time()
    duration = end - start

    logging.info(f"Completed in {duration} seconds.")
    logging.info(f"Result:\n{results}")
    return results


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(
        description="Helper Script that uses basic image recognition via opencv to count mat drops in FGO Screenshots")
    parser.add_argument('-d', '--debug', action='store_true', help="Enables printing of debug messages")
    parser.add_argument('-l', '--label', action='store_true',
                        help="Used for debugging - makes debug images with identified characters in red boxes")
    parser.add_argument('-nc', '--nocharSearch', action='store_false',
                        help="Disable search and labeling for characters in images (improves performance outside events)")
    parser.add_argument('-i', '--image', help='Image to process')
    args = parser.parse_args()

    run(args.image, args.debug, args.label, args.nocharSearch)