from pathlib import Path
from typing import TYPE_CHECKING

from antievil import (
    LogicError,
    PleaseDefineError,
    TypeExpectError,
    UnsupportedError,
)

from clyjin_templates.filesystem.models import (
    FileNode,
    FileNodeInternal,
    NodeContent,
    NodeFieldValue,
    NodeRoot,
    NodeType,
)
from clyjin_templates.template.group import TemplateGroupInternal
from clyjin_templates.template.vars import (
    TemplateGroupVar,
    TemplateGroupVarInternal,
    TemplateGroupVarsInternal,
    TemplateGroupVarValue,
)
from clyjin_templates.utils.klass import Static
from clyjin_templates.utils.never import never

if TYPE_CHECKING:
    from clyjin_templates.template.group import TemplateGroup


class TemplateGroupConversionUtils(Static):
    """
    Converts external Template Group to internal variant.
    """
    @classmethod
    def convert_to_internal(
        cls,
        group: "TemplateGroup",
        var_args: dict[str, TemplateGroupVarValue] | None = None,
    ) -> TemplateGroupInternal:
        internal_vars: TemplateGroupVarsInternal | None = \
            cls._get_internal_vars(group, var_args)

        return TemplateGroupInternal(
            name=group.name,
            tree=FileNodeConversionUtils.convert_to_internal(group.tree),
            templates=group.templates,
            description=group.description,
            vars=internal_vars,
        )

    @classmethod
    def _get_internal_vars(
        cls,
        group: "TemplateGroup",
        var_args: dict[str, TemplateGroupVarValue] | None = None,
    ) -> TemplateGroupVarsInternal | None:
        if group.vars is None:
            return None

        result: dict[str, TemplateGroupVarInternal] = {}

        for var_name, var in group.vars.model_dump().items():
            result[var_name] = cls._get_internal_var(
                var_name,
                TemplateGroupVar.model_validate(
                    var,
                ) if var is not None else None,
                var_args.get(var_name, None) if var_args is not None else None,
            )

        return TemplateGroupVarsInternal.model_validate(result)

    @classmethod
    def _get_internal_var(
        cls,
        var_name: str,
        var: TemplateGroupVar | None,
        var_arg: TemplateGroupVarValue | None = None,
    ) -> TemplateGroupVarInternal:
        final_value: TemplateGroupVarValue

        default: TemplateGroupVarValue | None = None
        if var is not None and var.default is not None:
            default = var.default

        if default is None and var_arg is None:
            raise PleaseDefineError(
                cannot_do="template vars initializing",
                please_define=f"variable=<{var_name}>",
            )
        elif (
            (default is None and var_arg is not None)
            or (default is not None and var_arg is not None)
        ):
            final_value = var_arg
        elif default is not None and var_arg is None:
            final_value = default
        else:
            errmsg: str = "reached unexpected branch"
            raise LogicError(errmsg)

        return TemplateGroupVarInternal(
            default=default,
            scopes=var.scopes if var is not None else None,
            value=final_value,
        )


class FileNodeConversionUtils(Static):
    """
    Converts external FileTreeNodes to internal variants.
    """
    @staticmethod
    def convert_to_internal(node: FileNode) -> FileNodeInternal:
        root: NodeRoot | None = node.root
        _type: NodeType | None = FileNodeConversionUtils._get_node_type(root)

        content: NodeContent | None = None
        if root is not None:
            content = FileNodeConversionUtils._get_node_content(
                root,
                _type,
            )

        nodes: dict[str, FileNodeInternal] | None = \
            FileNodeConversionUtils._convert_nodes(node)
        final_type: NodeType = FileNodeConversionUtils._get_final_type(
            _type,
            content,
            nodes,
        )

        return FileNodeInternal(
            type=final_type,
            content=content,
            nodes=nodes,
        )

    @staticmethod
    def _get_final_type(
        pretype: NodeType | None,
        content: NodeContent | None,
        nodes: dict[str, FileNodeInternal] | None,
    ) -> NodeType:
        """
        Finds final type out of existing node parameters.

        If pretype is not None, it is returned. Otherwise guess depending on
        other given arguments is made, according to conventional defaults.
        """
        if pretype is not None:
            return pretype

        if content is None and nodes is None:
            # empty file assumed
            return NodeType.File
        if content is None and nodes is not None:
            return NodeType.Dir
        if content is not None and nodes is None:
            return NodeType.File
        if content is not None and nodes is not None:
            errmsg: str = \
                f"unexpected defined content=<{content}> and" \
                f" nodes=<{nodes}> at the same parent node"
            raise LogicError(errmsg)

        errmsg: str = "not all branches are considered"
        raise LogicError(errmsg)

    @staticmethod
    def _get_node_type(
        root: NodeRoot | None,
    ) -> NodeType | None:
        if root is None:
            return NodeType.Dir

        _type: NodeFieldValue | None = root.get("$type", None)

        if isinstance(_type, str):
            _type = NodeType(_type)

        if _type is None:
            # at this points we cannot recognize which type a node should have,
            # if it will have any subnodes - we would set directory, otherwise
            # file. Further conversion operations should handle this.
            return None
        elif not isinstance(_type, NodeType):
            raise TypeExpectError(
                obj=_type,
                ExpectedType=NodeType,
                expected_inheritance="instance",
                ActualType=type(_type),
            )
        return _type

    @staticmethod
    def _get_node_content(
        root: NodeRoot,
        _type: NodeType | None,
    ) -> NodeContent | None:
        content: NodeFieldValue | None = root.get("$content", None)

        if content is None:
            return None

        match _type:
            case NodeType.File:
                return FileNodeConversionUtils._get_file_node_content(content)
            case NodeType.Dir:
                # content is not None and type is Dir => directories can't
                # have content field
                raise UnsupportedError(
                    title="`$content` field for node of type",
                    value=_type,
                )
            case None:
                # content is not None and type is None, assuming file
                return FileNodeConversionUtils._get_file_node_content(content)
            case _:
                never(_type)

    @staticmethod
    def _get_file_node_content(
        maybe_content: NodeFieldValue,
    ) -> NodeContent:
        if not isinstance(maybe_content, (str, Path)):
            raise TypeExpectError(
                obj=maybe_content,
                # TODO(ryzhovalex): multiple ExpectedTypes as soon as
                #   Antievil supports it
                # 0
                ExpectedType=str,
                expected_inheritance="instance",
                ActualType=type(maybe_content),
            )

        return maybe_content

    @staticmethod
    def _convert_nodes(
        node: FileNode,
    ) -> dict[str, FileNodeInternal] | None:
        if node.root is None:
            return None

        result: dict[str, FileNodeInternal] = {}
        for k, v in node.root.items():
            if isinstance(v, FileNode):
                result[k] = FileNodeConversionUtils.convert_to_internal(v)

        if not result:
            return None
        return result
