import random

from ExplanationText.explanationGenerators.ExplanationGeneratorV1.informationGenerator import generatePartInformation


def generateRandomPartConnection(singleObject):
    text = ""
    if 'parts' in singleObject:
        try:
            for part in singleObject['parts']:
                connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
                text += f"{part['partLabel']} is {connection} connected to " + singleObject['label'] + ". "
        except KeyError:
            print(singleObject)
    return text


def generateRandomPartConnectionWithInformation(singleObject, apiToken):
    text = ""
    if 'parts' in singleObject:
        for part in singleObject['parts']:
            connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
            text += f"{part['partLabel']} is {connection} connected to " + singleObject['label'] + ". "
            text += generatePartInformation(singleObject, part['partLabel'], 30, apiToken) + ". "
    return text
