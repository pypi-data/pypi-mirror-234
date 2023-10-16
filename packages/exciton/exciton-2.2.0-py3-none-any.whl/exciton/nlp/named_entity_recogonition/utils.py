from typing import Any, Dict, List

import numpy as np


def collect_named_entities(tokens: List[str]) -> List[Dict[str, Any]]:
    """Creates a list of entity named-tuples storing the entity type and the start and end offsets of the entity.

    Args:
        tokens (List[str]): input data.

    Returns:
        List[Dict[str, Any]]: output entities.
    """
    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None
    for offset, token_tag in enumerate(tokens):
        if token_tag == "O":
            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append(
                    {"label": ent_type, "start": start_offset, "end": end_offset}
                )
                start_offset = None
                end_offset = None
                ent_type = None
        elif ent_type is None:
            ent_type = token_tag[2:]
            start_offset = offset
        elif ent_type != token_tag[2:] or (
            ent_type == token_tag[2:] and token_tag[:1] == "B"
        ):
            end_offset = offset - 1
            named_entities.append(
                {"label": ent_type, "start": start_offset, "end": end_offset}
            )
            # start of a new entity
            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    # catches an entity that goes up until the last token
    if ent_type is not None and start_offset is not None and end_offset is None:
        named_entities.append(
            {"label": ent_type, "start": start_offset, "end": len(tokens) - 1}
        )
    return named_entities


def clean_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Clean the named entities recogonition results.

    Args:
        result (Dict[str, Any]): input

    Returns:
        Dict[str, Any]: output
    """
    text = result["text"]
    tokens = result["etokens"]
    labels = result["labels"]
    cand_labels = result["cand_labels"]
    cand_prob = result["cand_prob"]
    named_entities = collect_named_entities(labels)

    token_labels = []
    i = 0
    for j, wd in enumerate(tokens):
        wdlen = len(wd)
        if wd[:2] == "##":
            wdlen -= 2
        if wd[:1] == "▁":
            wdlen -= 1
        while i < len(text):
            if text[i] == " ":
                i += 1
            else:
                break
        span = [i, i + wdlen]
        i += wdlen
        token_labels.append(
            {
                "token": wd,
                "span": span,
                "label": labels[j],
                "cand_labels": cand_labels[j],
                "cand_prob": np.around(cand_prob[j], 4).tolist(),
            }
        )
    entities = []
    for itm in named_entities:
        span = [
            token_labels[itm["start"]]["span"][0],
            token_labels[itm["end"]]["span"][1],
        ]
        entities.append(
            {"label": itm["label"], "text": text[span[0] : span[1]], "span": span}
        )
    return {
        "text": text,
        "tokens": tokens,
        "named_entities": entities,
        "token_labels": token_labels,
    }
