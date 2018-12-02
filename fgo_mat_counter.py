#################################################################################
##  FGO Materials Parser/Calculator v0.191 ALPHA by Yhsa (4/8/2018)
##  Basic OpenCV Script to count and collate mat icons inside fgo screenshots
##  Free for distribution and use, please give credit where due
##  Thanks to: Officer Artoria, Yuki, Sigma, Snow and the folks of FGO Farmville for their help
#################################################################################


import cv2
import scipy
import numpy as np
import os
import time
import datetime
#import multiprocessing
import argparse
import logging
import xlrd
from progress.bar import Bar


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

CROPX = 115
CROPY = 100
CROPW = 800
CROPH = 335

DEBUG = False



def getOverlap(pt, ptList, distance=MIN_DISTANCE):
    row = pt[0]
    col = pt[1]
    for prevPt in ptList.keys():
        prevRow = prevPt[0]
        prevCol = prevPt[1]
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
     
def countMat(targetImg, targetpath, imgName, matName, matTemplate, charImgMap, ptList):
    #resultsImg = targetImg.copy() 

    w, h = matTemplate.shape[:-1]
    res = cv2.matchTemplate(targetImg, matTemplate, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
            
    #if(lock != None):
    #    lock.acquire()
    for pt in zip(*loc[::-1]):  # Switch collumns and rows          
        score = res[pt[1]][pt[0]] 
        overLapPt = getOverlap(pt, ptList)
        if(overLapPt == None):
            ptList[pt] = (matName, score)                
            #lower_y = np.array([0,60,150])
            #upper_y = np.array([100,255,255])
            #mask = (cv2.inRange(matWindow, lower_y, upper_y))
            #matWindow.setTo(Scalar(255,255,255), mask)
            #matWindow = cv2.bitwise_or(matWindow, matWindow, mask = mask)
            #matWindow[np.where(mask == [0,0,0])] = [0,0,0]
            #matWindow[np.where((matWindow>=[130,130,130]).all(axis=2))] = [255,255,255]
            #matWindow[np.where((matWindow<=[20,255,255]).all(axis=2))] = [255,255,255]
            #matWindow[np.where((matWindow>=[0,150,150]).all(axis=2))] = [255,255,255]
            #matWindow.Set(mask,cv2.Scalar(0,0,0))
            
            #matWindowGray = cv2.cvtColor( matWindow, cv2.COLOR_RGB2GRAY )
            #clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(14,10))
            #matWindowGray = clahe.apply(matWindowGray)
            #matWindowGray = cv2.bitwise_not(matWindowGray)
            #cv2.floodFill(matWindowGray, None, (0,0),255)
            
            #(thresh, matWindowBW) = cv2.threshold(matWindowGray, 126, 255, cv2.THRESH_BINARY)
            
            #pathname = "%s_%d_%d.png" % (imgName, col, row)
            #matWindowpathname = "%s_matWindow_%d_%d.png" % (imgName, col, row)
            #maskpathname = "%s_mask_%d_%d.png" % (imgName, col, row)
            #print pathname
            #cv2.imwrite(matWindowpathname, matWindowGray)
            #cv2.imwrite(pathname, matWindowBW)
            #text = pytesseract.image_to_string(matWindow,  config='-c tessedit_char_whitelist=()+x1234567890 davinci')
            #print text.encode('utf-8')
    
        else:
            oldScore = ptList[overLapPt][1]
            oldMatName = ptList[overLapPt][0]
            #print "          score: %s oldScore: %s" % (score, oldScore) 
            if(score > oldScore):
                ptList[overLapPt] = (matName, score)
                #print "          matName: %s score: %s ;; oldMatName: %s oldScore: %s" % (matName, score, oldMatName, oldScore) 
    #print "Finished countmat on ", matName
    #if(lock != None):
    #    lock.release()
        
    
        
        
    #resultsName = "%s_%s_results.png" % (imgName, matName)
    #cv2.imwrite(resultsName, resultsImg)

def countMatWrapper(args):
    countMat(*args)
    
def init_lock(l):
    global lock
    lock = l
    
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
    
def countMats(targetImg, imgName, targetpath, matImgMap, charImgMap, nodeDrops, params):

    offsetH, offsetW, baseH, baseW, LABEL, CHARSEARCH = params

    #search and mark target img for mat templates
    #ptList = multiprocessing.Manager().dict()
    #resultsImg = targetImg.copy() #remove after testing
    ptList = {}    
    #lock = multiprocessing.Lock()
    args = []
    #numCores = multiprocessing.cpu_count()
    #numPools = max(1, numCores - 1)
    #p = multiprocessing.Pool(numPools, initializer=init_lock, initargs=(lock,))
    
    #for matName in matImgMap.keys():
    #    if(matName in nodeDrops):            
    #        line = "    Checking for Mat: ", matName
    #        logging.debug(line)
    #        matTemplate = matImgMap[matName]
    #        args.append((targetImg, targetpath, imgName, matName, matTemplate, charImgMap, ptList))
    #p.map(countMatWrapper ,args)
    
    eventMatList = []
    for matName in matImgMap.keys():
        if(matName in nodeDrops):    
            matTemplate = matImgMap[matName]
            countMat(targetImg, targetpath, imgName, matName, matTemplate, charImgMap, ptList)  
        elif("{0}{1}".format("*", matName) in nodeDrops):
            matTemplate = matImgMap[matName]
            countMat(targetImg, targetpath, imgName, matName, matTemplate, charImgMap, ptList)  
            eventMatList.append(matName)
    
    matCount = {}
    #iterate over each found mat in that node
    valueString = ""
    matEntry = ""
    nameArray = []
    matName = ""
    
    for pt in ptList.keys():   
        #format output for spreadsheet
        matName = ptList[pt][0]
        nameArray = matName.split('.')
        matEntry = nameArray[0]   
        
        if(CHARSEARCH and matName in eventMatList):
            #new mat on img
            col = pt[0] 
            row = pt[1] 
            #resizedImg = cv2.resize(targetImg, (0,0), fx=RESIZEY, fy=RESIZEX)
            matWindow = targetImg[row+offsetH:row+(offsetH+baseH), col+offsetW:col+(offsetW+baseW)]
            #matWindow = cv2.add(matWindow, np.array([30.0]))
            valueString = getCharactersFromImage(matWindow, charImgMap, imgName, matName, pt, CHAR_THRESHOLD, LABEL)            
            #print "matEntry", matEntry, valueString, checkValueString(valueString)
            if(checkValueString(valueString)):
                matEntry = processValueString(valueString, matEntry)
                #logging.debug(matEntry)      
            else: #scan likely failed, retry with lower threshold
                valueString = getCharactersFromImage(matWindow, charImgMap, imgName, matName, pt, CHAR_THRESHOLD_LOOSE, LABEL)   
                matEntry = processValueString(valueString, matEntry) 
            

        if(matEntry not in matCount.keys()):
            matCount[matEntry] = 0
        matCount[matEntry] += 1   
        
    line = "Printing all Mats Found for %s..." % imgName 
    logging.debug(line)    
    
    if(len(matCount.keys()) <= 0):
        line =  "    > No Mats Found."        
        logging.debug(line)
    else:
        for matName in matCount.keys():     
            count = matCount[matName]
            if(count > 0):
                line = "    > %s: %d" % (matName, count)
                logging.debug(line)   
    
    
    return matCount
    #path = os.path.join(RESULTSFOLDER, imgName)
    #cv2.imwrite(path, resultsImg)

def updateTotalMats(totalMats, newMats):
    for mat in newMats.keys():
        if(mat not in totalMats.keys()):
            totalMats[mat] = 0
        totalMats[mat] += newMats[mat]
    
def analyze_folder(nodeName, nodePath, matImgMap, charImgMap, dropMap, LABEL=False, CHARSEARCH=False):
    #make dictionary of mat templates
    #start = time.time()
    
    targetList = os.listdir(nodePath)
    totalMats = {}
    runs = 0
    
    if len(targetList) <= 0:
        print "      No Screenshots Found."
        return totalMats, runs
    
    bar = Bar('   Processing', max=len(targetList), suffix='%(percent)d%%')    
    
    targetImg = None
    grayImg = None
    matCount = None
    
    offsetH = OFFSET_HEIGHT
    offsetW = OFFSET_WIDTH
    baseH = BASE_HEIGHT
    baseW = BASE_WIDTH
        
    for targetName in targetList:
    
        
        #read target image  
        targetpath = os.path.join(nodePath, targetName)
        if(not os.path.isfile(targetpath) or not isImage(targetName) or not os.path.exists(targetpath)):
            line = "%s is not a valid img or path, skip." % targetpath
            logging.debug(line)
            bar.next()
            continue
        
        targetImg = cv2.imread(targetpath, cv2.IMREAD_COLOR)
        runs += 1 
        
        #print targetImg.shape 
        if(targetImg is None):
            line = " %s is returns None from imread" % targetName
            logging.debug(line)
            continue
        height, width, channels = targetImg.shape         
        
        #check if image H W ratio is off
        ratio = 1.0 * width / height
        line = "ratio: ", ratio, 1.0 * TRAINING_IMG_WIDTH / TRAINING_IMG_HEIGHT        
        logging.debug(line)            
        
        if(abs(ratio - 1.0 * TRAINING_IMG_WIDTH / TRAINING_IMG_HEIGHT) > 0.25):
            #cut all black edges, credit https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
            grayImg = cv2.cvtColor(targetImg,cv2.COLOR_RGB2GRAY)
            if(LABEL):
                cv2.imwrite('gray.png',grayImg)
            _,thresh = cv2.threshold(grayImg,1,255,0)
            _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(targetImg, contours, -1, (0,255,0), 3)
                
            min_x = width
            min_y = height
            max_x = 0
            max_y = 0
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                min_x, max_x = min(x, min_x), max(x+w, max_x)
                min_y, max_y = min(y, min_y), max(y+h, max_y)
                
            targetImg = targetImg[min_y:max_x,min_x:max_x]
            if(LABEL):
                cv2.imwrite('cropped.png',targetImg)
            
            #refresh channels
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
            
        #crop to just mat location        
        targetImg = targetImg[CROPY:CROPY+CROPH,CROPX:CROPX+CROPW]
        
        if(LABEL):
            cv2.imwrite('just_mats.png',targetImg)
            
            
            
            
        params = (offsetH, offsetW, baseH, baseW, LABEL, CHARSEARCH)    
        nodeDrops = dropMap[nodeName]

        matCount = countMats(targetImg, targetName, targetpath, matImgMap, charImgMap, nodeDrops, params)
        updateTotalMats(totalMats, matCount)
        bar.next()
    #end = time.time()
    #print "Analyzed %d runs in ---- %s seconds -----" % (runs, end - start)
    print
    return totalMats, runs

def make_spreadsheet(nodeMap):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M")
    name = "FGO_Drops_"+timestamp+".csv"
    #name = "FGO_Dropsheet.csv"#no timestamp for now
    path = os.path.join(RESULTSFOLDER, name)
    
    f = open(path, "w")

    line = "sep=:\n"
    f.write(line)
        
    for node in nodeMap.keys():
        countMats, runs = nodeMap[node]
        
        line = "%s: %d run(s)\n" % (node, runs)
        f.write(line)
        
        for mat in countMats.keys():
            line = "    %s: %d\n" % (mat, countMats[mat])
            f.write(line)
            
        line = "\n"
        f.write(line)        
    f.close()
    
    return name
    
def update_spreadsheet(nodeMap): #incomplete function, need OfficerA's input
    mats = nodeMap.keys()
    sheetPath = os.path.join(RESULTSFOLDER, SUBMISSION_SHEET)
    dropsheet = xlrd.open_workbook(sheetPath)
    xl_sheet = dropsheet.sheet_by_name("Submissions")
    matsCol = xl_sheet.row(0)
                
    
def run():
    print "Fate/GrandOrder (NA) Screenshot Drops Parser - version 0.191 ALPHA"
    print
    print "THIS IS AN ALPHA RELEASE OF THE PROGRAM - MANY FEATURES ARE STILL INCONSISTENT OR NOT IMPLEMENTED"
    print "IF YOU FIND ANY BUGS (OR HAVE SOME FEEDBACK) PLEASE CONTACT YHSA AT yhsaweyland@gmail.com"
    print
    
    start = time.time()
    
    parser = argparse.ArgumentParser(description="Helper Script that uses basic image recognition via opencv to count mat drops in FGO Screenshots")
    parser.add_argument('-d', '--debug', action='store_true' , help="Enables printing of debug messages")
    parser.add_argument('-l', '--label', action='store_true' , help="Used for debugging - makes debug images with identified characters in red boxes")
    parser.add_argument('-nc', '--nocharSearch', action='store_false' , help="Disable search and labeling for characters in images (improves performance outside events)")
    args = parser.parse_args()
    
    DEBUG = args.debug,
    logging.basicConfig(format='%(relativeCreated)6d %(threadName)s %(message)s', level=logging.DEBUG,
                filename='logfile.log',
                filemode='w')
    if args.debug:
        iolog = logging.StreamHandler()
        iolog.setLevel(logging.DEBUG)
        # tell the handler to use this format
        logging.getLogger('').addHandler(iolog)
    
    #read all mats
    matImgMap = {}
    nodeMatFolderPath = os.path.join(REFFOLDER, MATFOLDER)
    matList = os.listdir(nodeMatFolderPath)
    for matName in matList:
        matpath = os.path.join(nodeMatFolderPath, matName)
        
        if(not isImage(matName) or not os.path.exists(matpath)):
            line = "%s is not a valid img/path, skip." % matpath
            logging.debug(line)
            continue
            
        mat_img = cv2.imread(matpath, cv2.IMREAD_COLOR)
        matImgMap[matName] = mat_img
        
    #read drop map
    dropMap = {}
    dropMapPath = os.path.join(REFFOLDER, DROPMAP)
    dropMapFile = open(dropMapPath, 'r')
    for line in dropMapFile:
        line = line.strip()
        nodeArray = line.split(":")
        node = nodeArray[0].strip()
        rawDropArray = nodeArray[1].strip().split(",")
        dropList = []
        for drop in rawDropArray:
            drop = drop.strip()
            drop = "{0}.png".format(drop) 
            dropList.append(drop)
            
        dropMap[node] = dropList
            
    dropMapFile.close()
    
    
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
    print "Running..."
    nodeList = os.listdir(TARGETFOLDER)
    nodeMap = {}
    for node in nodeList:
        nodePath = os.path.join(TARGETFOLDER, node)
        if(os.path.isdir(nodePath)):
            print "    > Analyzing screenshots for %s..." % node
            logging.debug("")
            #PROCESS!
            results = analyze_folder(node, nodePath, matImgMap, charImgMap, dropMap, args.label, args.nocharSearch)
            nodeMap[node] = results
            #print "done!"
    print 
    end = time.time()
    duration = end - start
    
    print "All nodes completed in %f seconds. Creating csv text file of mat drops..." % duration, 
    logging.debug("")
    sheetname = make_spreadsheet(nodeMap)
    #update_spreadsheet(nodeMap)  ##todo
    
    print "done!"
    print 
    print "CSV file %s created" % sheetname
    print 
    print "Thank you for valuable input! Have a nice day!"

            
if __name__ ==  '__main__':
    #multiprocessing.freeze_support()
    run()