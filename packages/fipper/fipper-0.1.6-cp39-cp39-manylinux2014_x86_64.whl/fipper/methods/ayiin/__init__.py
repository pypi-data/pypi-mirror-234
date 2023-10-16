from .build_button import BuildButton
from .button_parser import ButtonParser
from .tools import AyiinTools


class Ayiin(
    AyiinTools,
    BuildButton,
    ButtonParser
):
    pass
