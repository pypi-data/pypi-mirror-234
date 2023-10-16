from llm_guard.util import device, lazy_load_dep, logger

from .base import Scanner

_model_path = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
_categories = ["refusal"]


class NoRefusal(Scanner):
    """
    A class used to detect and handle refusals in language model output.

    This class uses the zero-shot-classification model from Hugging Face to classify refusals.

    Refusals are common when the prompt breaches policies defined by the model.
    """

    def __init__(self, threshold: float = 0.5):
        """
        Initializes an instance of the NoRefusal class.

        Parameters:
            threshold (float): The similarity threshold to consider an output as refusal.
        """

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

        classifier_output = self._classifier(output, _categories, multi_label=False)

        max_score = round(max(classifier_output["scores"]) if classifier_output["scores"] else 0, 2)
        if max_score > self._threshold:
            logger.warning(f"Detected refusal result with similarity score: {max_score}")

            return output, False, max_score

        logger.debug(f"No refusals. Max similarity with the known refusal results: {max_score}")

        return output, True, 0.0
