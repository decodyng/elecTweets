from bs4 import BeautifulSoup
import urllib2
import pytesseract
from PIL import Image
import time
import os
import json
import random
import datetime
from pattern.web import URL
import re
import glob

def getTableInfo(state):
        print "Processing: " + str(state)
        fieldNames = ["TV Station", "Market", "Date", "Type", "Status", "Spots", "Cost", "AdvertiserInfo", "FileInfo"]
        baseURL = r"http://politicaladsleuth.com/political-files/state/" + state + r"/"
        stateList = []
        page_no = 1
        maxPages = 10
        while page_no < maxPages:
            print "Page number" + str(page_no)
            print page_no < maxPages
            pageURL = baseURL + r'/?page=' + str(page_no)
            request = urllib2.Request(pageURL)
            try:
                page = urllib2.urlopen(request)
            except urllib2.URLError, e:
                if hasattr(e, 'reason'):
                    print 'Failed to reach url'
                    print 'Reason: ', e.reason
                    break
                elif hasattr(e, 'code'):
                    if e.code == 404:
                        print 'Error', e.code
                        print "Looks like that's the end of the line!"
                        break
            content = page.read()
            soup = BeautifulSoup(content, "lxml")
            if page_no == 1:
                lastButton = soup.find("li", id="btnLast")
                lastA =lastButton.find("a")
                lasthref = lastA.get('href')
                maxPages = int(re.search(r'\d+', lasthref).group())
            table = soup.find('table', {'class':"table-striped"})
            rows = table.findAll('tr')
            if len(rows) == 0:
                break
            # Process each row in the table
            rowID = 0
            for tr in rows:
                cols = tr.findAll('td')
                rowDict ={}
                colID = 0
                for td in cols:
                    if colID < 7:
                        rowDict[fieldNames[colID]] = str(td.find(text=True)).strip()
                    else:
                        rowDict[fieldNames[colID]] = str(td.find(text=True)).strip()
                        colID += 1
                        anchor = td.find("a")
                        if anchor is not None:
                            rowDict[fieldNames[colID]] = anchor.get('href')
                        else:
                            rowDict[fieldNames[colID]] = "NO URL"
                    colID += 1
                #print rowDict
                if rowID != 0:
                    stateList.append(rowDict)
                rowID += 1

            page_no += 1 # update the page
             # Generate a random waiting time to avoid being detected and banned
            wait_time = round(max(0, 1 + random.gauss(0, 0.5)), 2)
            time.sleep(wait_time)
        return stateList



def writeToJSON(dict, fileName):

        outputFile = open(fileName, "w")
        jsonDict = json.dumps(dict, indent=4)
        print >> outputFile, jsonDict
        outputFile.close()

def findPDFLinks(dictList, state):
    compDate = datetime.date(2014, 1, 1)
    returnList = []
    print "Processing state: " + state
    count = 0
    for dict in dictList:
        print "Processing buy number " + str(count)
        dateStr = dict["Date"]
        buyDate = datetime.datetime.strptime(dateStr, "%m/%d/%y").date()

        if buyDate > compDate:
            adBuyURL= dict["FileInfo"]
            if adBuyURL == "NO URL":
                continue
            fullURL = r'http://politicaladsleuth.com/' +adBuyURL
            print "Quering " + fullURL
            request = urllib2.Request(fullURL)
            try:
                page = urllib2.urlopen(request)
            except urllib2.URLError, e:
                if hasattr(e, 'reason'):
                    print 'Failed to reach url'
                    print 'Reason: ', e.reason
                    continue
                elif hasattr(e, 'code'):
                    if e.code == 404:
                        print 'Error', e.code
                        continue
            content = page.read()
            soup = BeautifulSoup(content, "lxml")
            link = soup.find("a", href=True, text="Original Document")
            PDFLink = link.get("href")
            print "Found PDF link " + PDFLink
            dict["PDFLink"] = PDFLink
            returnList.append(dict)
            count += 1
            wait_time = round(max(0, 1 + random.gauss(0, 0.5)), 2)
            time.sleep(wait_time)
    outFileName = state + "_pdfDictList.json"
    writeToJSON(returnList, outFileName)
    return returnList
    #open link
    #Find link associated with "Original Document" or "the original file at the FCC"
    #add PDFLink value to dictionary

def downloadPDFs(dictListJSON, state, jsonExists = False):
    #state = dictListJSON[0, 2]
    dlJSONFile = open(dictListJSON, "r")
    dictJSON = json.load(dlJSONFile)
    dlJSONFile.close()
    #some condition to check if the JSON already exists
    if jsonExists:
        pdfDictList = dictJSON
    else:
        pdfDictList = findPDFLinks(dictJSON, state)


    count = 0
    for dict in pdfDictList:
        #test if date > 01/01/13
        fileName = "".join(str(dict["AdvertiserInfo"]).split())
        print "Writing to " + fileName
        url = dict["PDFLink"]
        url = re.sub(' ', '%20', url)
        print url
        if url != "NO URL":
            urlOpened = URL(url)
            f = open(fileName, 'wb')
            #download to state pdfs directory
            f.write(urlOpened.download(cached=False))
            f.close()
        count += 1
        if count > 4:
            break

def parsePDF(pdfFileName):
    filestem = pdfFileName.split(".")[0]
    print filestem
    txtFileName = filestem + ".txt"
    tiffFileName = filestem + ".tiff"
    if not glob.glob(tiffFileName):
        convertString = "convert '" + pdfFileName + "' '" + tiffFileName + "'"
        os.system(convertString)
    outputString = pytesseract.image_to_string(Image.open(tiffFileName))
    txtFile = open(txtFileName, "w")
    txtFile.write(outputString)
    txtFile.close()


if __name__ == "__main__":
    #downloadPDFs("MI_pdfDictList.json", "MI", True)
    files = [X for X in glob.glob("*.pdf")]
    for file in files:
        parsePDF(file)
#     stateListing = ["MI", "MN", "AK", "AR", "CO", "GA", "IA", "KS", "NH", "NC", "KY", "LA"]
#     rawDictAll = {}
#     numState = len(stateListing)
#
#
#     #for i in range(0, len(stateListing)):
#     for i in range(0, 1):
#         state = stateListing[i]
#         #rawDict = getTableInfo(state)
#         #rawDictAll[state] = rawDict
#         #fileName = state + "_AdSleuthRawInfo.json"
#         #writeToJSON(rawDict, fileName)
#         downloadPDFs(fileName, state)
#     #writeToJSON(rawDictAll, "allStatesAdSleuth.json")






