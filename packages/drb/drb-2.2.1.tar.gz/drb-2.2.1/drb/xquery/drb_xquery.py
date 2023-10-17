from antlr4 import InputStream, CommonTokenStream
from drb.core import DrbNode
from .XQueryLexer import XQueryLexer
from .XQueryParser import XQueryParser
from .drb_xquery_context import DynamicContext
from .drb_xquery_utils import DrbQueryFuncUtil
from .drb_xquery_visitor import DrbQueryVisitor, DrbXqueryParserErrorListener
import io
import sys


class DrbXQuery:

    def __init__(self, xquery):
        self.static_context = None
        if isinstance(xquery, DrbNode):
            xquery = xquery.get_impl(io.BufferedIOBase)

        if isinstance(xquery, io.BufferedIOBase):
            reader = xquery
            xquery = reader.read().decode()
            reader.close()

        # init Lexer with query
        lexer = XQueryLexer(InputStream(xquery))

        self.stream = CommonTokenStream(lexer)
        self.parser = XQueryParser(self.stream)

        self.parser.addErrorListener(DrbXqueryParserErrorListener())
        # parse query and reject it if error
        self.tree = self.parser.module()

    def execute(self, *args, **kwargs):
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)

        list_nodes = args

        if len(list_nodes) == 0:
            list_nodes = [None]

        output_list = []
        for node_item in list_nodes:
            visitor = DrbQueryVisitor(DynamicContext(node_item),
                                      tokens=self.stream)

            visitor.external_var_map = kwargs
            self.static_context = visitor.static_context

            output = visitor.visitModule(self.tree)

            nodes_ouput = []

            if not isinstance(output, list):
                output_list.append(output)
                if output is not None:
                    node = DrbQueryFuncUtil.get_node(output)
                    if node is not None and isinstance(node, DrbNode):
                        if node not in nodes_ouput:
                            nodes_ouput.append(node)
            else:
                output_list.extend(output)
                for one_ouput in output:
                    if one_ouput is not None:
                        node = DrbQueryFuncUtil.get_node(one_ouput)
                        if node is not None and isinstance(node, DrbNode):
                            if node not in nodes_ouput:
                                nodes_ouput.append(node)

            for node in nodes_ouput:
                parent = node.parent
                while parent is not None:
                    if parent not in nodes_ouput:
                        nodes_ouput.append(parent)
                    parent = parent.parent

            for node_child in self.static_context.list_children_open:
                if node_child not in nodes_ouput:
                    node_child.close()

        sys.setrecursionlimit(old_limit)

        return output_list
