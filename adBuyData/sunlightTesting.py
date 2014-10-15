import requests
import pprint
import json

def dictFromJSON(json, respDict):
    for element in json['objects']:
        doc_status = element["doc_status"]
        if doc_status == "Not loaded":
            continue
        advertiser = element["advertiser"]
        total_spent = element["total_spent"]
        num_spots = element["num_spots"]
        contract_start = element["contract_start_date"]
        contract_end = element["contract_end_date"]
        description = element["description"]
        dma = element["nielsen_dma"]
        state = element["community_state"]
        uuid = element["uuid_key"]
        if state not in respDict:
            respDict[state] = {}
        if uuid not in respDict[state]:
            respDict[state][uuid] = {}
            respDict[state][uuid]["advertiser"] = advertiser
            respDict[state][uuid]["total_spent"] = total_spent
            respDict[state][uuid]["num_spots"] = num_spots
            respDict[state][uuid]["contract_start"] = contract_start
            respDict[state][uuid]["contract_end"] = contract_end
            respDict[state][uuid]["description"] = description
            respDict[state][uuid]["dma"] = dma


if __name__ == "__main__":
    APIKEY = '55d8c834f6144401be9dd2f176c3c753'
    query_params = {'apikey' : APIKEY,
                'format': 'json',
                'limit': 100,
                'contract_start_date__gte':'2014-05-01'
    }

    endpoint = 'http://politicaladsleuth.com/api/v1/politicalfile/?apikey=55d8c834f6144401be9dd2f176c3c753&contract_start_date__gte=2014-01-01&limit=250&format=json'
    moreData = True
    resultDict = {}

    while moreData:
        response = requests.get(endpoint)
        data = response.json()
        print data.keys()
        if not data["objects"]:
            break
        dictFromJSON(data, resultDict)
        nextData = data["meta"]["next"]
        if nextData is None:
            break
        offset = data["meta"]["offset"]
        print str(offset) + " listings processed so far"
        endpoint = "http://politicaladsleuth.com" + nextData

    outputFile = open("nonNullAdSleuthTest.json", "w")
    fullData = json.dumps(resultDict, indent=4)
    print >> outputFile, fullData




#allCandTypes = {}
# for element in data['objects']:
#     type = element['candidate_type']
#     if allCandTypes.get(type) is None:
#         allCandTypes[type] = 0
#     allCandTypes[type] += 1
# pprint.pprint(allCandTypes)

#with open('sunlightTesting.json', 'w') as outfile:
   # json.dump(data, outfile)