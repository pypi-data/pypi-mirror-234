import json
import logging
import os
from typing import Any, Dict, List, Union

import torch

from exciton.ml.tagging.xlmroberta import Tagging_Model

from .utils import clean_result


class NER_Model(Tagging_Model):
    """NER Model

    Args:
        model_option (str, optional): model option. Defaults to None.
        path_to_model (str, optional): path to model directory. Defaults to "model".
        device (str, optional): device. Defaults to "cpu".
    """

    def __init__(
        self,
        model_option: str = None,
        path_to_model: str = "model",
        device: str = "cpu",
    ):
        HOME = os.path.expanduser("~")
        MODEL_DIR = "exciton/models/nlp/named_entity_recogonition"
        if model_option:
            self.path_to_model = f"{HOME}/{MODEL_DIR}/{model_option}"
        else:
            self.path_to_model = path_to_model
        label_file = "{}/labels.json".format(path_to_model)
        with open(label_file, "r") as fp:
            labels = json.load(fp)
        n_labels = len(labels)
        self.labels = labels
        self.n_labels = n_labels
        super().__init__(n_labels=n_labels, device=device)

        logging.disable(logging.INFO)
        logging.disable(logging.WARNING)
        self.build_modules()
        self._init_model_parameters()

    def _get_raw_results(
        self, batch_text: List[Union[str, Dict[str, Any]]], top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """Get raw results.

        Args:
            batch_text (List[Union[str, Dict[str, Any]]]): batch text input.
            top_n (int, optional): top-n. Defaults to 5.

        Returns:
            List[Dict[str, Any]]: output data.
        """
        assert isinstance(batch_text, List)
        batch_data = []
        for itm in batch_text:
            if not isinstance(itm, Dict):
                itm = {"text": " ".join(itm.split())}
            itm["text"] = " ".join(itm["text"].split())
            batch_data.append(itm)
        self._build_batch(batch_data)
        with torch.no_grad():
            logits = self._build_pipe()
            logits = torch.softmax(logits, dim=2)
        prob, labels = logits.topk(self.n_labels, dim=2)
        prob = prob.squeeze(2)
        prob = prob.data.cpu().numpy().tolist()
        labels = labels.squeeze(2)
        labels = labels.data.cpu().numpy().tolist()
        output = []
        for k, itm in enumerate(self.batch_data["input_data_raw"]):
            lname = [self.labels[lb[0]] for lb in labels[k]]
            itm["labels"] = lname[1:][: len(itm["etokens"])]
            lcand = []
            for arr in labels[k]:
                out = []
                for lb in arr[:top_n]:
                    out.append(self.labels[lb])
                lcand.append(out)
            lcand = lcand[1:][: len(itm["etokens"])]
            itm["cand_labels"] = lcand
            itm["cand_prob"] = [arr[:top_n] for arr in prob[k]]
            itm["cand_prob"] = itm["cand_prob"][1:][: len(itm["etokens"])]
            output.append(clean_result(itm))
        return output

    def predict(
        self, input_text: List[Union[str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Annotate texts.

        Args:
            input_text (list): input data.

        Returns:
            List[Dict[str, Any]]: output data.
        """
        if not isinstance(input_text, list):
            input_text = [input_text]
        batch_size = min(20, len(input_text))
        k = 0
        output = []
        while k * batch_size < len(input_text):
            batch_text = input_text[k * batch_size : (k + 1) * batch_size]
            results = self._get_raw_results(batch_text)
            for itm in results:
                out = {"text": itm["text"], "named_entities": itm["named_entities"]}
                output.append(out)
            k += 1
        return output
