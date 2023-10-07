def generate_explanation_with_overview(image, objectList):
    """
    Main method for explanation with overview
    Current version:
        'This image contains a <mainLabel>, a <mainLabel>, ... and a <mainLabel>'
    """

    explanation = ""
    if len(objectList) < 1:
        return explanation

    explanation = "This image contains"

    # Case for one object
    if len(objectList) == 1:
        explanation += " a " + objectList[0]+"."

    # Case for multiple objects
    else:
        lastObject = objectList[-1]
        for objectLabel in objectList[0:-1]:
            explanation += " a " + objectLabel + ","

        # add last object and dot
        explanation = explanation[:-1] + " and a " + lastObject + "."

    return explanation