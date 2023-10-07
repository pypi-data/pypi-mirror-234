import json
import requests

def queryTextGenerationOrText2Text(query, endpoint, headers):
    """
    Function to process Query for tasks text-generation and text2Text
    """
    payload = {
        "inputs": query[3],
        "parameters": query[4],
        "options": {"wait_for_model": True}
    }
    data = json.dumps(payload)
    responseList = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    try:
        responseList = json.loads(responseList.content.decode("utf-8"))
    except:
        return False, [str(responseList)]

    if type(responseList) == list:
        explanation = responseList[0]['generated_text'].replace('\n', ' ').replace('\r', '')
        return True, explanation

    return False, [str(responseList)]


def queryFillMask(query, endpoint, headers):
    """
    Function to process Query for task fillMask
    Inputs have to contain [MASK] keyword and no parameters can be set
    """
    payload = {
        "inputs": query[3],
        "options": {"wait_for_model": True}
    }
    data = json.dumps(payload)
    responseList = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    responseList = json.loads(responseList.content.decode("utf-8"))

    if type(responseList) == list:
        parsedResponse = []
        for response in responseList:
            explanation = f"Token/Score: {response[0]['token_str']}/{response[0]['score']}, {response[0]['sequence']}"
            parsedResponse.append("     " + explanation.replace('\n', ' ').replace('\r', ''))
        return True, parsedResponse

    return False, [str(responseList)]


def querySummarization(query, endpoint, headers):
    """
    Function to process Query for task summarization
    """

    parameters = query[4]
    parameters['do_sample'] = False
    payload = {
        "inputs": query[3],
        "parameters": parameters,
    }
    data = json.dumps(payload)
    responseList = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    responseList = json.loads(responseList.content.decode("utf-8"))

    if type(responseList) == list:
        parsedResponse = []
        for response in responseList:
            explanation = response['summary_text']
            parsedResponse.append("     " + explanation.replace('\n', ' ').replace('\r', ''))
        return True, parsedResponse

    return False, [str(responseList)]


def queryConversational(query, endpoint, headers):
    """
    Function to process Query for tasks conversational
    Each prompt will be passed to model sequentially
    """
    parsedResponse = []
    past_user_inputs = []
    generated_responses = []

    for prompt in query[3]:
        inputs = {
            "past_user_inputs": past_user_inputs,
            "generated_responses": generated_responses,
            "text": prompt
        }

        payload = {
            "inputs": inputs,
            "parameters": query[4],
            "options": {"wait_for_model": True}
        }

        data = json.dumps(payload)
        response = requests.request("POST", endpoint + query[2], headers=headers, data=data)
        response = json.loads(response.content.decode("utf-8"))

        if 'conversation' in response and 'generated_text' in response:
            explanation = response['generated_text']
            parsedResponse.append("     '" + prompt + "' -> " + explanation.replace('\n', ' ').replace('\r', ''))
            past_user_inputs = response['conversation']['past_user_inputs']
            generated_responses = response['conversation']['generated_responses']
        else:
            return False, [str(response)]

    return True, parsedResponse


def getParts(inputSample, maxParts):
    """
    Help Function to get a string or partLabels with given maximum number of parts
    """
    returnValue = ""
    if 'parts' in inputSample:
        parts = inputSample.get('parts')
        count = 0

        # For each part
        for part in parts:
            partLabel = part.get('partLabel')

            # add part label
            if count < maxParts:
                returnValue += str(partLabel) + ", "
            count += 1

        # Add 'and' instead of last comma
        returnValue = returnValue[:-2]
        if len(parts) > 1:
            last_comma_index = returnValue.rfind(",")
            returnValue = returnValue[:last_comma_index] + " and" + returnValue[last_comma_index + 1:]

    return returnValue
