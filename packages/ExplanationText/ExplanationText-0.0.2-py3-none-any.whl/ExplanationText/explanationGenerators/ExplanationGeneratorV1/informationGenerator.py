from ExplanationText.explanationGenerators.APIUtils import queryTextGenerationOrText2Text

endpoint = "https://api-inference.huggingface.co/models/"


def generateObjectInformation(singleObject, length, apiToken):
    inputObject = singleObject.get("label")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiToken}"}

    configuration = {'return_full_text': False, 'num_return_sequences': 1, 'max_new_tokens': length,
                     'no_repeat_ngram_size': 1,
                     'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': length, 'top_p': 0.9,
                     'temperature': 0.5}
    prompt = "<|prompter|>Explain the main function of the following object: " + inputObject + \
             " Explanation:<|endoftext|><|assistant|>"
    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]

    (success, returnText) = queryTextGenerationOrText2Text(query, endpoint, headers)
    if success:
        return text_bis_letzter_punkt(returnText)
    return ""


def generatePartInformation(singleObject, part, length, apiToken):
    inputObject = singleObject.get("label")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiToken}"}

    configuration = {'return_full_text': False, 'num_return_sequences': 1, 'max_new_tokens': length,
                     'no_repeat_ngram_size': 1,
                     'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': length, 'top_p': 0.9,
                     'temperature': 0.9}
    prompt = "<|prompter|>Explain the main function of an " + part + " in object: " + inputObject + \
             " Explanation:<|endoftext|><|assistant|>"
    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]

    (success, returnText) = queryTextGenerationOrText2Text(query, endpoint, headers)
    if success:
        return text_bis_letzter_punkt(returnText)
    return ""


def text_bis_letzter_punkt(text):
    index = text.rfind('.')
    if index != -1:
        return text[:index + 1]
    else:
        return ''
