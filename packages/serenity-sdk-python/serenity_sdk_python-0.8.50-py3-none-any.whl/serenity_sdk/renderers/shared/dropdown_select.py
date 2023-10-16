
import ipywidgets
from typing import List, Optional


class DropdownSelectWidget:
    "This is a simple dropdown widget creater"

    def __init__(self, description: str, choices: List[str], default_choice: Optional[str] = None):
        """create a dropdown widget object

        Args:
            description (str): test shown in the widget
            choices (List[str]): list of choices to select
            default_choice (str, optional): the default choice. If None, set to the first choice in choices.
        """

        self.dropdown_widget = ipywidgets.Dropdown(
            options=choices,
            value=None,
            description=description,
            layout={'width': 'max-content'}
        )

        # set the default value
        if default_choice in choices:
            self.dropdown_widget.value = default_choice
        else:
            self.dropdown_widget.value = choices[0]

    @property
    def selected_choice(self) -> str:
        "selected choice value"
        return self.dropdown_widget.value
