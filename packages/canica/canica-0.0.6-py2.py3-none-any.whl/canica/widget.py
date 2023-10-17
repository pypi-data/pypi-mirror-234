import importlib.metadata
import pathlib
from typing import Optional

import anywidget
import pandas as pd
import traitlets

from canica.data import create_input_dict

try:
    __version__ = importlib.metadata.version("canica")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class CanicaWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # Data used by the widget
    data = traitlets.Dict().tag(sync=True)
    hue_col_name = traitlets.Unicode(allow_none=True).tag(sync=True)
    algo_name = traitlets.Unicode().tag(sync=True)

    def __init__(
        self,
        df: pd.DataFrame,
        embedding_col: str,
        text_col: Optional[str] = None,
        hue_col: Optional[str] = None,
    ) -> None:
        """Create a new widget.

        Args:
            df: DataFrame containing the text, embeddings, and hue_col
            embedding_col: Name of the column containing the embeddings
            text_col: Name of the column containing the text.
                If None, defaults to "text".
            hue_col: Name of the column containing the variable to color by.
                If None, no coloring is applied.
        """
        super().__init__()

        assert isinstance(embedding_col, str), "embeddings variable must be a string"
        assert text_col is None or isinstance(
            text_col, str
        ), "text_var variable must be a string"
        assert hue_col is None or isinstance(
            hue_col, str
        ), "hue_col variable must be a string"

        self.hue_col_name = hue_col
        if text_col is None:
            text_col = "text"

        # Represent data in the format expected by the widget. This is:
        # {
        #     text: { [key: string]: string };
        #     embeddings: { [key: string]: Vector };
        #     hue_var: { [key: string]: number };
        # }
        self.data = create_input_dict(
            df,
            embedding_col=embedding_col,
            text_col=text_col,
            hue_col=self.hue_col_name,
        )


class CanicaTSNE(CanicaWidget):
    def __init__(
        self,
        df: pd.DataFrame,
        embedding_col: str,
        text_col: Optional[str] = None,
        hue_col: Optional[str] = None,
    ) -> None:
        """
        Create a new canica widget using TSNE.

        Args:
            df: DataFrame containing the text, embeddings, and hue_col
            embedding_col: Name of the column containing the embeddings
            text_col: Name of the column containing the text.
                If None, defaults to "text".
            hue_col: Name of the column containing the variable to color by.
                If None, no coloring is applied.
        """
        super().__init__(
            df, embedding_col=embedding_col, text_col=text_col, hue_col=hue_col
        )
        self.algo_name = "TSNE"


class CanicaUMAP(CanicaWidget):
    def __init__(
        self,
        df: pd.DataFrame,
        embedding_col: str,
        text_col: Optional[str] = None,
        hue_col: Optional[str] = None,
    ) -> None:
        """
        Create a new canica widget using UMAP.

        Args:
            df: DataFrame containing the text, embeddings, and hue_col
            embedding_col: Name of the column containing the embeddings
            text_col: Name of the column containing the text.
                If None, defaults to "text".
            hue_col: Name of the column containing the variable to color by.
                If None, no coloring is applied.
        """
        super().__init__(
            df, embedding_col=embedding_col, text_col=text_col, hue_col=hue_col
        )
        self.algo_name = "UMAP"
