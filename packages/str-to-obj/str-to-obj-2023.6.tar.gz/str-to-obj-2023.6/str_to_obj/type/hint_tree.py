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

from __future__ import annotations

import dataclasses as dtcl
import re as regx
from types import EllipsisType, NoneType, UnionType
from typing import Any, Union, get_args, get_origin

from str_to_obj.task.inspection import HintComponents
from str_to_obj.type.annotation import annotation_t
from str_to_obj.type.hint import (
    any_hint_h,
    complex_hint_additions_h,
    non_complex_hint_h,
    simple_hint_h,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _hint_node_t:
    """
    Leave elements to the tree.
    """

    type: non_complex_hint_h | UnionType | EllipsisType | type[NoneType]
    annotations: tuple[annotation_t, ...] = ()


@dtcl.dataclass(slots=True, repr=False, eq=False)
class hint_tree_t(_hint_node_t):
    elements: tuple[hint_tree_t, ...] = None

    @classmethod
    def NewFromTypeHint(
        cls, hint: any_hint_h | complex_hint_additions_h, /
    ) -> hint_tree_t:
        """
        Note that type hints cannot translate into hint trees with an OR-node having a child
        OR-node. For example: str | (int | float) is interpreted as str | int | float. This
        is important when creating a type selector for multi-type parameters since only
        direct child nodes are taken into account for widget creation, so these nodes must
        be types, not an OR subtree.
        """
        if isinstance(hint, annotation_t):
            # This is a common mistake in specifications.
            raise ValueError(
                f'{hint}: Invalid hint type "{type(hint).__name__}"; '
                f"Expected={any_hint_h}."
            )

        # Dealing with complex_hint_additions_h first
        if hint is Ellipsis:
            return cls(type=EllipsisType)
        if (hint is None) or (hint is NoneType):
            return cls(type=NoneType)

        # nnts: Do not use "annotations" since it shadows __future__.annotations.
        raw_hint, nnts = HintComponents(hint)

        if (origin := get_origin(raw_hint)) is None:
            return cls(type=raw_hint, annotations=nnts)

        # Handled types: list, set, tuple, with sets using the dict delimiters { and }.
        if origin is dict:
            raise TypeError(f"{origin.__name__}: Unhandled type.")

        if origin is Union:
            origin = UnionType
        # get_args returns NoneType for None. This must be taken into account above.
        elements = tuple(cls.NewFromTypeHint(_elm) for _elm in get_args(raw_hint))
        return cls(type=origin, annotations=nnts, elements=elements)

    @property
    def all_annotations(self) -> list[annotation_t]:
        """"""
        output = list(self.annotations)

        if self.elements is not None:
            for element in self.elements:
                output.extend(element.all_annotations)

        return output

    @property
    def template(self) -> simple_hint_h | dict[int, Any] | None:
        """"""
        if self.type is NoneType:
            return None

        if self.type is UnionType:
            return {_key: _elm.template for _key, _elm in enumerate(self.elements)}

        if self.elements is None:
            return self.type

        return self.type(_elm.template for _elm in self.elements)

    @property
    def template_as_str(self) -> str:
        """"""
        output = (
            str(self.template)
            .replace(str(EllipsisType), "...")
            .replace("<class '", "")
            .replace("'>", "")
        )
        output = regx.sub("{\d: ", "{", output, flags=regx.ASCII)
        output = regx.sub(", \d:", " |", output, flags=regx.ASCII)

        return output


# Potential additions for _hint_node_t:
# def __str__(self) -> str:
#     """"""
#     return text_t.from_markup(self.__rich__()).plain
#
# def __rich__(self) -> str:
#     """"""
#     output = [TypeAsRichStr(self)]
#
#     names = (_fld.name for _fld in dtcl.fields(self))
#     for name in names:
#         value = getattr(self, name)
#         output.append(f"    {NameValueTypeAsRichStr(name, value, separator='@=@')}")
#
#     output = AlignedOnSeparator(output, "@=@", " = ")
#
#     return "\n".join(output)
