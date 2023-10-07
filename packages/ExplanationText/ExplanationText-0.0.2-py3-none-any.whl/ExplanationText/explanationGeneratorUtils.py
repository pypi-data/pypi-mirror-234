"""
File with general utility functions for the explanation generator
"""


def validateAndParseImage(image, minimumRelevance, maximumPartCount):
    """
    Function to parse, validate and sort content of labels dictionary
    """
    if 'objects' not in image or image.get('objects') == "":
        return [], []

    objectList = []
    newObjects = []
    objects = image.get('objects')
    all_probabilities_given = True

    for singleObject in objects:

        if 'label' not in singleObject or singleObject.get('label') == "":
            break

        objectList.append(singleObject.get('label'))
        if 'probability' in singleObject:
            singleObject.update({'probability': float_to_percentage(singleObject.get('probability'))})
        else:
            all_probabilities_given = False

        if 'parts' not in singleObject:
            break

        if 'heatmap' in singleObject:
            del singleObject['heatmap']

        if 'parts' not in singleObject or len(singleObject.get('parts')) < 1:
            singleObject.pop('parts')
        else:
            # parse part labels
            parts = singleObject.get('parts')
            sortedParts = []
            for part in parts:
                if 'labels' in part and singleObject.get('label') in part.get('labels') \
                        and len(part.get('labels').get(singleObject.get('label'))) > 0:
                    newPart = {"partLabel": part.get('labels').get(singleObject.get('label'))[0]}
                    if 'relevancy' in part:
                        try:
                            # Check if relevance is greater than minimum relevance
                            relevance = float_to_percentage(part.get('relevancy'))
                            if relevance >= minimumRelevance:
                                newPart.update({'relevance': relevance})
                                sortedParts.append(newPart)
                        except ValueError:
                            print(str(part.get(
                                'relevance') + " is not a valid value for relevance in object " + singleObject.get(
                                'label')))
                    else:
                        sortedParts.append(newPart)
                else:
                    print(part.get('labels'))

            # Sort part labels
            sortedParts = sorted(sortedParts, key=lambda d: d['relevance'], reverse=True)
            if len(sortedParts) > 0:
                singleObject.update({'parts': sortedParts[:maximumPartCount]})
            else:
                singleObject.pop('parts')

        newObjects.append(singleObject)

    if all_probabilities_given:
        # Sort objects
        sortedObjects = sorted(newObjects, key=lambda d: d['probability'], reverse=True)
        return objectList, sortedObjects
    else:
        return objectList, newObjects


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        if 0 < a < 1:
            return round(float(a) * 100)
        else:
            return 100
    except ValueError:
        return 0
