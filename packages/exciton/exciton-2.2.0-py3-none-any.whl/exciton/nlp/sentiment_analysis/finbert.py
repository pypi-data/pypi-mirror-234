import json
import os
from typing import Any, Dict, List

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


class Finbert_Model(object):
    def __init__(
        self,
        path_to_model: str = None,
        device: str = "cpu",
    ) -> None:
        self.path_to_model = path_to_model
        self.device = torch.device(device)
        self.train_modules = {}
        self.base_modules = {}
        self.batch_data = {}

        if self.path_to_model is None:
            HOME = os.path.expanduser("~")
            MODEL_DIR = "exciton/models/nlp/sentiment_analysis"
            model = "finbert"
            path_to_model = f"{HOME}/{MODEL_DIR}/{model}"
            self.path_to_model = path_to_model
        label_file = f"{path_to_model}/models/config.json"
        with open(label_file, "r") as fp:
            labels = json.load(fp)["id2label"]
        self.labels = labels
        self.n_classes = len(labels)
        finbert = AutoModelForSequenceClassification.from_pretrained(
            f"{path_to_model}/models", num_labels=self.n_classes
        )
        tokenizer = AutoTokenizer.from_pretrained(f"{path_to_model}/tokenizer")
        self.nlp = pipeline(
            "sentiment-analysis", model=finbert, tokenizer=tokenizer, device=device
        )

    def predict(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sentiment Analysis Finbert.

        Args:
            input_data (List[Dict[str, Any]]): Input data.

        Returns:
            List[Dict[str, Any]]: Output.
        """
        batch_size = min(50, len(input_data))
        k = 0
        output = []
        while k * batch_size < len(input_data):
            batch_data = input_data[k * batch_size : (k + 1) * batch_size]
            batch_text = [sen["text"] for sen in batch_data]
            results = self.nlp(batch_text)
            for t, out in enumerate(results):
                out["text"] = batch_data[t]["text"]
                output.append(out)
            k += 1
        return output
