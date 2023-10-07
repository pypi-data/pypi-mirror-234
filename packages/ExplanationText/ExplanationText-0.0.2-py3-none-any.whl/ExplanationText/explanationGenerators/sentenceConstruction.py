def generate_explanation_with_sentence_construction(singleObject):
    """
    Main method for explanation with sentence construction
    Current version:
        'Object in image was classified as a <main label> with <percentage>% certainty.
        The <main label> was mainly classified that way, because of the <part label>
        with <percentage>% relevance at position <position> , <more part labels> ... and <last part label>'
    """
    explanation = ""
    if len(singleObject) < 1:
        return explanation

    # main label sentence
    explanation += generate_main_label_explanation(singleObject)

    # part labels sentence
    if 'parts' not in singleObject:
        return explanation[:-1]
    explanation += generate_part_label_explanation(singleObject)

    return explanation


def generate_main_label_explanation(singleObject):
    """
    Method to construct main label sentence
    """

    mainLabel = singleObject.get('label')
    explanation = "Object in image was classified as a " + mainLabel

    # main label percentage
    if 'probability' in singleObject:
        mainLabelPercentage = singleObject.get('probability')
        explanation += " with " + str(mainLabelPercentage) + "% certainty. "
    else:
        return explanation + "."

    return explanation


def generate_part_label_explanation(singleObject):
    """
    Method to construct part label sentence
    """

    # get main label
    if 'label' in singleObject:
        mainLabel = singleObject.get('label')
    else:
        mainLabel = "object"

    # Start of the second sentence
    explanation = "The " + str(mainLabel) + " was mainly classified that way, because of the "

    # sentence part for each part label
    for part in singleObject.get('parts'):

        partLabel = part.get('partLabel')

        # add part label
        explanation += str(partLabel)

        # optionally add relevance and position if given in sample
        if 'relevance' in part:
            relevance = part.get('relevance')
            explanation += " with " + str(relevance) + "% relevance"

        explanation += ", "

    # fix format of last part explanation and return explanation
    return format_explanation(explanation, singleObject)


def format_explanation(explanation, singleObject):
    """
    Method fix format issues with last part explanation sentence.
    Add dot at the end and replace last comma with 'and'.
    """
    if explanation.endswith(" "):
        explanation = explanation[:-2] + "."

    if 'parts' in singleObject:
        last_comma_index = explanation.rfind(",")
        explanation = explanation[:last_comma_index] + " and" + explanation[last_comma_index + 1:]

    return explanation


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        return str(round(float(a) * 100))
    except ValueError:
        return "0.0"
