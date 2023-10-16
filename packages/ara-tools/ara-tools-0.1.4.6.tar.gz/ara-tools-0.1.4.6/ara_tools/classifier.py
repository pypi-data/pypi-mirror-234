class Classifier:

    valid_classifiers = {
        "vision": "vision",
        "businessgoal": "goals",
        "capability": "capabilities",
        "keyfeature": "keyfeatures",
        "feature": "features",
        "epic": "epics",
        "story": "stories",
        "task": "tasks",
        "tasklist": "tasks",
        "example": "examples",
    }
    
    classifier_order = [
        "vision",
        "businessgoal",
        "capability",
        "keyfeature",
        "epic",
        "story",
        "example",
        "feature",
        "task",
        "tasklist",
        "issue",
    ]

    @staticmethod
    def get_sub_directory(classifier):
        return Classifier.valid_classifiers.get(classifier)

    @staticmethod
    def is_valid_classifier(classifier):
        return classifier in Classifier.valid_classifiers

    @staticmethod
    def ordered_classifiers():
        return Classifier.classifier_order
