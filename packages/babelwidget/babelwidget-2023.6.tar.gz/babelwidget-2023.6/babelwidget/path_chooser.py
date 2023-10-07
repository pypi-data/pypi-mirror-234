# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
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

from pathlib import Path as path_t
from typing import Callable, Literal, Sequence, TypeVar

from babelwidget.main import backend_t

"""
valid_types: {"Type": "extension", "Type": ("extension", "extension",...), ...}
filter: "Image files (*.png *.xpm *.jpg);Text files (*.txt);Any files (*)"
"""


path_chooser_wgt_h = TypeVar("path_chooser_wgt_h")
valid_types_h = dict[str, str | Sequence[str]]
document_selection_fct_h = Callable[..., path_t | None]


def NewSelectedInputDocument(
    title: str,
    caption: str,
    backend: backend_t,
    /,
    *,
    mode: Literal["any", "document", "folder"] = "any",
    valid_types: valid_types_h = None,
    start_folder: str | path_t = None,
    initial_selection: str | path_t = None,
) -> path_t | None:
    """"""
    extension_filter, _ = _AllowedTypesElements(valid_types)
    check_existence = False
    if mode == "document":
        dialog_mode = backend.DIALOG_MODE_EXISTING_FILE
    elif mode == "folder":
        dialog_mode = backend.DIALOG_MODE_FOLDER
    else:
        # TODO: Check if that allows to select a folder (documentation says "The name of
        #     a file, whether it exists or not."). So a priori, no. But then how can we
        #     allow selection of either a file or a folder?
        dialog_mode = backend.DIALOG_MODE_ANY
        check_existence = True

    while True:
        dialog = _GenericDocumentDialog(
            title, caption, extension_filter, start_folder, initial_selection, backend
        )
        dialog.setAcceptMode(backend.DIALOG_ACCEPT_OPEN)
        dialog.setFileMode(dialog_mode)

        output = _SelectedDocument(dialog, backend)
        if output is None:
            return None
        if check_existence and not output.exists():
            backend.ShowErrorMessage(f"{output}: Nonexistent file or folder")
            start_folder = _StartFolderFromFolder(output)
            initial_selection = None
        else:
            # The file dialog does not allow to select either a file or a folder. So the
            # solution here is to select a file, and if a folder was needed, take the
            # parent.
            if (mode == "folder") and output.is_file():
                output = output.parent
            return output


def NewSelectedOutputDocument(
    title: str,
    caption: str,
    backend: backend_t,
    /,
    *,
    mode: Literal["any", "document", "folder"] = "any",
    valid_types: valid_types_h = None,
    auto_overwrite: bool = False,
    start_folder: str | path_t = None,
    initial_selection: str | path_t = None,
) -> path_t | None:
    """"""
    extension_filter, allowed_extensions = _AllowedTypesElements(valid_types)
    while True:
        dialog = _GenericDocumentDialog(
            title, caption, extension_filter, start_folder, initial_selection, backend
        )
        dialog.setAcceptMode(backend.DIALOG_ACCEPT_SAVE)
        dialog.setFileMode(backend.DIALOG_MODE_ANY)
        if auto_overwrite:
            dialog.setOption(backend.DIALOG_AUTO_OVERWRITE)

        output = _SelectedDocument(dialog, backend)
        if output is None:
            return None
        # The file dialog does not allow to select either a file or a folder. So the solution here is to select a file,
        # and if a folder was needed, take the parent. See (*) below.
        if (mode == "folder") and output.exists() and output.is_file():
            output = output.parent

        erroneous_selection = False
        if output.exists():
            if (mode == "document") and not output.is_file():
                backend.ShowErrorMessage(f"{output}: Not of regular file")
                erroneous_selection = True
            # Unnecessary due to (*) above
            # elif (mode == "folder") and not output.is_dir():
            #     ShowErrorMessage(f"{output}: Not a folder")
            #     erroneous_selection = True

        if not erroneous_selection:
            if ("*" in allowed_extensions) or (
                output.suffix.lower()[1:] in allowed_extensions
            ):
                return output
            else:
                backend.ShowErrorMessage(f"{output}: Extension is not valid")

        start_folder = _StartFolderFromFolder(output)
        initial_selection = None


def _AllowedTypesElements(
    valid_types: valid_types_h | None, /
) -> tuple[str, tuple[str]]:
    """"""
    if valid_types is None:
        return "Any file or folder (*)", ("*",)

    types = []
    extensions = []
    filters = []
    for _type, extension in valid_types.items():
        types.append(_type)
        if isinstance(extension, str):
            extensions.append(extension)
            if extension == "*":
                new_extensions = ("*",)
            else:
                new_extensions = (f"*.{extension}",)
        else:
            extensions.extend(extension)
            new_extensions = tuple(f"*.{_ext}" for _ext in extension)
        filters.append(f"{_type.title()} ({' '.join(new_extensions)})")

    return ";".join(filters), tuple(extensions)


def _StartFolderFromFolder(folder: path_t, /) -> path_t | None:
    """"""
    output = folder

    root = folder.root
    while (output != root) and (not output.exists()):
        output = output.parent
    if output == root:
        output = None

    return output


def _GenericDocumentDialog(
    title: str,
    caption: str,
    extension_filter: str,
    start_folder: str | path_t,
    initial_selection: str | path_t,
    backend: backend_t,
    /,
) -> path_chooser_wgt_h:
    """"""
    output = backend.path_chooser_wgt_t(caption, extension_filter=extension_filter)
    output.setWindowTitle(title)
    if start_folder is not None:
        output.setDirectory(str(start_folder))
    if initial_selection is not None:
        output.selectFile(str(initial_selection))

    return output


def _SelectedDocument(
    dialog: path_chooser_wgt_h, backend: backend_t, /
) -> path_t | None:
    """"""
    status = dialog.RunAndGetClosingStatus()
    if status == backend.DIALOG_ACCEPTATION:
        return path_t(dialog.SelectedFile())

    return None
