import re
import pprint

def createCandidateDict(candName, state):
    compressedName = "".join(candName.split())
    idDict = {}
    fileName = compressedName + ".txt"
    readFile = open(fileName, "r")
    count = 0

    for line in readFile:
        print count
        line = re.sub(r'\n', "", line)
        if line == '':
            continue
        if ignoreLine(line, candName) == True:
            continue
        elif count == 0:
            tweetString = line
        elif count == 1:
            coordinates = line
        elif count == 2:
            tweet_id = line
        elif count == 3:
            tweeter_sn = line
        elif count == 4:
            tweetTime = line
            if tweet_id not in idDict:
                innerDict = {"tweetString": tweetString, "coordinates":coordinates,
                             "tweet_id":tweet_id, "tweeter_sn": tweeter_sn, "tweetTime": tweetTime}
                idDict[tweet_id] = innerDict
        elif count == 5:
            if re.search("BREAK", line) is None:
                raise Exception(line)
            count = 0
            continue
        count += 1
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(idDict)

def ignoreLine(line, candName):

    test2String = candName + " Senate"
    test3String = candName + " " + state
    test4String = candName + r' Republican|Democrat'
    test5String = r'"' + candName + r'"'
    test1 = re.search(r'\d+ tweets found', line) is not None
    test2 = re.search(test2String, line) is not None
    test3 = re.search(test3String, line) is not None
    test4 = re.search(test4String, line) is not None
    test5 = re.search(test5String, line) is not None
    print repr(line)
    print test1
    print test2
    print test3
    print test4
    print test5
    return (test1 or test2 or test3 or test4 or test5)


if __name__ == "__main__":
        candDict = {}
        stateCandDict = {}
        candidateList = {"Gary Peters":"MI", "Terri Lynn Land":"MI","Al Franken":"MN","Mike McFadden":"MN",
                         "Mark Begich":"AK","Dan Sullivan":"AK","Mark Pryor":"AR","Tom Cotton":"AR","Mark Udall":"CO",
                         "Cory Gardner":"CO","David Perdue":"GA","Michelle Nunn":"GA","Bruce Braley":"IA",
                         "Joni Ernst":"IA","Pat Roberts":"KS","Greg Orman":"KS","Jeanne Shaheen":"NH",
                        "Scott Brown":"NH","Kay Hagan":"NC","Thom Tillis":"NC","Mitch McConnell":"KY",
                        "Alison Grimes":"KY","Mary Landrieu":"LA","Bill Cassidy":"LA","Rob Maness": "LA"}

        #for candidate, state in candidateList.iteritems():
        candidate = "Al Franken"
        state = "MN"
        if state not in stateCandDict.keys():
            stateCandDict[state] = []
        stateCandDict[state].append(createCandidateDict(candidate, state))


