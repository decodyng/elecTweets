import json
import re
import numpy as np


#for json in list of candidateJSONs
#import json
#create new master output dict with keys = calendar days
#Go through dict and convert string date to date date and date time
#determine day of this entry
#add it to the new dict on the key of that day

def createOutputDict(candDict):
    outputDict = {}
    for entry in candDict:
        if entry == "distinctTweets":
            outputDict["totalDistinctTweets"] = candDict[entry]
        else:
            thisEntry = candDict[entry]
            thisStringDT = thisEntry["tweetTime"]
            thisDayMonth = re.search(r'[A-Z][a-z][a-z] \d\d', thisStringDT).group()
            thisDateString = thisDayMonth + " 2014"
            thisTime = re.search(r'\d\d:\d\d:\d\d', thisStringDT).group()
            thisFullDT = thisDateString + " " + thisTime



            thisEntry["date"] = thisDateString
            thisEntry["dt"] = thisFullDT

            if thisEntry["date"] not in outputDict:
                outputDict[thisEntry["date"]] = {}
                outputDict[thisEntry["date"]]['numTweets'] = 0
            outputDict[thisEntry["date"]][thisEntry["tweetID"]] = thisEntry
            outputDict[thisEntry["date"]]['numTweets'] += 1

    return outputDict

def getCandidateAverage(fileName):
    candJSONFile = open(fileName, "r")
    candJSON = json.load(candJSONFile)
    candJSONFile.close()
    dailyAmounts = []

    for topKey in candJSON:
        if topKey != "totalDistinctTweets":
            ##check for partial days
            mon = topKey[0:4]
            print mon
            day = topKey[4:6]
            print day
            yr = topKey[6:]
            print yr
            priorDay = str(int(day) - 1)
            postDay = str(int(day) +1)
            priorDate = mon + priorDay + yr
            postDate  = mon + postDay + yr
            print topKey
            print priorDate
            print postDate
            if priorDate in candJSON and postDate in candJSON:
                amnt = candJSON[topKey]["numTweets"]
                dailyAmounts.append(amnt)
    return np.mean(dailyAmounts)

def getAggregateText(candDict):
    allTxt = ""
    for keyID in candDict:
        if keyID != "distinctTweets":
            allTxt = allTxt + " " + candDict[keyID]["tweetString"].encode("ascii", 'ignore')
    return allTxt
if __name__ == "__main__":
    candidateList = {"Gary Peters":"MI", "Terri Lynn Land":"MI","Al Franken":"MN","Mike McFadden":"MN",
                         "Mark Begich":"AK","Dan Sullivan":"AK","Mark Pryor":"AR","Tom Cotton":"AR","Mark Udall":"CO",
                         "Cory Gardner":"CO","David Perdue":"GA","Michelle Nunn":"GA","Bruce Braley":"IA",
                         "Joni Ernst":"IA","Pat Roberts":"KS","Greg Orman":"KS","Jeanne Shaheen":"NH",
                        "Scott Brown":"NH","Kay Hagan":"NC","Thom Tillis":"NC","Mitch McConnell":"KY",
                        "Alison Grimes":"KY","Mary Landrieu":"LA","Bill Cassidy":"LA","Rob Maness": "LA"}
    candidateAverages = {}
    for candidate in candidateList:
        fileNameStem = "".join(candidate.split())
        fileName = fileNameStem + ".json"
        candJSONFile = open(fileName, "r")
        candJSON = json.load(candJSONFile)
        candJSONFile.close()
        # outputCandDict = createOutputDict(candJSON)

        #outputFileName = fileNameStem + "DT" + ".json"
        # outputFile = open(outputFileName, "w")
        # outputJSON = json.dumps(outputCandDict, indent=4)
        # print >> outputFile, outputJSON
        #outputFile.close()
        #candidateAverage = getCandidateAverage(outputFileName)
        #candidateAverages[candidate] = candidateAverage

        #averageFile = open("averageTweetsByCandidate.json", "w")
        #outputAverages = json.dumps(candidateAverages)
        #print >> averageFile, outputAverages
        #averageFile.close()

        aggregateText = getAggregateText(candJSON)
        candTextName = fileNameStem + "Text.txt"
        candTextFile = open(candTextName, "w")
        candTextFile.write(aggregateText)
        candTextFile.close()

