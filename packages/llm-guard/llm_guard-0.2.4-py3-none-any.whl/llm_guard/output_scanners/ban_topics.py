from typing import List

from llm_guard.util import device, lazy_load_dep, logger

from .base import Scanner

_model_path = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"


class BanTopics(Scanner):
    """
    A text scanner that checks whether the generated text output includes banned topics.

    The class uses the zero-shot-classification model from Hugging Face to scan the topics present in the text.
    """

    def __init__(self, topics=List[str], threshold: float = 0.75):
        """
        Initializes BanTopics with a list of topics and a probability threshold.

        Parameters:
            topics (List[str]): The list of topics to be banned from the text.
            threshold (float): The minimum probability required for a topic to be considered present in the text.
                               Default is 0.75.

        Raises:
            ValueError: If no topics are provided.
        """
        if len(topics) == 0:
            raise ValueError("No topics provided")

        self._topics = topics
        self._threshold = threshold

        transformers = lazy_load_dep("transformers")
        self._classifier = transformers.pipeline(
            "zero-shot-classification",
            model=_model_path,
            device=device(),
        )
        logger.debug(f"Initialized model {_model_path} on device {device()}")

    def scan(self, prompt: str, output: str) -> (str, bool, float):
        if output.strip() == "":
            return output, True, 0.0

        if len(self._topics) == 0:
            raise ValueError("No topics provided")

        classifier_output = self._classifier(output, self._topics, multi_label=False)

        max_score = round(max(classifier_output["scores"]) if classifier_output["scores"] else 0, 2)
        if max_score > self._threshold:
            logger.warning(
                f"Topics detected for the prompt {classifier_output['labels']} with scores: {classifier_output['scores']}"
            )

            return output, False, max_score

        logger.debug(
            f"No banned topics detected ({classifier_output['labels']}, scores: {classifier_output['scores']})"
        )

        return output, True, 0.0
