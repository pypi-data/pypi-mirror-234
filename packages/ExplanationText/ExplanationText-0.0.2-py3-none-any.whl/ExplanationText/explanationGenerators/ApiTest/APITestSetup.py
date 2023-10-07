import random

from ExplanationText.explanationGenerators.sentenceConstruction import generate_explanation_with_sentence_construction


def getRunConfiguration(singleObject):
    prompt = generate_explanation_with_sentence_construction(singleObject)
    if 'parts' in singleObject:
        for part in singleObject['parts']:
            connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
            prompt += f"{part['partLabel']} is {connection} connected to " + singleObject['label'] + ". "

    # Text Generation
    aModels = ["prithivida/parrot_paraphraser_on_T5", "ramsrigouthamg/t5_sentence_paraphraser"]
    aConfig = {'num_return_sequences': 3, 'min_new_tokens': 250, 'no_repeat_ngram_size': 3, 'max_time': 120.0,
               'num_beams': 3, 'do_sample': True, 'top_k': len(prompt), 'top_p': 0.9, 'temperature': 0.9}
    aPrompt = prompt

    bModels = ["bigscience/bloom", "EleutherAI/gpt-neox-20b"]
    bConfig = {'return_full_text': False, 'num_return_sequences': 3, 'max_new_tokens': len(prompt),
               'no_repeat_ngram_size': 3,
               'max_time': 120.0, 'num_beams': 3, 'do_sample': True, 'top_k': len(prompt), 'top_p': 0.9,
               'temperature': 0.9}
    bPrompt = "Rephrase the sentence. Sentence: " + prompt + " Rephrase:"

    cModels = ["OpenAssistant/oasst-sft-1-pythia-12b"]
    cConfig = {'return_full_text': False, 'num_return_sequences': 1, 'max_new_tokens': len(prompt),
               'no_repeat_ngram_size': 1,
               'max_time': 120.0, 'num_beams': 1, 'do_sample': True, 'top_k': len(prompt), 'top_p': 0.9,
               'temperature': 0.9}
    cPrompt = "<|prompter|>Paraphrase the following sentence: " + prompt + ".<|endoftext|><|assistant|>"

    testA = ["TG_A", aModels, ["text-generation"], [aPrompt, aPrompt, aPrompt], aConfig]
    testB = ["TG_B", bModels, ["text-generation"], [bPrompt, bPrompt, bPrompt], bConfig]
    testC = ["TG_C", cModels, ["text-generation"], [cPrompt, cPrompt], cConfig]

    # Summarization
    dModels = ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6", "philschmid/bart-large-cnn-samsum",
               "moussaKam/barthez-orangesum-abstract", "google/pegasus-cnn_dailymail", "google/pegasus-xsum",
               "google/bigbird-pegasus-large-bigpatent", "csebuetnlp/mT5_multilingual_XLSum",
               "pszemraj/led-base-book-summary", "slauw87/bart_summarisation", "google/pegasus-large", "facebook/bart"
                                                                                                       "-large-xsum"]
    dConfig = {'min_length': round(len(prompt) * 0.75), 'max_length': round(len(prompt) * 1.25),
               'max_time': 120.0}
    dPrompt = prompt
    testD = ["SUM", dModels, ["summarization"], [dPrompt], dConfig]

    tests = [testC]

    return tests


demoSample = []


def getParts(s, p):
    pass


# ---- Examples for tasks -----

# Test Fill Mask (has to contain [MASK]
test_b_models = ["microsoft/deberta-base", "bert-base-uncased"]
test_b_tasks = ["fillMask"]
test_b_prompts = []
for sample in demoSample:
    test_b_prompts.extend([f"The Objects {getParts(sample, 2)} are [MASK]."])
test_b_configuration = {}
test_b = ["FillMask_Test_", test_b_models, test_b_tasks, test_b_prompts, test_b_configuration]

# Test Conversational (Each prompt will is next conversation piece)
test_c_models = ["microsoft/DialoGPT-large"]
test_c_tasks = ["conversational"]
test_c_prompts = []
for sample in demoSample:
    test_c_prompts.extend(
        [f"An image was classified by a neural network as a {sample.get('mainLabel')}. Explain the classification.",
         f"How did you came up with this explanation?"])
test_c_configuration = {"max_time": 120.0}
test_c = ["Conversational_", test_c_models, test_c_tasks, test_c_prompts, test_c_configuration]

# Test Summarization (empty configuration)
test_d_models = ["facebook/bart-large-cnn", "philschmid/bart-large-cnn-samsum"]
test_d_tasks = ["summarization"]
test_d_prompts = []
for sample in demoSample:
    test_d_prompts.extend([f"An image was classified by a neural network as a {sample.get('mainLabel')}. The "
                           f"reason for this classification is ",
                           f"Image Classification of {sample.get('mainLabel')} with neural networks work the "
                           f"following way"])
test_d = ["Summarization_", test_d_models, test_d_tasks, test_d_prompts, {}]

runTest = [test_b, test_c, test_d]

# ---- End of Examples-----
