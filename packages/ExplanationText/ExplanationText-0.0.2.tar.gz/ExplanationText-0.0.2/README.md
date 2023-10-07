# Explanation Text Generator

##### Version of 18th of September 2023

Class to generate text explanations of image classifications 
in different modes and with given main and part labels.

## Main Usage
Basically these two lines are sufficient, they are described in more details below:
```
explanationGenerator = ExplanationGenerator(<ApiToken>, <Mode>)
explanationText = explanationGenerator.generate_explanation(<Labels>)
```
First you have to create a ExplanationGenerator and set a explanation mode and 
your [HuggingFace API Token](https://huggingface.co/docs/hub/security-tokens), if you want to use modes that uses their API.
The different explanation modes can be found [here](#ExplanationModes). 
If you leave it empty, the sentence construction method will be used. 
Afterward you can call the *generate_explanation* method with your list of labels
receive an explanation text. In order to generate multiple explanations, 
*generate_explanation* can also handle lists of labels and returns a list 
of individual explanation texts.
You can set two more configurations with the constructor. *MinimumRelevance* (default 10)
filters part labels with a relevance percentage below that value and *maximumPartCount* (default 5)
sets the number of maximum part labels that should be used for the explanation text.

## Format
The format of *Labels* should be a python dictionary or a list of dictionary objects.
More specifically this object has to contain a non empty key *mainLabel*, which is the
minimum requirement. Optionally a *probability* with a float value can be set.
Part labels are set as a list with a key *parts*. Each part has to contain a *partLabel*
field and optionally a relevance and position.
```json
{
  "objects": [
    {
      "label": "plane", 
      "probability": 0.9, 
      "position": "left",
      "parts": [
        {"partLabel": "cockpit", "relevance": 0.6}, 
        {"partLabel": "wings", "relevance": 0.2}
       ]
    },
    {
      "label": "tree", 
      "probability": 0.6, 
      "position": "top"
    }
  ]
}
```
This is an example of the label format of an object plane.
Internally the method *generate_explanation* validates, filters and sorts
the given main and part labels.
```json
{
    "img": "image",
        "objects" : [
            {
                "heatmap": "Base64",
                "label": "car",
                "parts": [
                    {
                        "img": "Base64",
                        "relevancy": 2000,
                        "rect": "(0, 0, 0, 0)",
                        "labels": [{"car": ["door", ""]}, {"plane" : ["door"]}]
                    },
                    {
                        "img": "Base64",
                        "relevancy": 2000,
                        "rect": "(0, 0, 0, 0)",
                        "labels": [{"car": ["plane", ""]}]
                    }
                ]
            },
            {} 
        ]
}
```


### UPDATE FOR PROTOTYPE OCTOBER 2023
After communication with the other groups, a new format came up, that we now
use as the input. Internally, as of September 2023, we parse that format into
our old one you can see above, to make sure all our components still work.

## Test Bench Usage
To test the different explanation methods, we created a test bench. 
It reads and parses sample labels from a folder with .txt files and creates
explanation texts with a given mode. Additionally, it can randomize the samples
and write the explanations into an output file.
```
demoApiToken = "<Your Huggingface API Token>"
testBench = TestBench('testData', demoApiToken, mode="ExplanationGeneratorV1")
testBench.test_data(100, writeToFile=True, randomize=True)
```
All parameters, except for *inputFolderPath* and *SampleCount* are optional.
If the sample count number is higher than the given samples, the test bench
uses all the samples. The default output folder path is *ExplanationText/output/*
and can be set with an additional parameter *outputPath*.
If parameter mode is set to *All*, all implemented modes will be tested with the
given data.

## Explanation Modes
Here is an overview of the different explanation text modes.

### ExplanationGeneratorV1
This is currently the best mode to generate texts. It follows the structure 
shown in diagram in confluence under 'Language Models' -> 'Umsetzung' -> 'aktueller Stand'
and described in chapter 3 of the 'Zwischenbericht'. To use it, set attribute *mode* to 
'ExplanationGeneratorV1'.

Positive example of current version:
```
    "overview": "This image contains a train, a horse and a boat.",
    "horse": {
        "medium": 
            "The horse in the image was classified as a horse with 
            99% certainty. The horse was mainly classified that 
            way, because of the head with 40% relevance and neck
            with 24% relevance. The head is strongly connected to
            the horse, while the neck is very strongly connected
            to the horse.",
        "detailed": 
            "The main function of the following object is to 
            provide transportation and support to its rider. The 
            object in the image was classified as a horse with a
            99% certainty, due to the distinctive head and neck 
            features. The head was found to have a high relevance,
            as it is a prominent feature of the horse. The neck 
            was also found to be important, as it is connected to
            the head and appears to provide support to the horse."
    },
    ....
```

It is important to notice, that the implementation of component *partConnection* 
is currently faked with random connections.


### Overview
The mode overview describes only the main labels of an image and should
give an overview of the objects detected. The mode can be set using the string
'Overview'. 
```
The image contains a <main label 1>, .. and a <main label N>.
```
### Sentence Construction
Sentence Construction is the easiest way of creating a detailed explanation text.
It basically just puts the main and part label with additional information into
a fixed sentence structure without any additionally information or processing.
The current variant creates two sentences with the following structure:
```
Object in image was classified as a <main label> with <percentage>%
certainty. The <main label> was mainly classified that way, because
of the <part label> with <percentage>% relevance at position 
<position> , <more part labels> ... and <last part label>
```
The whole second sentence and information about relevance and position are 
optional and will be set if the necessary information is given.
This method can be used with the string 'SentenceConstruction'.

### API Test
API Test is a method to evaluate large language models on [HugginFace](https://huggingface.co/models).
It uses the [HuggingFace API](https://huggingface.co/docs/api-inference/index) to test out sets of models, tasks and prompts.
For this, a *test* can be set up in class [APITest](explanationGenerators/ApiTest/APITest.py) and run with prompts provided by
the Testbench. Examples for test setups can be found in class [APITestUtils](explanationGenerators/APIUtils.py).
It is necessary to create an account on HuggingFace and provide a custom API Key at the top of [APITest](explanationGenerators/ApiTest/APITest.py).

This method can be used with the string 'APITest'.
