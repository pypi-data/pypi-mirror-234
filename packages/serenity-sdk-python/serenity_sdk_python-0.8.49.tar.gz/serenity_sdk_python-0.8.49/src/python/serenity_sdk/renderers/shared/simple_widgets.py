"""
Module with simple widgets that can be used in the Serenity SDK.
"""
from typing import Any
import ipywidgets
from IPython.display import display


def display_in_hbox(content: Any, height: str = '300px', width='100%'):
    """
    Displays the given content in a horizontal box with the given height and width.
    For dataframes `df`, set `content=df.style` to get scrollable tables.
    """

    out = ipywidgets.Output()
    with out:
        display(content)
    display(ipywidgets.HBox([out], layout=ipywidgets.Layout(height=height, width=width)))
