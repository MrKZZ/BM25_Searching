import csv

def prasecsv():
    csvFile = open('clinical_trials.judgments.2017.csv', "r")
    reader = csv.reader(csvFile)
    judgement = {}
    for item in reader:
        if item[0] not in judgement:
            judgement[item[0]] = item[1]
        else:
            judgement[item[0]] += " "+item[1]
    return judgement
