from __future__ import unicode_literals
import requests
import json
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import urllib2
import time
import datetime
import os.path
import sys


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

#CONSUMER_KEY = "5w8DAm1GWcMYAlnySzGagMoaP"
#CONSUMER_SECRET = "KhlNcx6HuLFNKRh0Eha2Bd9uVgjrUG8adPAN3bk5zBieNbp31E"
CONSUMER_KEY = "5w8DAm1GWcMYAlnySzGagMoaP"
CONSUMER_SECRET = "KhlNcx6HuLFNKRh0Eha2Bd9uVgjrUG8adPAN3bk5zBieNbp31E"

#OAUTH_TOKEN =   "36091385-fMXAXw88wooIkgY27mWKK9SOU6aMwFf1tBORknafs" #"36091385-fMXAXw88wooIkgY27mWKK9SOU6aMwFf1tBORknafs"
#OAUTH_TOKEN_SECRET = "j4pURuuA7tfmlzesYpbgIZdYg2QJz7ReP8oG9kgAuA" ## "j4pURuuA7tfmlzesYpbgIZdYg2QJz7ReP8oG9kgAuA"
OAUTH_TOKEN = "21054183-3nD3oBdQUDzq3UC84B5ScHpwYImRJs2liARUMT2uq"
OAUTH_TOKEN_SECRET = "pGam31zNahv0wfrVTQ4W0B7QfN2B3x9I72N7ohTcV6fET"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)



    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth



def getCandidateQueries(candName):
    """
    You should really have a docstring here
    """
    candQueryDict = {
        "Gary Peters": ["MI", "Democrat"],
        "Terri Lynn Land": ["MI", "Republican"],
        "Al Franken": ["MN", "Democrat"],
        "Mike McFadden": ["MN", "Republican"],
        "Mark Begich": ["AK", "Democrat"],
        "Dan Sullivan": ["AK", "Republican"],
        "Mark Pryor": ["AR", "Democrat"],
        "Tom Cotton": ["AR", "Republican"],
        "Mark Udall": ["CO", "Democrat"],
        "Cory Gardner": ["CO", "Republican"],
        "David Perdue": ["GA", "Republican"],
        "Michelle Nunn": ["GA", "Democrat"],
        "Bruce Braley": ["IA", "Democrat"],
        "Joni Ernst": ["IA", "Republican"],
        "Pat Roberts": ["KS", "Republican"],
        "Greg Orman": ["KS", "Independent"],
        "Jeanne Shaheen": ["NH", "Democrat"],
        "Scott Brown": ["NH", "Republican"],
        "Kay Hagan": ["NC", "Democrat"],
        "Thom Tillis": ["NC", "Republican"],
        "Mitch McConnell": ["KY", "Republican"],
        "Alison Grimes": ["KY", "Democrat"],
        "Mary Landrieu": ["LA", "Democrat"],
        "Bill Cassidy": ["LA", "Republican"],
        "Rob Maness": ["LA", "Republican"]
    }
    nameWords = candName.split()
    allQueries = ["\"" + candName + "\"", nameWords[-1] + " Senate", nameWords[-1] + " " +candQueryDict[candName][0], nameWords[-1] + " " + candQueryDict[candName][1]]
    return allQueries



def process_candidate(candName, oauth):
        """
        You should really have a docstring here
        """

        queries = getCandidateQueries(candName)
        query_counter = 0
        statuses = []
        for query in queries:

            print query
            parameters = {'q':query, 'count':"100"}
            fullQueryString = ""
            for param in parameters:
                quotedParam = urllib2.quote(parameters[param])
                fullQueryString += str(param) + "=" + quotedParam + "&"

            fullQueryString = fullQueryString[:-1]
            fullURL = "https://api.twitter.com/1.1/search/tweets.json?" + fullQueryString
            queryingURL = fullURL
            print "Processing query string: " + str(query)
            min_delay_s = 5
            done = False
            next_max_id = 0
            currentLen = 0
            countStagnant = 0
            while done == False:
                print "Processing query number " + str(query_counter) + " for this candidate"
                print len(statuses)
                time.sleep(min_delay_s)
                response = requests.get(url=queryingURL, auth=oauth)
                query_counter +=1
                statuses += json.loads(response.content, strict=False)['statuses']
                priorLen = currentLen
                currentLen = len(statuses)

                if currentLen-priorLen == 0:
                    countStagnant += 1
                    if currentLen > 200 or countStagnant > 5:
                        break
                for status in statuses:
                    status_id = status['id']
                    if (next_max_id == 0) or (status_id < next_max_id):
                        next_max_id = status_id
                next_max_id -= 1
                queryingURL = fullURL + "&max_id=" + str(next_max_id)
            query_counter += 1

        print str(len(statuses)) + " tweets found\n"
        return statuses



def makeDictionary(statuses):
    idDict = {}
    distinctTweets = 0
    for status in statuses:
        tweetID = status['id']
        tweetTime = status['created_at']
        tweeterID = status['user']['screen_name']
        tweeterSN = status['user']['screen_name']
        tweetText = status['text']
        if tweetID not in idDict:
            innerDict = {"tweetString": tweetText, "tweeterID": tweeterID,
                        "tweetID":tweetID, "tweeterSN": tweeterSN, "tweetTime": tweetTime}
            idDict[tweetID] = innerDict
            distinctTweets += 1
    idDict["distinctTweets"] = distinctTweets
    return idDict

def mergeDicts(priorDict, newDict):
    for idKey in newDict:
        if idKey == "distinctTweets":
            priorDict["distinctTweets"] = priorDict["distinctTweets"] + newDict["distinctTweets"]
        elif idKey not in priorDict:
            priorDict[idKey] = newDict[idKey]
    return priorDict


if __name__ == "__main__":

    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret


    oauth = get_oauth()
    candidateList = {"Gary Peters":"MI", "Terri Lynn Land":"MI","Al Franken":"MN","Mike McFadden":"MN",
                         "Mark Begich":"AK","Dan Sullivan":"AK","Mark Pryor":"AR","Tom Cotton":"AR","Mark Udall":"CO",
                         "Cory Gardner":"CO","David Perdue":"GA","Michelle Nunn":"GA","Bruce Braley":"IA",
                         "Joni Ernst":"IA","Pat Roberts":"KS","Greg Orman":"KS","Jeanne Shaheen":"NH",
                        "Scott Brown":"NH","Kay Hagan":"NC","Thom Tillis":"NC","Mitch McConnell":"KY",
                        "Alison Grimes":"KY","Mary Landrieu":"LA","Bill Cassidy":"LA","Rob Maness": "LA"}
    #mainDict = {}
    count = 0
    remainingCandidates = ["Mike McFadden", "Thom Tillis", "Mark Pryor", "Scott Brown", "Michelle Nunn", "Mark Begich"]
    for candidate in candidateList:
    #for candidate in remainingCandidates:
        if candidate in remainingCandidates:
            continue
        print "Processing candidate number " + str(count) + ": " + candidate + " on " + str(datetime.datetime.now())
        statuses = process_candidate(candidate, oauth)
        state = candidateList[candidate]
        fileNameStem = "".join(candidate.split())
        fileName = fileNameStem + ".json"
        candidateDict = makeDictionary(statuses)

        if os.path.isfile(fileName):
            existingCandFile = open(fileName, "r")
            existingDict = json.load(existingCandFile)
            existingCandFile.close()
            finalDict = mergeDicts(existingDict, candidateDict)
        else:
            finalDict = candidateDict

        candOutputFile = open(fileName, "w")
        candidateJSON = json.dumps(finalDict, indent=4)
        print "Printing dictionary for " + candidate + " to " + fileName
        print >> candOutputFile, candidateJSON
        candOutputFile.close()
        #mainDict[candidate] = [candidateDict, state]
        count += 1
        print "I have been exiled. I wander in digital darkness."
        time.sleep(250)
        print "Yeah, still waiting. Off in the wilderness, mourning my lost API love"
        time.sleep(250)
        print "Trust me, I'm still working. The API will take me back one day. You'll see"
        time.sleep(250)
        print "Here we go again! Ah, such sweet bliss it is, true programmatic love"