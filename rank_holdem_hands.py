import json
import pandas as pd
import csv

NUM_PLAYER_LIST = ["6p", "9p"]


def transformHand(handsStr):
    handList = handsStr.split(",")
    hand1 = handList[0].strip()
    hand2 = handList[1].strip()

    hand1Num = hand1[0]
    hand1Suit = hand1[1]

    hand2Num = hand2[0]
    hand2Suit = hand2[1]

    # Data is designed to have hand1Num > hand2Num
    # Thus, no need to check and reverse the hands

    # When hand is pair
    if(hand1Num == hand2Num):
        return ("Pair " + hand1Num.upper())
    
    # When hand is suited
    if(hand1Suit == hand2Suit):
        return ("Suited " + (hand1Num + hand2Num).upper())

    return ("Offsuit " + (hand1Num + hand2Num).upper())


def createTransformedHandOddsDict(handList, oddsList):
    transformedHandOddsDict = {}


    for i in range(len(handList)):
        hand = handList[i]
        odds = oddsList[i]

        transformedHand = transformHand(hand)

        if(transformedHand not in transformedHandOddsDict):
            transformedHandOddsDict[transformedHand] = []

        transformedHandOddsDict[transformedHand].append(odds)
    
    return transformedHandOddsDict


def createHandAvgOddsTupleList(transformedHandOddsDict):
    tHandAvgOddsTupleList = []

    for tHand, oddsList in transformedHandOddsDict.items():
        avgOdds = round(sum(oddsList)/float(len(oddsList)), 5)

        tHandAvgOddsTupleList.append((tHand, avgOdds))
    
    tHandAvgOddsTupleList = sorted(tHandAvgOddsTupleList, key=lambda x:x[1], reverse=True)

    return tHandAvgOddsTupleList

def createHandAvgOddsTupleDict(transformedHandOddsDict):
    tHandAvgOddsTupleDict = {}

    for tHand, oddsList in transformedHandOddsDict.items():
        avgOdds = round(sum(oddsList)/float(len(oddsList)), 5)
        tHandAvgOddsTupleDict[tHand] = avgOdds

    return tHandAvgOddsTupleDict


def mergeResultIntoDf(tHandAvgOdds6pTupleList, transformedHandAvgOdds9pDict):
    mergedResultDict = {
        'rank': [],
        'hand': [],
        'odds_6p': [],
        'odds_9p': []
    }


    for i in range(len(tHandAvgOdds6pTupleList)):
        tHand6p = tHandAvgOdds6pTupleList[i][0]

        odds6p = tHandAvgOdds6pTupleList[i][1]
        odds9p = transformedHandAvgOdds9pDict[tHand6p]

        mergedResultDict['rank'].append(i+1)
        mergedResultDict['hand'].append(tHand6p)
        mergedResultDict['odds_6p'].append(odds6p)
        mergedResultDict['odds_9p'].append(odds9p)

    mergedResultDf = pd.DataFrame(data=mergedResultDict)
    
    return mergedResultDf


if __name__ == "__main__":
    npTHandAvgOddsTupleListDict = {}

    # For 6p
    csvFileName = "data/handWinRate_6p.csv"
    handWinRateDf = pd.read_csv(csvFileName, header=None)

    handList = handWinRateDf.iloc[:, 0].values
    oddsList = handWinRateDf.iloc[:, 1].values

    transformedHandOdds6pDict = createTransformedHandOddsDict(handList, oddsList)

    tHandAvgOdds6pTupleList = createHandAvgOddsTupleList(transformedHandOdds6pDict)


    # For 9p
    csvFileName = "data/handWinRate_9p.csv"
    handWinRateDf = pd.read_csv(csvFileName, header=None)

    handList = handWinRateDf.iloc[:, 0].values
    oddsList = handWinRateDf.iloc[:, 1].values

    transformedHandOdds9pDict = createTransformedHandOddsDict(handList, oddsList)
    transformedHandAvgOdds9pDict = createHandAvgOddsTupleDict(transformedHandOdds9pDict)

    resultDf = mergeResultIntoDf(tHandAvgOdds6pTupleList, transformedHandAvgOdds9pDict)

    print(resultDf)


    resultCsvFileName = "result/hand_rank.csv"
    resultDf.to_csv(resultCsvFileName, index=False)

    resultJsonFilename = "result/hand_rank.json"
    jsonStr = resultDf.to_json(orient="index")

    with open(resultJsonFilename, "w") as text_file:
        text_file.write(jsonStr)
