import RankCalculator
import csv

schoolslink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQfU-xYwtTc9nlW_tpsEmk-TMlUqsvzLooC8m3tcFnS7ig3lvWkA_b_2BxzUNGik8zq6IV-Lg9BwGSV/pub?output=csv"
regattaLink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQfeyC1LeMtdi0qIz-GWxke3jPQ1jJzp72YNi_I9YXF1f73HXUBRTG7AqePHI_L5X54HVwAofxueTiO/pub?output=csv"
rankingsOutputFile = "rankings.csv"
componentScoresFile = "component scores.csv"


ranks, schoolobjects = RankCalculator.calculateRanks(regattaLink, schoolslink)

f = open(rankingsOutputFile, "w")
f.truncate()
f.close()

with open(rankingsOutputFile, 'w') as result:
    writer = csv.writer(result, delimiter=",")
    writer.writerow(('School', 'Score'))
    for row in ranks:
        row = (row[0], str(row[1]))
        writer.writerow(row)


f = open(componentScoresFile, "w")
f.truncate()
f.close()

with open(componentScoresFile, 'w') as result:
    writer = csv.writer(result, delimiter=",")
    writer.writerow(('School', 'Counted Scores Regular Regattas', 'Championship Score'))
    for school in schoolobjects:
        obje = schoolobjects[school]
        row = (obje.name, obje.countedPoints, obje.SRegattaScore)
        writer.writerow(row)
