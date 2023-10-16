# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import importlib.util as mprt
import sys as sstm
from os import sep as PATH_SEPARATOR
from pathlib import Path as path_t
from types import ModuleType
from typing import Any, Callable, Protocol, TypeVar

button_wgt_h = TypeVar("button_wgt_h")
choices_dots_wgt_h = TypeVar("choices_dots_wgt_h")
choices_list_wgt_h = TypeVar("choices_list_wgt_h")
color_h = TypeVar("color_h")
grid_lyt_h = TypeVar("grid_lyt_h")
group_wgt_h = TypeVar("group_wgt_h")
hbox_lyt_h = TypeVar("hbox_lyt_h")
label_wgt_h = TypeVar("label_wgt_h")
library_wgt_h = TypeVar("library_wgt_h")
menu_wgt_h = TypeVar("menu_wgt_h")
paragraph_wgt_h = TypeVar("paragraph_wgt_h")
scroll_container_h = TypeVar("scroll_container_h")
stack_wgt_h = TypeVar("stack_wgt_h")
tabs_wgt_h = TypeVar("tabs_wgt_h")
text_wgt_h = TypeVar("text_wgt_h")
vbox_lyt_h = TypeVar("vbox_lyt_h")


class backend_p(Protocol):
    ALIGNED_CENTER: Any
    ALIGNED_HCENTER: Any
    ALIGNED_LEFT: Any
    ALIGNED_RIGHT: Any
    ALIGNED_TOP: Any
    BASE_PALETTE: Any
    DIALOG_ACCEPTATION: Any
    DIALOG_ACCEPT_OPEN: Any
    DIALOG_ACCEPT_SAVE: Any
    DIALOG_AUTO_OVERWRITE: Any
    DIALOG_MODE_ANY: Any
    DIALOG_MODE_EXISTING_FILE: Any
    DIALOG_MODE_FOLDER: Any
    FORMAT_RICH: Any
    LINE_NO_WRAP: Any
    SELECTABLE_TEXT: Any
    SIZE_EXPANDING: Any
    SIZE_FIXED: Any
    SIZE_MINIMUM: Any
    TAB_POSITION_EAST: Any
    WIDGET_TYPE: Any
    WORD_NO_WRAP: Any

    Color: Callable[[str], color_h]

    qt_core_app_t: Any
    event_loop_t: Any

    library_wgt_t: library_wgt_h

    button_wgt_t: button_wgt_h
    choice_menu_wgt_t: choices_list_wgt_h
    dot_button_wgt_t: library_wgt_h
    group_wgt_t: group_wgt_h
    label_wgt_t: label_wgt_h
    menu_wgt_t: menu_wgt_h
    paragraph_wgt_t: paragraph_wgt_h
    path_chooser_wgt_t: library_wgt_h
    scroll_container_t: scroll_container_h
    stack_wgt_t: stack_wgt_h
    tabs_wgt_t: tabs_wgt_h
    text_wgt_t: text_wgt_h

    hbox_lyt_t: hbox_lyt_h
    vbox_lyt_t: vbox_lyt_h
    grid_lyt_t: grid_lyt_h

    ShowErrorMessage: Callable[..., None]
    ShowMessage: Callable[..., None]


@dtcl.dataclass(repr=False, eq=False)
class backend_t(backend_p):
    name: str

    def __post_init__(self) -> None:
        """"""
        base_path = path_t(__file__).parent
        package_path = base_path.parent
        path = base_path / "backend" / self.name
        if not path.is_dir():
            raise ValueError(f"Invalid backend folder: {path}.")

        standard_modules = set(sstm.stdlib_module_names).union(
            sstm.builtin_module_names
        )
        for node in path.rglob("*.py"):
            if node.is_file():
                relative = node.relative_to(package_path)
                name = str(relative.parent / relative.stem).replace(PATH_SEPARATOR, ".")
                spec = mprt.spec_from_file_location(name, node)
                module = mprt.module_from_spec(spec)
                sstm.modules[name] = module
                spec.loader.exec_module(module)

                for name in dir(module):
                    if name[0] == "_":
                        continue

                    element = getattr(module, name)
                    if not (
                        isinstance(element, ModuleType)
                        or (element.__module__[0] == "_")
                        or (element.__module__ in standard_modules)
                    ):
                        setattr(self, name, element)
