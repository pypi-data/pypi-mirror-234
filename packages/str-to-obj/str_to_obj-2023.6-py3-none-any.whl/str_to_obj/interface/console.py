# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2023)
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

from typing import Any, Sequence


def TypeAsRichStr(value: Any, /, *, prefix: str = "") -> str:
    """
    Richer alternative (however, causes troubles with packages like TensorFlow):
    Additional parameter: relative_to_home: bool = True
    from conf_ini_g.extension.python import SpecificationPath
    return (
        f"[bold magenta]{type(instance).__name__}[/]"
        f"[gray]@"
        f"{SpecificationPath(type(instance), relative_to_home=relative_to_home)}:[/]"
    )
    """
    return f"[yellow]{prefix}{type(value).__name__}[/]"


def NameValueTypeAsRichStr(name: str, value: Any, /, *, separator: str = "=") -> str:
    """"""
    formatted_type = TypeAsRichStr(value, prefix=":")
    if isinstance(value, Sequence) and (value.__len__() == 0):
        value = "[cyan]<empty>[/]"

    return f"[blue]{name}{separator}[/]{value}{formatted_type}"
