import requests
import re
import time
import random
import json

API_KEY = '441fa6e7e06b2a19b8270a92597abadd:2:69908438'

def get_cand_IDs():
    candidateList = {"Gary Peters":"MI", "Terri Lynn Land":"MI","Al Franken":"MN","Mike McFadden":"MN",
                             "Mark Begich":"AK","Dan Sullivan":"AK","Mark Pryor":"AR","Tom Cotton":"AR","Mark Udall":"CO",
                             "Cory Gardner":"CO","David Perdue":"GA","Michelle Nunn":"GA","Bruce Braley":"IA",
                             "Joni Ernst":"IA","Pat Roberts":"KS","Greg Orman":"KS","Jeanne Shaheen":"NH",
                            "Scott Brown":"NH","Kay Hagan":"NC","Thom Tillis":"NC","Mitch McConnell":"KY",
                            "Alison Grimes":"KY","Mary Landrieu":"LA","Bill Cassidy":"LA","Rob Maness": "LA"}

    req_dict = {}
    for candName, state in candidateList.iteritems():
        cand_search_endpoint = 'http://api.nytimes.com/svc/elections/us/v3/finances/2014/seats/{0}/senate.json?api-key=441fa6e7e06b2a19b8270a92597abadd:2:69908438'.format(state)
        response = requests.get(cand_search_endpoint)
        print cand_search_endpoint
        data = response.json()
        results = data['results']
        lastName = candName.split()[-1]
        for result in results:
            if re.search(lastName.upper(), result['candidate']['name']) is not None:
                print result['candidate']['name']
                req_dict[candName] = {}
                req_dict[candName]['fec_id'] = result['candidate']['id']
                req_dict[candName]['committee_url'] = result['committee']
                req_dict[candName]['canon_name'] = result['candidate']['name']
        wait_time = round(max(0, 1 + random.gauss(0, 0.5)), 2)
        time.sleep(wait_time)
    return req_dict

# f = open("nytLookup.json", "w")
# jsonDict = json.dumps(req_dict, indent=4)
# print >> f, req_dict


#go through results from http://api.nytimes.com/svc/elections/us/{version}/finances/{campaign-cycle}/committees/{fec-id}/filings[.response-format]?api-key={your-API-key}[&callback={callback-function}]
#look for F9 (maybe other?)
#Get date and maybe amount