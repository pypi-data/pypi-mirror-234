from typing import List, Union

import pandas as pd


def build_dict_from_columns(
    ids: pd.Index,
    text: pd.Series,
    embeddings: List[List],
    hue: Union[pd.Series, None] = None,
) -> dict:
    """Output a dictionary with the desired columns for the widget.
    The type of the input dictionary is:
        { text: { [key: string]: string };
        embeddings: { [key: string]: Vector };
        hue_var: { [key: string]: number }; }
    """
    final_dict = {}
    final_dict["text"] = {id: txt for id, txt in zip(ids, text)}
    final_dict["embeddings"] = {id: emb for id, emb in zip(ids, embeddings)}
    if hue is not None:
        final_dict["hue_var"] = {id: h for id, h in zip(ids, hue)}
    return final_dict


def create_input_dict(
    df: pd.DataFrame,
    embedding_col: str,
    text_col: str,
    hue_col: Union[str, None] = None,
) -> dict[str, dict]:
    """
    Create a dictionary in the desired format for the widget.

    Args:
        df: DataFrame containing the text, embeddings, and hue_col.
        embedding_col: Name of the column containing the embeddings.
        text_col: Name of the column containing the text.
        hue_col: Name of the column containing the variable to color by.
            If None, no coloring is applied.
    """
    # Check that the desired columns are in the DataFrame.
    assert embedding_col in df.columns, "embeddings variable not in DataFrame"
    assert text_col in df.columns, "text variable not in DataFrame"
    assert hue_col is None or hue_col in df.columns, "hue_col not in DataFrame"
    # If the DataFrame doesn't have a unique index it leads to issues.
    assert df.index.is_unique, "Elements of the input DataFrame's index must be unique"

    # Extract desired columns from DataFrame
    _ids = df.index
    _text = df[text_col]
    _embeddings = [list(emb) for emb in df[embedding_col]]
    if hue_col is not None:
        _hue = df[hue_col]
        assert pd.api.types.is_string_dtype(_hue) or pd.api.types.is_numeric_dtype(
            _hue
        ), f"hue_col ({hue_col}) column must be either string or numeric"
    else:
        _hue = None

    # Build dictionary in the right format
    return build_dict_from_columns(
        ids=_ids, text=_text, embeddings=_embeddings, hue=_hue
    )
