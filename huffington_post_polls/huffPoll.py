import requests
import json

def pullData():
    replyDict = {}
    stateList = ["NC", "AK", "AR", "KY", "CO", "LA", "GA", "NH", "IA", "KS", "MI", "MN"]
    for state in stateList:
        replyDict[state] = {}
        print state
        endpoint = "http://elections.huffingtonpost.com/pollster/api/polls.json?state=" + state +"&topic=2014-senate"
        response = requests.get(endpoint)
        data = response.json()
        print len(data)
        for element in data:
            id = element["id"]
            print id
            partisan = element["partisan"]
            start_date = element["start_date"]
            end_date = element["end_date"]
            questions = element["questions"]
            replyDict[state][id] = {}
            replyDict[state][id]["partisan"] = partisan
            replyDict[state][id]["start_date"] = start_date
            replyDict[state][id]["end_date"] = end_date
            replyDict[state][id]["questions"] = {}
            for question in questions:
                qchart = question["chart"]
                responses = question["subpopulations"][0]["responses"]
                replyDict[state][id]["questions"][qchart] = {}
                for response in responses:
                    choice = response["choice"]
                    value = response["value"]
                    print str(choice) + ": " + str(value)
                    replyDict[state][id]["questions"][qchart][choice] = value

    replyJSON = json.dumps(replyDict, indent=4)
    outputFile = open("huffPoll.json", "w")
    print >> outputFile, replyJSON



if __name__ == "__main__":
    pullData()

