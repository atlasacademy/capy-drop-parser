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
import json
import pathlib

LABEL = False
DEBUG = False

TRAINING_IMG_HEIGHT = 1080
TRAINING_IMG_WIDTH = 1920
TRAINING_IMG_ASPECT_RATIO = float(TRAINING_IMG_WIDTH) / TRAINING_IMG_HEIGHT
TRAINING_IMG_MAT_SCALE = 0.54
MIN_DISTANCE = 50
DIGIT_MIN_DISTANCE = 9
THRESHOLD = .82
CHAR_THRESHOLD = .65
CHAR_THRESHOLD_LOOSE = .59

REFFOLDER = pathlib.Path(__file__).parent / 'ref'

OFFSET_HEIGHT = 75
OFFSET_WIDTH = 13
BASE_HEIGHT = 22
BASE_WIDTH = 80

def getOverlap(pt, ptList, distance=MIN_DISTANCE):
    row = pt[1]
    col = pt[0]
    for prevPt in ptList.keys():
        prevRow = prevPt[1]
        prevCol = prevPt[0]
        if abs(prevRow - row) < distance and abs(prevCol - col) < distance:
            return prevPt
    return None

def getCharTagValue(char):
    array = char.split("_")
    valueChar = array[1]
    return valueChar

def countMat(targetImg, template, ptList):
    res = cv2.matchTemplate(targetImg, template['image'], cv2.TM_CCOEFF_NORMED)
    loc = np.asarray(res >= THRESHOLD).nonzero()

    # Reverse rows and columns of the matrix so that coordinates are relative to (0,0) [column, row] being the upper left of the image
    # instead of the traditional indexing of a multidimensional array [row, column].
    # This means that when indexing back into the res array the indexes will need to be swapped agian.
    for pt in zip(*loc[::-1]):
        score = res[pt[1]][pt[0]]
        overLapPt = getOverlap(pt, ptList)
        if overLapPt is None:
            ptList[pt] = (template['id'], score)
        else:
            oldScore = ptList[overLapPt][1]
            if score > oldScore:
                ptList[overLapPt] = (template['id'], score)


def getCharactersFromImage(matWindow, templates, threshold, x, y, pos):
    charPtList = {}

    resultsImg = None

    if LABEL:
        resultsImg = matWindow.copy()

    for char in templates:
        charTemplate = char['image']
        charValue = getCharTagValue(char['id'])
        w, h = charTemplate.shape[:-1]

        charRes = cv2.matchTemplate(matWindow, charTemplate, cv2.TM_CCOEFF_NORMED)
        charLoc = np.where(charRes >= threshold)

        for cpt in zip(*charLoc[::-1]):  # Switch collumns and rows
            charScore = charRes[cpt[1]][cpt[0]]
            overlapCharPt = getOverlap(cpt, charPtList, DIGIT_MIN_DISTANCE)
            if overlapCharPt is None:
                charPtList[cpt] = (charValue, charScore)
            else:
                oldCharScore = charPtList[overlapCharPt][1]
                if charScore > oldCharScore:
                    charPtList[overlapCharPt] = (charValue, charScore)
                    #print "old -> new: %s -> %s @ %s [ %f vs %f ] " % (oldCharName, charValue, cpt, oldCharScore, charScore)

    if LABEL:
        for cpt in charPtList.keys():
            cv2.rectangle(resultsImg, cpt, (cpt[0] + h, cpt[1] + w), (0, 0, 255), 1)
        #cv2.imwrite(f'current_character_window_{y}_{x}_{pos}.png', resultsImg)
        cv2.imwrite(f'current_character_window.png', resultsImg)

    #finished evaluating characters, construct number representation of mats
    charValPositionList = []
    for cpt in charPtList.keys():
        (charValue, charScore)  = charPtList[cpt]
        ccol = cpt[0]
        charValPositionList.append((ccol, charValue))

    # sort each character img by its relative col position in the img
    charValPositionList = sorted(charValPositionList, key = lambda x: x[0])
    valueString = ""
    prevccol = -1
    for charValue  in charValPositionList:
        if prevccol >= 0 and ccol - prevccol > DIGIT_MIN_DISTANCE:
            valueString += ' '
        valueString += charValue[1]
    return valueString

def get_stack_base(valueString):
    matches = re.search('(x|\+)([0-9]+)', valueString)
    if matches is None or matches.group(2) is None:
        raise Exception('Failed to find base stack size')

    return int(matches.group(2))

def checkValueString(valueString):
    try:
        get_stack_base(valueString)
        return True
    except:
        return False

def get_stack_base_top(valueString):
    matches = re.search('(x|\+)([0-9]+)', valueString)
    if matches is None or matches.group(2) is None:
        raise Exception('Failed to find base stack size')

    return int(matches.group(2))

def checkValueStringTop(valueString):
    try:
        get_stack_base_top(valueString)
        return True
    except:
        return False

def get_stack_sizes(image, mat_drops, templates):
    currencies = [template for template in templates if template["type"] == "currency"]
    character_templates = [template for template in templates if template["type"] == "character"]
    for drop in mat_drops:
        drop['stack'] = 0
        for currency in currencies:
            if drop['id'] == currency['id']:
                top_line = image[drop['y']+40:drop['y']+69, drop['x']+7:drop['x']+88]
                drop_identifier = f"{drop['y']:3d}_{drop['x']:3d}"

                top_stack_size_string = getCharactersFromImage(top_line, character_templates, CHAR_THRESHOLD, drop['x'], drop['y'], "atop")
                logging.debug(f"{drop_identifier} | 1st try top   : {top_stack_size_string}")

                if not checkValueStringTop(top_stack_size_string):
                    top_stack_size_string = getCharactersFromImage(top_line, character_templates, CHAR_THRESHOLD_LOOSE, drop['x'], drop['y'], "atop")
                    logging.debug(f"{drop_identifier} | 2nd try top   : {top_stack_size_string}")

                if checkValueStringTop(top_stack_size_string):
                    drop['stack'] = get_stack_base_top(top_stack_size_string)
                    logging.debug(f"{drop_identifier} | Top    string : {drop['stack']}")
                else:
                    logging.error(f'{drop_identifier} | Failed to get top stack count')
                    bottom_line = image[drop['y']+61:drop['y']+89, drop['x']+7:drop['x']+95]

                    stack_size_string = getCharactersFromImage(bottom_line, character_templates, CHAR_THRESHOLD, drop['x'], drop['y'], "bottom")
                    logging.debug(f"{drop_identifier} | 1st try bottom: {stack_size_string}")

                    if not checkValueString(stack_size_string):
                        stack_size_string = getCharactersFromImage(bottom_line, character_templates, CHAR_THRESHOLD_LOOSE, drop['x'], drop['y'], "bottom")
                        logging.debug(f"{drop_identifier} | 2nd try bottom: {stack_size_string}")

                    if checkValueString(stack_size_string):
                        drop['stack'] = get_stack_base(stack_size_string)
                        logging.debug(f"{drop_identifier} | Bottom string : {drop['stack']}")
                    else:
                        logging.error(f'{drop_identifier} | Failed to get bottom stack count')
                        drop['stack'] = -1



def countMats(targetImg, templates):
    #Crop image to just include the mat window
    targetImg = targetImg[80:80 + 360, 115:115 + 810]
    if LABEL:
        cv2.imwrite('just_mats.png', targetImg)

    #search and mark target img for mat templates
    ptList = {}
    for mat in [template for template in templates if template["type"] == "material" or template["type"] == "currency"]:
        countMat(targetImg, mat, ptList)

    drops = []
    for pt in ptList.keys():
        matName = ptList[pt][0]
        drop = {"id": matName, "x": pt[0], "y": pt[1], "score": ptList[pt][1]}
        drops.append(drop)

    if len(drops) <= 0:
        logging.debug("No Mats Found.")
    else:
        logging.debug("Found mats:")
        for drop in drops:
           logging.debug(drop)

    # Detecting stack size is called here because cropping to just the stack size text based on the mat location needs
    # needs to be done with the cropped version of the image the mats were detected in for the location to remain
    # accurate.
    get_stack_sizes(targetImg, drops, templates)

    return drops

def crop_top_bottom_blue_borders(image):
    height, width, _ = image.shape
    new_height = width / TRAINING_IMG_ASPECT_RATIO
    adjustment = int((height - new_height) / 2)

    image = image[adjustment:height - adjustment, 0:width]
    if LABEL:
        cv2.imwrite('post_1.3_ratio_crop.png', image)

    return image

def crop_side_and_bottom_blue_borders(image):
    height, width, _ = image.shape
    image = image[0:height - 60, 275:width - 275]
    if LABEL:
        cv2.imwrite('post_2.1_ratio_crop.png', image)

    return image

def crop_black_edges(targetImg):
        # cut all black edges, credit https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
        grayImg = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY)
        if LABEL:
            cv2.imwrite('gray.png', grayImg)

        _, thresh = cv2.threshold(grayImg, 70, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height, width, _ = targetImg.shape
        min_x = width
        min_y = height
        max_x = 0
        max_y = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)

        targetImg = targetImg[min_y:max_y, min_x:max_x]
        if LABEL:
            cv2.imwrite('post_black_crop.png', targetImg)

        return targetImg

def get_qp_from_text(text):
    qp = 0
    power = 1
    # re matches left to right so reverse the list to process lower orders of magnitude first.
    for match in re.findall('[0-9]+', text)[::-1]:
        logging.debug(f"QP match: {match}")
        qp += int(match) * power
        power *= 1000

    return qp

def extract_text_from_image(image, file_name='pytesseract_input.png'):
    gray =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, qp_image = cv2.threshold(gray, 65, 255, cv2.THRESH_BINARY_INV)

    if LABEL:
        cv2.imwrite(file_name, qp_image)

    return pytesseract.image_to_string(qp_image, config='-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=,0123456789')

def get_qp(image):
    qp_gained_text = extract_text_from_image(image[435:430 + 47, 348:348 + 311], 'qp_gained_text.png')
    logging.debug(f'QP gained text: {qp_gained_text}')
    qp_total_text = extract_text_from_image(image[481:481 + 38, 212:212 + 282], 'qp_total_text.png')
    logging.debug(f'QP total text: {qp_total_text}')
    qp_gained = get_qp_from_text(qp_gained_text)
    qp_total = get_qp_from_text(qp_total_text)

    if qp_total == 0:
        raise Exception("Failed to extract QP total from text returned by tesseract")

    return qp_gained, qp_total


def get_scroll_bar_start_height(image):
    height, width, _ = image.shape
    upper_left_x = width - 117
    gray_image = cv2.cvtColor(image[90:90 + 330, upper_left_x:upper_left_x + 30], cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_image, 225, 255, cv2.THRESH_BINARY)
    if LABEL: cv2.imwrite('scroll_bar_binary.png', binary)
    _, template = cv2.threshold(cv2.imread(os.path.join(REFFOLDER, 'scroll_bar_upper.png'), cv2.IMREAD_GRAYSCALE), 225, 255, cv2.THRESH_BINARY)
    res = cv2.matchTemplate(binary, template, cv2.TM_CCOEFF_NORMED)
    _, maxValue, _, max_loc = cv2.minMaxLoc(res)
    return max_loc[1] if maxValue > 0.5 else -1


def get_aspect_ratio(image):
    height, width, _ = image.shape
    return float(width) / height

def get_drop_count(image):
    try:
        text = extract_text_from_image(image[0:0 + 35, 806:806 + 40], 'drop_count_text.png')
        logging.debug(f'Drop count text: {text}')
        return int(re.search("([0-9]+)", text).group(1))
    except:
        return -1

def analyze_image(image_path, templates, LABEL=False):
    if not os.path.isfile(image_path):
        raise Exception(f'{image_path} does not exist')

    targetImg = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if targetImg is None:
        raise Exception(f'{image_path} returned None from imread')

    #check if image H W ratio is off
    aspect_ratio = get_aspect_ratio(targetImg)
    logging.debug(f'Input aspect ratio is {aspect_ratio:.4f}, training ratio is {TRAINING_IMG_ASPECT_RATIO:.4f}')
    if abs(aspect_ratio - TRAINING_IMG_ASPECT_RATIO) > 0.1:
        targetImg = crop_black_edges(targetImg)

    # Aspect ratio of 1.3 causes FGO to add blue borders on the top and bottom
    if abs(1.3 - get_aspect_ratio(targetImg)) < 0.1:
        targetImg = crop_top_bottom_blue_borders(targetImg)

    # Aspect ratio of 2.165 causes FGO to add blue borders to both sides and the bottom; at least on some devices.
    if abs(2.165 - get_aspect_ratio(targetImg)) < 0.1:
        targetImg = crop_side_and_bottom_blue_borders(targetImg)

    # refresh channels
    height, width, channels = targetImg.shape

    #print height, width
    wscale = (1.0 * width) / TRAINING_IMG_WIDTH
    hscale = (1.0 * height) / TRAINING_IMG_HEIGHT
    scale = min(wscale, hscale)
    resizeScale = TRAINING_IMG_MAT_SCALE / scale

    if resizeScale > 1:
        matImgResize = 1 / resizeScale
        line = f"Too small, resizing targetImage with {matImgResize:.2f}"
        targetImg = cv2.resize(targetImg, (0,0), fx=resizeScale, fy=resizeScale, interpolation=cv2.INTER_CUBIC)
        logging.debug(line)

    else:
        line = f"Too big, resizing targetImage with {resizeScale:.2f}"
        logging.debug(line)
        targetImg = cv2.resize(targetImg, (0,0), fx=resizeScale, fy=resizeScale, interpolation=cv2.INTER_AREA)

    if LABEL:
        cv2.imwrite('resized.png',targetImg)

    mat_drops = countMats(targetImg, templates)
    qp_gained, qp_total = get_qp(targetImg)
    scroll_position = get_scroll_bar_start_height(targetImg)
    drop_count = get_drop_count(targetImg)
    return { "qp_gained": qp_gained, "qp_total": qp_total, 'scroll_position': scroll_position, "drop_count": drop_count, "drops_found": len(mat_drops), "drops": mat_drops }

def load_image(image_path):
    if not os.path.isfile(image_path):
        raise Exception(f'Path is not a file: {image_path}')

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise Exception(f'Failed to load file as image: {image_path}')

    return image

def load_template_images(settings, template_dir):
    for template in settings:
        template['image'] = load_image(os.path.join(template_dir, template['id']))

    return settings

def analyze_image_for_discord(image_path, settings, template_dir):
    try:
        settings = load_template_images(settings, template_dir)
        with open(REFFOLDER / 'characters.json') as fp:
            characters = json.load(fp)
            characters = load_template_images(characters, REFFOLDER)
            settings.extend(characters)
        result = analyze_image(image_path, settings)
        result['matched'] = True
    except Exception as e:
        result = { 'matched': False, 'exception': e }

    result['image_path'] = str(image_path)
    return result

def run(image, debug=False, label=False):
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

    base_settings = os.path.join(REFFOLDER, "settings.json")
    base_img_dir_image = os.path.dirname(image)
    custom_settings = os.path.join(base_img_dir_image, "settings.json")
    custom_ref = os.path.join(base_img_dir_image, "files")
    
    if os.path.exists(custom_settings):
        chosen_setting, chosen_ref = custom_settings, custom_ref
    else:
        chosen_setting, chosen_ref = base_settings, REFFOLDER
    
    with open(chosen_setting) as fp:
        settings = json.load(fp)
    settings = load_template_images(settings, chosen_ref)
        
    with open(REFFOLDER / 'characters.json') as fp:
        characters = json.load(fp)
        characters = load_template_images(characters, REFFOLDER)
        settings.extend(characters)


    logging.info("Running...")
    results = analyze_image(image, settings, label)

    end = time.time()
    duration = end - start

    logging.info(f"Completed in {duration:.2f} seconds.")
    logging.info(f"Result:\n{results}")
    return results


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(
        description="Helper Script that uses basic image recognition via opencv to count mat drops in FGO Screenshots")
    parser.add_argument('-d', '--debug', action='store_true', help="Enables printing of debug messages")
    parser.add_argument('-l', '--label', action='store_true',
                        help="Used for debugging - makes debug images with identified characters in red boxes")
    parser.add_argument('-nc', '--nocharSearch', action='store_true', default=False,
                        help="Disable search and labeling for characters in images (improves performance outside events)")
    parser.add_argument('-i', '--image', help='Image to process')
    args = parser.parse_args()

    results = run(args.image, args.debug, args.label)
    print(results)
    # with open(REFFOLDER / 'settings.json') as fp:
    #     settings = json.load(fp)
    # settings = load_template_images(settings, REFFOLDER)
    # for template in settings:
    #     if template['type'] == 'currency' or template['type'] == 'material':
    #         h, w, _ = template['image'].shape
    #         cv2.imwrite(str((REFFOLDER / f'{template["id"]}')), template['image'][15:h, 0:w])
