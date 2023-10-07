import time
import copy

from ExplanationText.explanationGeneratorUtils import *
from ExplanationText.explanationGenerators.ApiTest.APITest import generate_explanation_with_APITest
from ExplanationText.explanationGenerators.ExplanationGeneratorV1.main import *
from ExplanationText.explanationGenerators.overview import generate_explanation_with_overview
from ExplanationText.explanationGenerators.sentenceConstruction import generate_explanation_with_sentence_construction


class ExplanationGenerator:
    """
    Main class of Explanation Generator that runs generation methods of
    different text generation methods with given mode.
    """

    def __init__(self, apiToken="", mode="ExplanationGeneratorV1",
                 minimumRelevance=10,
                 maximumPartCount=5):
        """
        Constructor sets explanation mode, default one is sentence construction.
        """
        self.apiToken = apiToken
        self.mode = str.lower(mode)
        self.minimumRelevance = minimumRelevance
        self.maximumPartCount = maximumPartCount

    def generate_explanation(self, image):
        """
        Main method to generate text explanation for given image.
        Returns Explanation text for mode overview and individual ones for each object
        """
        image_copy = copy.deepcopy(image)
        # Validate input
        label_list, object_list = validateAndParseImage(image_copy, self.minimumRelevance, self.maximumPartCount)
        fullExplanation = {}

        # Overview Mode
        overviewText = ""
        if self.mode == str.lower('OverviewBasic'):
            overviewText = generate_explanation_with_overview(object_list, label_list)
        elif self.mode == str.lower('ExplanationGeneratorV1'):
            overviewText = generateEGV1Overview(object_list, label_list, self.apiToken)
        else:
            print("The desired text explanation overview mode " + self.mode + " isn't implemented yet")
        fullExplanation.update({"overview": overviewText})

        measuredTimes = []
        for singleObject in object_list:
            startTime = time.time()
            objectName = singleObject.get("label")

            # Medium Mode
            mediumText = ""
            if self.mode == str.lower('SentenceConstruction'):
                mediumText = generate_explanation_with_sentence_construction(singleObject)
            elif self.mode == str.lower('ApiTest'):
                mediumText = generate_explanation_with_APITest(singleObject)
            elif self.mode == str.lower('ExplanationGeneratorV1'):
                mediumText = generatorEGV1Medium(singleObject, self.apiToken)
            else:
                print("The desired text explanation mode " + self.mode + " isn't implemented yet")

            # Detailed Mode
            detailedText = ""
            if self.mode == str.lower('SentenceConstruction'):
                detailedText = generate_explanation_with_sentence_construction(singleObject)
            elif self.mode == str.lower('ApiTest'):
                detailedText = generate_explanation_with_APITest(singleObject)
            elif self.mode == str.lower('ExplanationGeneratorV1'):
                detailedText = generateEGV1Detailed(singleObject, self.apiToken)

            # Append to return value
            while objectName in fullExplanation:
                objectName = objectName + "_"
            fullExplanation.update({objectName: {"medium": mediumText, "detailed": detailedText}})

            # measureTime
            endTime = time.time()
            measuredTimes.append(endTime - startTime)

        averageTime = round(sum(measuredTimes) / max(len(measuredTimes), 1), 2)
        # do not print time in package
        # print("Average time for generating explanation per object: " + str(averageTime) + " sec")

        return fullExplanation  # , averageTime
