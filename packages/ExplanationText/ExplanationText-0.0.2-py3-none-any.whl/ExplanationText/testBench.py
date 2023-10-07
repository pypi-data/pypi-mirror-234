import json
import os
import random
from datetime import datetime
from explanationGeneratorMain import *


class TestBench:
    """
    A testbench class that reads data from a file and provides a testData method to
    test the ExplanationText implementation automatically
    """

    def __init__(self, inputFolderPath, apiToken, mode="ExplanationGeneratorV1", outputPath="output"):
        """
        Constructor for the testbench class, calls read_data method and sets in- and output folder paths
        """
        self.folderPath = inputFolderPath
        self.outputPath = outputPath
        self.mode = mode
        self.samples = self.read_data()
        self.modeDescription = str(self.mode)
        self.imageMaxSize = 5
        self.imageSize = random.randint(1, self.imageMaxSize)
        self.apiToken = apiToken

    def read_data(self):
        """
        Method to read data from all .txt files in a given folder return as a list
        """
        print("Start reading data from files")
        data = []
        for root, dirs, files in os.walk(self.folderPath):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        data.extend([line.strip() for line in lines])
        print("Data from files read")
        return data

    def write_output(self, explanations, filename):
        """
        Method to write explanation into output .txt file
        """
        outputFolderExists = os.path.exists(self.outputPath)
        if not outputFolderExists:
            print("Directory for output " + str(self.outputPath) + " does not exist")
            os.makedirs(self.outputPath)
            print("New output directory is created")
        file_path = os.path.join(self.outputPath, filename + ".txt")
        with open(file_path, 'x') as f:
            if not type(explanations) == list:
                explanations = [explanations]
            for explanation in explanations:
                f.write(json.dumps(explanation, indent=4, ensure_ascii=False) + '\n')

    def test_data(self, objectCount, randomize=True, writeToFile=False):
        """
        Method to test sample labels with given length and optional randomization
        and optional write into output file
        """

        # catch a too big sample count
        if objectCount > len(self.samples) or objectCount < 1:
            print("Length of testdata is smaller then desired number of test samples or below 1.")
            objectCount = len(self.samples)

        # get test data sample
        test_data = []
        if randomize:
            for i in range(objectCount):
                x = random.sample(self.samples, 1)
                test_data.append(x[0])
        else:
            for i in range(min(objectCount, len(self.samples))):
                test_data.append(self.samples[i])

        # parse test data sample
        parsed_test_data = self.parse_test_data(test_data)
        print("Test Data parsed")
        # print(json.dumps(parsed_test_data, indent=3))

        # generate explanations
        explanations = []
        explanations.extend(["--- Explanations for Mode: " + self.modeDescription + " ---"])
        explanations.extend(self.generate_explanations(parsed_test_data))

        # write in output file
        if writeToFile:
            print("Writing into output file..")
            now = datetime.now()
            filename = now.strftime("explanation_%d%m%Y_%H%M%S")
            self.write_output(explanations, filename)
            print("Explanations written into file " + str(filename))

    def generate_explanations(self, parsed_test_data):
        explanationGenerator = ExplanationGenerator(mode=self.mode, apiToken=self.apiToken)
        print("\nStart testing samples with mode " + str(self.modeDescription))

        explanations = []
        averageTimes = []
        for testSample in parsed_test_data:
            explanation, averageTime = explanationGenerator.generate_explanation(testSample)
            print(json.dumps(explanation, indent=4, ensure_ascii=False))
            print("")
            explanations.append(explanation)
            averageTimes.append(averageTime)

        totalAverageTime = round(sum(averageTimes) / len(averageTimes), 2)
        print("All samples tested with an total average of " + str(totalAverageTime) + " seconds per object")
        return explanations

    def parse_test_data(self, data):
        """
        Method to parse raw text line from text file into list of main label and part label
        """
        objectList = []
        unusableCount = 0

        # for each line of read data
        for sample in data:
            sample_split = sample.split(";")
            if len(sample_split) == 0 or sample_split[0] == "":
                unusableCount += 1
            else:

                # Parse main label and probability
                split = sample_split[0].split(",")
                mainLabel = split[0]
                newSample = {'heatmap': 'base64', 'label': mainLabel}

                if len(split) > 1:
                    probability = split[1].replace(",", ".")
                    try:
                        probability = float(probability)
                        newSample.update({'probability': probability})
                    except ValueError:
                        pass

                sample_split.pop(0)

                # Parse each part label
                partLabelList = []
                for partLabel in sample_split:
                    split = partLabel.split(",")
                    if len(split) > 0 and not split[0] == "":
                        newPartLabel = {"img": "base64", "rect": "(0, 0, 0, 0)", 'labels': {mainLabel: [split[0][1:]]}}

                        # Optionally add relevance and position
                        if len(split) > 1:
                            relevance = split[1].replace(",", ".")
                            try:
                                relevance = float(relevance)
                                newPartLabel.update({'relevancy': relevance})
                            except ValueError:
                                pass
                        if len(split) > 2:
                            newSample.update({'position': split[2][1:]})

                        partLabelList.append(newPartLabel)

                        newSample.update({'parts': partLabelList})
                objectList.append(newSample)

        if unusableCount > 0:
            print(str(unusableCount) + " samples where unusable")

        imageList = []
        while len(objectList) >= 1:
            if len(objectList) < self.imageSize:
                imageList.append({"image": "base64", "objects": objectList})
                break
            else:
                objects = []
                for i in range(self.imageSize):
                    objects.append(objectList.pop(0))
                imageList.append({"image": "base64", "objects": objects})
            self.imageSize = random.randint(1, self.imageMaxSize)
        return imageList


# TestBench Demo
demoApiToken = "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"
testBench = TestBench('testData', demoApiToken, mode="ExplanationGeneratorV1")
testBench.test_data(100, writeToFile=True, randomize=True)
