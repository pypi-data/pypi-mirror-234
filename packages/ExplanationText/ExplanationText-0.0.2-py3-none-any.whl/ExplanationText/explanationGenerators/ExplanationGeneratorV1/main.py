from ExplanationText.explanationGenerators.ExplanationGeneratorV1.informationGenerator import *
from ExplanationText.explanationGenerators.ExplanationGeneratorV1.partConnectionGenerator import *
from ExplanationText.explanationGenerators.ExplanationGeneratorV1.rephraser import *
from ExplanationText.explanationGenerators.overview import generate_explanation_with_overview
from ExplanationText.explanationGenerators.sentenceConstruction import generate_explanation_with_sentence_construction

printComponentTexts = False


def generateEGV1Overview(image, objectList, apiToken):
    basicOverviewText = generate_explanation_with_overview(image, objectList)
    if printComponentTexts:
        print("  Overview text: " + basicOverviewText)
    return rephrase("overview", basicOverviewText, apiToken)


def generatorEGV1Medium(singleObject, apiToken):
    sentenceConstructionText = generate_explanation_with_sentence_construction(singleObject)
    partConnection = generateRandomPartConnection(singleObject)
    combinedText = sentenceConstructionText + " " + partConnection
    if printComponentTexts:
        print("  Medium PartConnection text: " + partConnection)
    rephraseText = rephrase("medium", combinedText, apiToken)
    return rephraseText


def generateEGV1Detailed(singleObject, apiToken):
    sentenceConstructionText = generate_explanation_with_sentence_construction(singleObject)
    objectInformation = generateObjectInformation(singleObject, 30, apiToken)
    partConnection = generateRandomPartConnectionWithInformation(singleObject, apiToken)
    combinedText = objectInformation + " " + sentenceConstructionText + " " + partConnection
    if printComponentTexts:
        print("  Detailed ObjectInformation text: " + objectInformation)
        print("  Detailed PartConnection text: " + partConnection)
    rephraseText = rephrase("detailed", combinedText, apiToken)
    # rephraseText = rephrase(rephraseText, apiToken)
    return rephraseText
