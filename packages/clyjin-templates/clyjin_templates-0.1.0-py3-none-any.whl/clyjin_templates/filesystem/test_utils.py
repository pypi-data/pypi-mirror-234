from clyjin_templates.filesystem.models import FileNodeInternal, NodeType


def test_s1_conversion(s1_root_node_internal: FileNodeInternal):
    node: FileNodeInternal = s1_root_node_internal

    expected_node: FileNodeInternal = FileNodeInternal(
        type=NodeType.Dir,
        content=None,
        nodes={
            "src": FileNodeInternal(
                type=NodeType.Dir,
                content=None,
                nodes={
                    "__init__.py": FileNodeInternal(
                        type=NodeType.File,
                        content="&s1_1.py",
                        nodes=None,
                    ),
                    "drivers": FileNodeInternal(
                        type=NodeType.Dir,
                        content=None,
                        nodes={
                            "main.py": FileNodeInternal(
                                type=NodeType.File,
                                content="&s1_2.py",
                                nodes=None,
                            ),
                        },
                    ),
                    "local": FileNodeInternal(
                        type=NodeType.Dir,
                        content=None,
                        nodes=None,
                    ),
                },
            ),
            "README.md": FileNodeInternal(
                type=NodeType.File,
                content="# s1_readme",
            ),
        },
    )

    assert node == expected_node
