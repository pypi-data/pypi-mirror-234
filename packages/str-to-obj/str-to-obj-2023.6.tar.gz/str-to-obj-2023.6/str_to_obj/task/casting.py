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
from pathlib import Path as path_t
from types import EllipsisType, NoneType, UnionType
from typing import Any, Iterable

from str_to_obj.type.hint import any_hint_h, simple_hint_h
from str_to_obj.type.hint_tree import hint_tree_t


class _not_a_leaf_node_t:
    pass


_NOT_A_LEAF_NODE = _not_a_leaf_node_t()


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _value_node_t:
    """
    Leave elements to the tree.
    leaf_value: None for non-leaf nodes; Actual value (before or after cast) for leaves.
    """

    type: simple_hint_h = None
    leaf_value: Any | None = _NOT_A_LEAF_NODE


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _value_tree_t(_value_node_t):
    elements: tuple[_value_tree_t, ...] = None

    @classmethod
    def NewFromValue(cls, value: Any, /) -> _value_tree_t:
        """"""
        if isinstance(value, Iterable) and not isinstance(value, str):
            elements = tuple(cls.NewFromValue(_elm) for _elm in value)
            return cls(type=type(value), elements=elements)

        return cls(leaf_value=value)

    def _RebuiltValue(self) -> Any:
        """"""
        if self.leaf_value is _NOT_A_LEAF_NODE:
            return self.type(_elm._RebuiltValue() for _elm in self.elements)

        return self.leaf_value

    def CastValue(
        self, hint_tree: hint_tree_t, /, *, only_check_validity: bool = False
    ) -> tuple[Any, list[str]] | list[str]:
        """"""
        issues = self._CastToHint(hint_tree)
        if issues.__len__() > 0:
            if only_check_validity:
                return issues
            else:
                return None, issues

        if only_check_validity:
            return []
        else:
            return self._RebuiltValue(), []

    def _CastToHint(self, hint_node: hint_tree_t, /) -> list[str]:
        """
        Returned value=the value tree has been successfully cast to the hint tree
        specification, or not.
        """
        hn_type = hint_node.type
        hn_elements = hint_node.elements

        if hn_type is Any:
            return self._CompliesWithAnnotations(hint_node)

        if hn_type is NoneType:
            # None is not supposed to have annotations. They are ignored if it does.
            if self.leaf_value is None:
                output = []
            else:
                output = [f"{self.leaf_value}: Invalid value; Expected=None."]
            return output

        if hn_type is UnionType:
            issues = []
            for element in hn_elements:
                local_issues = self._CastToHint(element)
                if local_issues.__len__() > 0:
                    issues.extend(
                        f"    - {element.type.__name__}: {_elm}"
                        for _elm in local_issues
                    )
                else:
                    return []
            rebuilt = self._RebuiltValue()
            type_options = " or ".join(_elm.type.__name__ for _elm in hn_elements)
            issues = "\n".join(issues)
            return [f"{rebuilt}: Cannot be cast to type {type_options}:\n{issues}"]

        if self.elements is None:
            if hn_elements is None:
                if not isinstance(self.leaf_value, hn_type):
                    # Dealing with "equivalent" types, such as "str" and "pathlib.Path".
                    if issubclass(hn_type, path_t):
                        if isinstance(self.leaf_value, str):
                            if self.leaf_value == "":
                                # path_t("") == current_folder (.)!
                                self.leaf_value = None
                            else:
                                self.leaf_value = hn_type(self.leaf_value)
                        else:
                            return [
                                f"{self.leaf_value}: Cannot be cast to type "
                                f'"{hn_type.__name__}".'
                            ]
                    else:
                        return [
                            f"{self.leaf_value}: Invalid value type "
                            f'"{type(self.leaf_value).__name__}"; '
                            f'Expected="{hn_type.__name__}".'
                        ]

                return self._CompliesWithAnnotations(hint_node)
            else:
                return [
                    f"{self.leaf_value}: Not a container value; "
                    f"Expected=Container with template {hint_node.template_as_str}."
                ]

        # For then on, self.elements is not None.

        if hn_elements is None:
            # The type hint does not fully specify valid values, so anything is valid.
            if not issubclass(self.type, hn_type):
                rebuilt = self._RebuiltValue()
                try:
                    _ = hn_type(rebuilt)
                except:
                    return [f"{rebuilt}: Cannot be cast to type {hn_type.__name__}."]

            return self._CompliesWithAnnotations(hint_node)

        n_value_elements = self.elements.__len__()
        n_hint_elements = hn_elements.__len__()
        has_ellipsis = (n_hint_elements == 2) and (hn_elements[1].type is EllipsisType)
        should_fake_ellipsis = (n_hint_elements == 1) and issubclass(
            hn_type, (list, set)
        )
        if (
            has_ellipsis
            or should_fake_ellipsis
            or (n_value_elements == n_hint_elements)
        ):
            if has_ellipsis or should_fake_ellipsis:
                adjusted_hn_elements = n_value_elements * (hn_elements[0],)
            else:
                adjusted_hn_elements = hn_elements
            issues = []
            for value_elm, hint_elm in zip(self.elements, adjusted_hn_elements):
                value_elm: _value_tree_t
                issues.extend(value_elm._CastToHint(hint_elm))
            if issues.__len__() > 0:
                return issues

            return self._CompliesWithAnnotations(hint_node)

        return [
            f"{self.leaf_value}: Invalid container value; "
            f"Expected=Value following template {hint_node.template_as_str}."
        ]

    def _CompliesWithAnnotations(self, hint_node: hint_tree_t, /) -> list[str]:
        """"""
        output = []

        for annotation in hint_node.annotations:
            output.extend(annotation.ValueIsCompliant(self._RebuiltValue()))

        return output


def CastValue(
    value: Any, hint: any_hint_h | hint_tree_t, /, *, only_check_validity: bool = False
) -> tuple[Any, list[str]] | list[str]:
    """"""
    value_tree = _value_tree_t.NewFromValue(value)
    if not isinstance(hint, hint_tree_t):
        hint = hint_tree_t.NewFromTypeHint(hint)

    return value_tree.CastValue(hint, only_check_validity=only_check_validity)
