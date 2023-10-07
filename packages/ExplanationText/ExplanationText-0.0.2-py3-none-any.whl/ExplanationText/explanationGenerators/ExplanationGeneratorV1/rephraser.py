from ExplanationText.explanationGenerators.APIUtils import queryTextGenerationOrText2Text


def rephrase(mode, inputText, apiToken):
    endpoint = "https://api-inference.huggingface.co/models/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiToken}"}
    prompt = "<|prompter|>Paraphrase the following sentence: " + inputText + ". Parapharsed text: " \
                                                                             "<|endoftext|><|assistant|>"

    if mode == "overview":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': len(inputText),
                         'no_repeat_ngram_size': 1,
                         'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': len(inputText), 'top_p': 0.9,
                         'temperature': 0.6}

    elif mode == "medium":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': len(inputText),
                         'no_repeat_ngram_size': 1,
                         'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': len(inputText), 'top_p': 0.9,
                         'temperature': 0.8}

    else:
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': round(len(inputText) * 1.5),
                         'no_repeat_ngram_size': 1,
                         'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': len(inputText), 'top_p': 0.9,
                         'temperature': 0.99}

    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]
    (success, returnText) = queryTextGenerationOrText2Text(query, endpoint, headers)
    if success:
        return returnText

    print(returnText)
    return ""
