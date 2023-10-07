import json
import os
import re
from typing import Any, Dict, List

import pysbd
from sentence_splitter import SentenceSplitter


class Exciton_SBD(object):
    """Customized Sentence Boundary Disambiguation.

    Note:
        This is not a standard SBD. The goal is to split text into small pieces.

    Args:
        language (str): language.
        path_to_model (str, optional): path to model. Defaults to None.
    """

    def __init__(self, language: str, path_to_model: str = None) -> None:
        if path_to_model is None:
            HOME = os.path.expanduser("~")
            MODEL_DIR = "exciton/models/nlp/sentence_tokenizer/exciton_sbd"
            path_to_model = f"{HOME}/{MODEL_DIR}"
        with open(f"{path_to_model}/exciton_eos.json") as fp:
            self.eos = json.load(fp)
        self.pattern = re.compile("|".join(self.eos[language]))

    def split(self, text: str) -> List[str]:
        """Split Text.

        Args:
            text (str): Source text.

        Returns:
            List[str]: List of sentences.
        """
        sents = []
        last_pos = 0
        for itm in self.pattern.finditer(text):
            if itm.span()[1] < len(text):
                wd = text[itm.span()[1]]
                if wd != " ":
                    continue
            sen = text[last_pos : itm.span()[1]].strip()
            sents.append(sen)
            last_pos = itm.span()[1]
        if last_pos < len(text):
            sen = text[last_pos:].strip()
            sents.append(sen)
        return sents


class Sentence_Tokenizer(object):
    """Sentence Tokenizer.

    Args:
        path_to_model (str, optional): _description_. Defaults to None.

    Note:
        This is not a standard SBD. The goal is to split text into small pieces.
    """

    def __init__(self, path_to_model: str = None) -> None:
        if path_to_model is None:
            HOME = os.path.expanduser("~")
            MODEL_DIR = "exciton/models/nlp/sentence_tokenizer/exciton_sbd"
            path_to_model = f"{HOME}/{MODEL_DIR}"
        with open(f"{path_to_model}/support_languages.json") as fp:
            self.support_languages = json.load(fp)
        self.worker = {}
        lang_pysbd = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "pysbd"
        ]
        for lang in lang_pysbd:
            self.worker[lang] = pysbd.Segmenter(language=lang, clean=False).segment
        lang_ss = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "sentsplit"
        ]
        for lang in lang_ss:
            self.worker[lang] = SentenceSplitter(language=lang).split
        lang_exciton = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "exciton"
        ]
        for lang in lang_exciton:
            self.worker[lang] = Exciton_SBD(
                language=lang, path_to_model=path_to_model
            ).split

    def get_support_languages(self) -> List[Dict[str, Any]]:
        """Get support languages.

        Returns:
            List[Dict[str, Any]]: List of languages.
        """
        langs = [
            {"code": itm["code"], "name": itm["name"]} for itm in self.support_languages
        ]
        return langs

    def predict(self, source: str, source_lang: str = None) -> List[str]:
        """Begin to work.

        Args:
            source (str): Source text.
            source_lang (str): source language.

        Returns:
            List[str]: List of sentences.
        """
        if source_lang is None or source_lang not in self.support_languages:
            source_lang = "unk"
        output = []
        for seg in source.split("\n"):
            out = []
            for sen in self.worker[source_lang](seg):
                if len(out) > 0 and len(out[-1]) < 10:
                    out[-1] += " " + sen.strip()
                else:
                    out.append(sen.strip())
            output.extend(out)
        return output
