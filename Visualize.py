import ast
import inspect
import json
import re
import uuid
import pydot_ng as pydot
from _ast import AST


def ast_parse(method):
    def wrapper(*args, **kwargs):
        if isinstance(args[0], str):
            ast_obj = ast.parse(args[0])
        else:
            obj = inspect.getsource(args[0])
            ast_obj = ast.parse(obj)
        json_parsed = method(ast_obj, **kwargs)
        parsed = json.loads(json_parsed)

        return parsed

    return wrapper


@ast_parse
def json_ast(node):
    def _format(_node):
        if isinstance(_node, AST):
            fields = [("_PyType", _format(_node.__class__.__name__))]
            fields += [(a, _format(b)) for a, b in iter_fields(_node)]
            return "{ %s }" % ", ".join(('"%s": %s' % field for field in fields))
        if isinstance(_node, list):
            return "[ %s ]" % ", ".join([_format(x) for x in _node])
        if isinstance(_node, bytes):
            return json.dumps(_node.decode("utf-8"))

        return json.dumps(_node)

    return _format(node)


def iter_fields(node):
    try:
        for field in node._fields:
            yield field, getattr(node, field)
    except AttributeError:
        yield


def construct_graph(graph, ast_nodes, parent_node="", node_hash="__init__"):
    if isinstance(ast_nodes, dict):
        for key, node in ast_nodes.items():
            if not parent_node:
                parent_node = node
                continue
            if key == "_PyType":
                node = graph_detail(node, ast_nodes)
                node_hash = draw(parent_node, node, graph=graph, parent_hash=node_hash)
                parent_node = node
                continue
            if isinstance(node, dict):
                construct_graph(
                    graph, node, parent_node=parent_node, node_hash=node_hash
                )
            if isinstance(node, list):
                [
                    construct_graph(
                        graph, item, parent_node=parent_node, node_hash=node_hash
                    )
                    for item in node
                ]
    graph.write_png("astree.png")


def graph_detail(value, ast_scope):
    detail_keys = ("module", "n", "s", "id", "name", "attr", "arg")
    for key in detail_keys:
        if not isinstance(dict.get(ast_scope, key), type(None)):
            value = f"{value}\n{key}: {ast_scope[key]}"

    return value


def draw(parent_name, child_name, graph, parent_hash):
    parent_node = pydot.Node(parent_hash, label=parent_name, shape="box")
    child_hash = str(uuid.uuid4())
    child_node = pydot.Node(child_hash, label=child_name, shape="box")
    graph.add_node(parent_node)
    graph.add_node(child_node)
    graph.add_edge(pydot.Edge(parent_node, child_node))
    return child_hash


def clean_node(method):
    def wrapper(*args, **kwargs):
        parent_name, child_name = tuple(
            "_node" if node == "node" else node for node in args
        )
        illegal_char = re.compile(r"[,\\/]$")
        illegal_char.sub("*", child_name)
        if not child_name:
            return
        if len(child_name) > 2500:
            child_name = "~~~DOCS: too long to fit on graph~~~"
        args = (parent_name, child_name)
        return method(*args, **kwargs)

    return wrapper


def visualize(code):
    graph = pydot.Dot(
        graph_type="digraph",
        strict=True,
        constraint=True,
        concentrate=True,
        splines="polyline",
    )
    construct_graph(graph, json_ast(code))
