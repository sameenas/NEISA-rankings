import pandas as pd
import numpy as np
import GoogleSheets
import TechscoreReader
import csv

class School:
    def __init__(self, name):
        self.name = name
        self.points = []
        self.SRegattaScore = (0, None)
        self.countedPoints = [] #if this is empty then all the points are counted

    def addPoints(self,x,regattaName):
        self.points.append((x, regattaName))
        self.points = sorted(self.points, key=lambda x: x[0], reverse=True)

    def getPointsTotal(self):
        if len(self.points) > 3:
            self.countedPoints = [self.points[0], self.points[1], self.points[2], self.points[3]]
        return sum([pair[0] for pair in self.countedPoints]) + self.SRegattaScore[0]

def calculateRank(type, totalTeams, score):
    if score == 0:
        return 0
    first = None
    last = 0
    if type == "A":
        first = 8.5
    elif type == "B":
        first = 5.01
    elif type == "C":
        first = 4.16
    elif type == "WSC":
        first = 10.0
    elif type == "WA":
        first = 8.5
    elif type == "WB":
        first = 7.0
    elif type == "SC":
        first = 10.0
        last = 5.0
    elif type == "SC_alt":
        first = 7

    droprate = .005 * first
    amounttodrop = (18-totalTeams)*droprate
    first = first - amounttodrop
    rankvalue = -1.0 * (first-last) / (totalTeams-1) * (score-1) + first
    if (abs(rankvalue) < .003): rankvalue = 0.0
    return rankvalue

def enterScores(schoolobjects, data, type, totalTeams, regattaName):
    data = list(data)
    seen = set()
    offset = 0
    for scoreind in range(len(data)):
        team = data[scoreind]
        if team in seen:
            offset += 1
            continue
        seen.add(team)
        score = calculateRank(type, totalTeams, scoreind+1-offset)
        if team in schoolobjects:
            schoolobjects[team].addPoints(score, regattaName)

def enterSScores(schoolobjects, data, type, totalTeams, regattaName):
    data = list(data)
    if type == "SC_A":
        type = "SC"
    elif type == "SC_B":
        type = "B"
    elif type == "WSC_A":
        type = "WSC"
    else:
        "AHHH you did something stupid"

    for scoreind in range(len(data)):
        team = data[scoreind]
        score = calculateRank(type, totalTeams, scoreind+1)
        if team in schoolobjects:
            if schoolobjects[team].SRegattaScore[0] == 0:
                schoolobjects[team].SRegattaScore = (score, regattaName)
            else:
                print("hmm you tried to add two s scores to the same school object")

def getRank(schoolobjects):
    tuplist = []
    for schoolname in schoolobjects:
        school = schoolobjects[schoolname]
        tuplist.append((school.name, school.getPointsTotal()))
    tuplist.sort(key=lambda x: x[1], reverse = True)
    return tuplist

def addSchoolObjects(schoolsLink):
    schools = GoogleSheets.readSheet(schoolsLink).Schools
    schoolobjects = {}
    for school in schools:
        schoolobjects[school] = School(school)
    return schoolobjects

def calculateRanks(regattaLink, schoolsLink):
    df = GoogleSheets.readSheet(regattaLink)
    schoolobjects = addSchoolObjects(schoolsLink)
    for index, regatta in df.iterrows():
        regattaType = regatta.Type
        regattaFinishes, totalTeams = TechscoreReader.getRegattaResultsAndNumTeams(regatta.Link)
        regattaName = (regatta.Link.split("/"))[-2]
        if regattaType in ("SC_A", "WSC_A", "SC_B"):
            enterSScores(schoolobjects, regattaFinishes, regattaType, totalTeams, regattaName)
            continue

        if (regattaType == "A") and (totalTeams < 18):
            totalTeams = 18

        if regattaType == "special_A":
            regattaType = "A"

        if regattaType not in ("A", "special_A", "WSC", "B", "C", "WA", "WB", "SC", "SC_alt"):
            print("incorrect regatta type; something is wrong")
            continue

        enterScores(schoolobjects, regattaFinishes, regattaType, totalTeams, regattaName)

    return (getRank(schoolobjects), schoolobjects)


def CalculateScoreTable(totalTeamsMaximum, totalTeamsMinimum, regattaType):
    totalteams = totalTeamsMaximum
    while totalteams >= totalTeamsMinimum:
        print("for teams:", totalteams)
        for i in range(1, totalteams+1):
            print(calculateRank(regattaType, totalteams, i))
        totalteams = totalteams - 1
