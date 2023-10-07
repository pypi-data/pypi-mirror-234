import json
import os
from typing import Any, Dict, List, Union

import spacy


class Spacy_NER(object):
    """Spacy NER wrapper."""

    def __init__(self) -> None:
        HOME = os.path.expanduser("~")
        MODEL_DIR = "exciton/models/nlp/named_entity_recognition/spacy"
        with open(f"{HOME}/{MODEL_DIR}/support_languages.json") as fp:
            self.support_languages = json.load(fp)
        self.worker = {}
        for lang in self.support_languages:
            self.worker[lang["code"]] = spacy.load(lang["spacy"])

    def get_support_languages(self) -> List[Dict[str, Any]]:
        """Get support languages.

        Returns:
            List[Dict[str, Any]]: List of languages.
        """
        langs = [
            {"code": itm["code"], "name": itm["name"]} for itm in self.support_languages
        ]
        return langs

    def predict(
        self, input_data: List[Union[str, Dict[str, Any]]], source_lang: str
    ) -> List[Dict[str, Any]]:
        """Begin to work.

        Args:
            source (str): Source text.
            source_lang (str): source language.

        Returns:
            List[str]: List of sentences.
        """
        output = []
        for itm in input_data:
            if isinstance(itm, str):
                itm = {"text": itm}
            docs = self.worker[source_lang](itm)
            for token in docs.ents:
                print(token, token.start_char, token.end_char, token.label_)
        return
