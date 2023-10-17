from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl
from decimal import Decimal
from typing import Any, Dict, Tuple
from drb.core.node import DrbNode
from drb.drivers.xml import XmlNode
from .XQueryLexer import XQueryLexer
from .XQueryParser import XQueryParser
from .XQueryParserVisitor import XQueryParserVisitor
from .drb_xquery_context import (
    AxeNode, DynamicContext, NavigationStep, StaticContext, NamespaceMap
)
from .drb_xquery_func import DrbQueryFuncCall
from .drb_xquery_item import DrbXqueryItem
from .drb_xquery_utils import DrbQueryFuncUtil
from .drb_xquery_variable import XqueryVariable, XqueryBuildIn
from .execptions import DynamicException, ErrorXQUERY, StaticException
import html
import io
import drb.topics.resolver as resolver


class DrbQueryVisitor(XQueryParserVisitor):

    def __init__(self, dynamic_context: DynamicContext,
                 static_context=None,
                 list_context=None,
                 step_nav=NavigationStep.CHILD,
                 is_module=False,
                 external_var_map: dict = None,
                 tokens=None):

        self.is_module = is_module

        self.prefix_module = ''
        self.tokens = tokens

        self.dynamic_context = dynamic_context

        if list_context is None:
            self.list_context = [self.dynamic_context]
        else:
            self.list_context = list_context

        self.current_axe = AxeNode(step_nav)
        self.flwor_scope_list = None

        if static_context is None:
            self.static_context = StaticContext()
            DrbQueryFuncCall.init_namespace_context(self.static_context)
        else:
            self.static_context = static_context

        self.external_var_map = external_var_map
        if self.external_var_map is None:
            self.external_var_map = {}

    def get_namespace_full_name(self, prefix: str):
        ns_full = self.static_context.get_namespace_full_name(prefix)
        if self.dynamic_context and len(ns_full) == 0:
            if isinstance(self.dynamic_context, DynamicContext):
                ns_full = self.dynamic_context.get_namespace_full_name(prefix)
            else:
                return ns_full
        return ns_full

    def visitVersionDecl(self, ctx: XQueryParser.VersionDeclContext):
        # unused we don't control the version
        return ''

    def visitModuleImport(self, ctx: XQueryParser.ModuleImportContext):
        index_uri = 0
        prefix_module = ''
        ns_module = ''
        uri_of_lib = None
        if ctx.ncName() is not None:
            prefix_module = self.visitNcName(ctx.ncName())
            module_context = self.visitUriLiteral(ctx.uriLiteral(index_uri))
            index_uri = index_uri + 1
            self.static_context.add_namespace(prefix_module, module_context)
            uri_of_lib = module_context
            ns_module = module_context

        if ctx.KW_AT() is not None:
            uri_of_lib = self.visitUriLiteral(ctx.uriLiteral(index_uri))

        if uri_of_lib is not None:
            if uri_of_lib in self.static_context.imported_module.keys():
                return

            self.static_context.imported_module[uri_of_lib] = prefix_module
            node_module = resolver.create(uri_of_lib)
            if node_module.has_impl(io.RawIOBase):
                impl = node_module.get_impl(io.BufferedIOBase)

                xquery_buffer = impl.readlines()
                impl.close()
                node_module.close()
                xquery_string = ''

                for line in xquery_buffer:
                    xquery_string = xquery_string + line.decode('utf-8')
                lexer = XQueryLexer(InputStream(xquery_string))
                stream = CommonTokenStream(lexer)
                parser = XQueryParser(stream)
                tree = parser.libraryModule()

                visitor = DrbQueryVisitor(None, is_module=True)
                visitor.static_context.imported_module = \
                    self.static_context.imported_module.copy()
                # visitor.static_context.clone(self.static_context)
                output = visitor.visit(tree)

                for ns, name_var in \
                        visitor.static_context.in_scope_variables.keys():
                    var = \
                        visitor.static_context.in_scope_variables[ns, name_var]
                    if ns is not None \
                            and ns != ns_module:
                        continue
                        # TODO raise error
                    var.namespace = prefix_module
                    self.static_context.in_scope_variables[module_context,
                                                           var.name] = var

                for ns, func_name in visitor.static_context.\
                        namespace_builtin_func.keys():

                    if ns is not None and ns != ns_module:
                        continue

                    ns = ns_module
                    func = visitor.static_context.namespace_builtin_func[
                        ns, func_name]

                    self.static_context.namespace_builtin_func[
                        ns, func_name] = func
        else:
            raise DynamicException(ErrorXQUERY.FOAR0001,
                                   "Error import is not correct")

    def visitMainModule(self, ctx: XQueryParser.MainModuleContext):
        if ctx.prolog() is not None:
            visitor = DrbQueryVisitor(self.dynamic_context,
                                      static_context=self.static_context,
                                      external_var_map=self.external_var_map,
                                      tokens=self.tokens)
            visitor.visitProlog(ctx.prolog())
        if ctx.queryBody() is not None:
            return self.visitQueryBody(ctx.queryBody())
        return ''

    def visitModuleDecl(self, ctx: XQueryParser.ModuleDeclContext):
        if ctx.ncName() is not None:
            prefix = self.visitNcName(ctx.ncName())
            full_name = self.visitStringLiteral(ctx.stringLiteral())
            self.static_context.add_namespace(prefix, full_name)
            self.prefix_module = prefix
        return ''

    def visitFunctionDecl(self, ctx: XQueryParser.FunctionDeclContext):
        if ctx.eqName() is not None:
            eqname = self.visitEqName(ctx.eqName())
            if self.is_module:
                self.static_context.add_func_build_in(eqname, ctx,
                                                      self.static_context)
            else:
                self.static_context.add_func_build_in(eqname, ctx)

    def visitNamespaceDecl(self, ctx: XQueryParser.NamespaceDeclContext):
        if ctx.ncName() is not None:
            prefix = self.visitNcName(ctx.ncName())
            full_name = self.visitUriLiteral(ctx.uriLiteral())

            self.static_context.add_namespace(prefix, full_name)
        return ''

    def visitDefaultNamespaceDecl(
            self, ctx: XQueryParser.DefaultNamespaceDeclContext):
        if ctx.stringLiteral() is not None:
            namespace = self.visitStringLiteral(ctx.stringLiteral())
            if ctx.KW_ELEMENT():
                self.static_context.namespace_default_elt = namespace
            if ctx.KW_FUNCTION():
                self.static_context.namespace_default_func = namespace
        return ''

    def visitVarDecl(self, ctx: XQueryParser.VarDeclContext):
        varname_full = self.visitVarName(ctx.varName())
        var_namespace, var_name = DrbQueryFuncUtil.split_namespace_name(
            varname_full)

        var_value = None
        external_var = False
        type_var = None
        if ctx.typeDeclaration() is not None:
            type_var = self.visitTypeDeclaration(ctx.typeDeclaration())

        if ctx.KW_EXTERNAL() is not None:
            external_var = True
            if var_name in self.external_var_map.keys():
                var_value = self.external_var_map[var_name]
            elif ctx.varDefaultValue() is not None:
                var_value = self.visitVarDefaultValue(ctx.varDefaultValue())
            else:
                raise DynamicException(
                    ErrorXQUERY.XPDY0002,
                    "No value for external variable " + var_name + " given.")

        elif ctx.varValue() is not None:
            var_value = self.visitVarValue(ctx.varValue())

        self.static_context.add_var(varname_full,
                                    XqueryVariable(var_name,
                                                   var_namespace,
                                                   external=external_var,
                                                   value=var_value,
                                                   type_var=type_var))

    def visitVarRef(self, ctx: XQueryParser.VarRefContext):
        var_name = self.visitEqName(ctx.eqName())
        var = self.static_context.get_var(var_name)

        return var.get_value()

    def visitStringConcatExpr(self, ctx: XQueryParser.StringConcatExprContext):
        res = self.visitChildren(ctx)
        return res

    def visitSequenceType(self, ctx: XQueryParser.SequenceTypeContext):
        res = self.visitItemType(ctx.itemType())
        if res is None:
            return res
        if ctx.STAR():
            # to simplify if max > 1 like 100 there are no limit
            return res, 0, 100
        if ctx.PLUS():
            # to simplify if max > 1 like 100 there are no limit
            return res, 1, 100
        if ctx.QUESTION():
            return res, 0, 1

        return res

    def visitArgumentList(self, ctx: XQueryParser.ArgumentListContext):
        result = []
        list_context = self.list_context
        dynamic_context = self.dynamic_context
        for arg in ctx.argument():
            result.append(self.visitArgument(arg))
            self.list_context = list_context
            self.dynamic_context = dynamic_context

        return result

    @staticmethod
    def get_value_from_definition_type(value_arg,
                                       type_var_full,
                                       func_msg):
        arg_min = 1
        arg_max = 1
        if isinstance(type_var_full, tuple):
            arg_min = type_var_full[1]
            arg_max = type_var_full[2]
            type_var_full = type_var_full[0]

        type_var_namespace, type_var = \
            DrbQueryFuncUtil.split_namespace_name(type_var_full)
        value_arg_typed = XqueryVariable.get_value_typed(
            type_var,
            type_var_namespace,
            value_arg,
            arg_min=arg_min,
            arg_max=arg_max,
            func_msg=func_msg)
        return value_arg_typed

    def call_built_in_func(self,
                           func: XqueryBuildIn,
                           argument_list: list):
        built_in_func = func.exp_func
        list_param = built_in_func.functionParams()

        old_scop = None
        previous_context = None
        if func.specific_context is not None:
            previous_context = self.static_context
            self.static_context = func.specific_context
        old_scop = self.static_context.in_scope_variables
        self.static_context.in_scope_variables = old_scop.copy()

        if list_param is not None:
            list_def_args = list_param.functionParam()
            if len(list_def_args) != len(argument_list):
                raise DynamicException(ErrorXQUERY.XPST0017, "Function call " +
                                       func.name +
                                       "() does not match "
                                       "arity of "
                                       "the built-in function")
            for index in range(len(list_def_args)):
                def_arg = list_def_args[index]
                arg_name = self.visitQName(def_arg.qName())
                value_arg = argument_list[index]

                if def_arg.typeDeclaration() is not None:
                    type_var_full = self.visitTypeDeclaration(
                        def_arg.typeDeclaration())
                    if type_var_full is not None:
                        value_arg = self.get_value_from_definition_type(
                            value_arg,
                            type_var_full,
                            func.name + ' arg index ' + str(index + 1))

                self.static_context.add_var(arg_name, XqueryVariable(arg_name,
                                            value=value_arg))
        elif len(argument_list) != 0:
            raise DynamicException(ErrorXQUERY.XPST0017, "Function call " +
                                   func.name +
                                   "() is call with arg "
                                   "but build in don't take any "
                                   "any built-in function")

        result = self.visitFunctionBody(built_in_func.functionBody())

        if built_in_func.functionReturn() is not None and \
                built_in_func.functionReturn().KW_AS() is not None:
            type_var_full = self.visitSequenceType(built_in_func.
                                                   functionReturn().
                                                   sequenceType())

            if type_var_full is not None:
                result = self.get_value_from_definition_type(result,
                                                             type_var_full,
                                                             func.name +
                                                             ' return ')

        self.static_context.in_scope_variables = old_scop

        if previous_context is not None:
            self.static_context = previous_context

        return result

    def visitFunctionCall(self, ctx: XQueryParser.FunctionCallContext):
        name_full = self.visitEqName(ctx.eqName())

        (namespace, name_func) = DrbQueryFuncUtil.split_namespace_name(
            name_full)

        if namespace is None or len(namespace) == 0:
            namespace = self.static_context.namespace_default_func

        func_to_call = self.static_context.get_func_namespace(namespace,
                                                              name_func)
        argument_list = self.visitArgumentList(ctx.argumentList())

        if func_to_call is not None:
            return func_to_call(
                name_func, self.dynamic_context,
                self.static_context, *argument_list)

        func_to_call = self.static_context.get_func_build_in(name_full)
        if func_to_call is not None:
            return self.call_built_in_func(func_to_call, argument_list)

        raise DynamicException(ErrorXQUERY.XPST0017, "Function call " +
                               name_full +
                               "() does not match the name and "
                               "arity of "
                               "any built-in function")

    def visitAttributeNameOrWildcard(self,
                                     ctx: XQueryParser
                                     .AttributeNameOrWildcardContext):
        return self.visitChildren(ctx)

    def visitElementNameOrWildcard(self,
                                   ctx: XQueryParser
                                   .ElementNameOrWildcardContext):
        return self.visitChildren(ctx)

    @staticmethod
    def append_or_extend(object_to_append, list_object: list):
        if isinstance(object_to_append, list):
            list_object.extend(object_to_append)
        else:
            list_object.append(object_to_append)

    @staticmethod
    def append_object_or_index(list_source: list, list_or_slice_or_index,
                               list_result: list):
        if isinstance(list_or_slice_or_index, list):
            list_result.extend(list_or_slice_or_index)
        elif isinstance(list_or_slice_or_index, int):
            list_result.append(list_source[list_or_slice_or_index])
        else:
            list_result.append(list_or_slice_or_index)

    def visitOrExpr(self, ctx: XQueryParser.OrExprContext):
        if len(ctx.KW_OR()) == 0:
            return self.visitChildren(ctx)

        for toComp in ctx.andExpr():
            visitor_for_comp = DrbQueryVisitor(
                self.dynamic_context,
                static_context=self.static_context,
                external_var_map=self.external_var_map,
                tokens=self.tokens)
            result = visitor_for_comp.visitAndExpr(toComp)
            if DrbQueryFuncUtil.get_effective_boolean_value(result):
                return True
        return False

    def visitAndExpr(self, ctx: XQueryParser.AndExprContext):
        if len(ctx.KW_AND()) == 0:
            return self.visitChildren(ctx)

        for toComp in ctx.comparisonExpr():
            visitor_for_comp = DrbQueryVisitor(
                self.dynamic_context,
                static_context=self.static_context,
                external_var_map=self.external_var_map,
                tokens=self.tokens)
            result = visitor_for_comp.visitComparisonExpr(toComp)
            if not DrbQueryFuncUtil.get_effective_boolean_value(result):
                return False

        return True

    def visitComparisonExpr(self, ctx: XQueryParser.ComparisonExprContext):
        op = ctx.valueComp()
        if op is None:
            op = ctx.generalComp()
        if op is None:
            op = ctx.nodeComp()
        if op is None:
            return self.visitChildren(ctx)
        op = op.getText()

        visitor_for_left = DrbQueryVisitor(self.dynamic_context,
                                           static_context=self.static_context,
                                           external_var_map=self.
                                           external_var_map,
                                           tokens=self.tokens)
        visitor_for_right = DrbQueryVisitor(self.dynamic_context,
                                            static_context=self.static_context,
                                            external_var_map=self.
                                            external_var_map,
                                            tokens=self.tokens)

        left = visitor_for_left.visitStringConcatExpr(
            ctx.stringConcatExpr(0))
        right = visitor_for_right.visitStringConcatExpr(
            ctx.stringConcatExpr(1))

        list_left = left
        if not isinstance(left, list):
            list_left = [left]

        list_right = right
        if not isinstance(right, list):
            list_right = [right]

        test_ok = False

        for left_item in list_left:
            for right_item in list_right:
                if op == 'is':
                    if left_item is right_item:
                        test_ok = True
                        break
                    else:
                        continue

                left_value, right_value = \
                    DrbQueryFuncUtil.convert_before_compare(left_item,
                                                            right_item)

                if op == 'eq' or op == '=':
                    if DrbQueryFuncUtil.is_equal(left_value, right_value):
                        test_ok = True
                        break
                elif op == 'ne' or op == '!=':
                    if left_value != right_value:
                        test_ok = True
                        break
                elif op == 'gt' or op == '>':
                    if left_value > right_value:
                        test_ok = True
                        break
                elif op == 'ge' or op == '>=':
                    if left_value >= right_value:
                        test_ok = True
                        break
                elif op == 'lt' or op == '<':
                    if left_value < right_value:
                        test_ok = True
                        break
                elif op == 'le' or op == '<=':
                    if left_value <= right_value:
                        test_ok = True
                        break

            if test_ok:
                break

        return test_ok

    def visitUnaryExpression(self, ctx: XQueryParser.UnaryExpressionContext):
        res = self.visitChildren(ctx)
        if ctx.MINUS() is not None and len(ctx.MINUS()) > 0:
            if isinstance(res, (int, Decimal, float)):
                res = res * -1
        return res

    def visitNumericLiteral(self, ctx: XQueryParser.NumericLiteralContext):
        res = ctx.IntegerLiteral()
        if res is not None:
            return int(ctx.getText())
        res = ctx.DoubleLiteral()
        if res is not None:
            return float(ctx.getText())
        res = ctx.DecimalLiteral()
        if res is not None:
            return Decimal(ctx.getText())
        return ctx.getText()

    def visitStringLiteral(self, ctx: XQueryParser.StringLiteralContext):
        if ctx.stringLiteralQuot() is not None:
            # for item in ctx.stringLiteralQuot().stringContentQuot():
            result = ''
            for stringContext in ctx.stringLiteralQuot().children:
                str_Quot = stringContext.getText()
                if str_Quot == '"':
                    continue
                if str_Quot == '""':
                    str_Quot = '"'
                result = result + str(str_Quot)
            return result
        if ctx.stringLiteralApos() is not None:
            result = ''
            for stringContext in ctx.stringLiteralApos().stringContentApos():
                str_Quot = stringContext.getText()
                if str_Quot == "'":
                    continue
                result = result + str_Quot
            return result
        return self.visitChildren(ctx)

    def visitIntersectExceptExpr(self,
                                 ctx: XQueryParser.IntersectExceptExprContext):
        if ctx.KW_INTERSECT() and len(ctx.KW_INTERSECT()) >= 1:
            result = None
            for exp in ctx.instanceOfExpr():
                result_partial = self.visitInstanceOfExpr(exp)
                result = DrbQueryFuncUtil.intersect(result_partial,
                                                    result)
            return result
        elif ctx.KW_EXCEPT() and len(ctx.KW_EXCEPT()) >= 1:
            result = None
            for exp in ctx.instanceOfExpr():
                result_partial = self.visitInstanceOfExpr(exp)

                result = DrbQueryFuncUtil.except_op(result_partial,
                                                    result)
            return result
        else:
            return self.visitChildren(ctx)

    def visitUnionExpr(self, ctx: XQueryParser.UnionExprContext):
        if len(ctx.intersectExceptExpr()) <= 1:
            return self.visitChildren(ctx)

        result = None
        for exp in ctx.intersectExceptExpr():
            res_partial = self.visitIntersectExceptExpr(exp)
            result = DrbQueryFuncUtil.union(res_partial, result)
        return result

    def visitMultiplicativeExpr(self,
                                ctx: XQueryParser.MultiplicativeExprContext):
        if len(ctx.unionExpr()) <= 1:
            return self.visitChildren(ctx)

        operation = None

        res_final = None
        n = ctx.getChildCount()
        for i in range(n):

            c = ctx.getChild(i)
            if isinstance(c, TerminalNodeImpl):
                operation = c.getText()
            elif isinstance(c, XQueryParser.UnionExprContext):
                left_part = self.visitUnionExpr(c)
                operand_left = DrbQueryFuncUtil.get_numeric_value(
                    left_part, True)

                if operand_left is None:
                    if res_final is None:
                        raise StaticException(ErrorXQUERY.XPST0003,
                                              "first opreand of "
                                              "Multiplicative Exp "
                                              "must be numeric")
                    else:
                        operand_left = 0

                if res_final is None:
                    res_final = operand_left
                elif operation == '*':
                    res_final = res_final * operand_left
                elif operation == 'mod':
                    res_final = res_final % operand_left
                elif operation == 'div':
                    # Manage div by zero
                    if operand_left == 0:
                        # if float can return inf or -inf
                        if isinstance(res_final, float) \
                                or isinstance(operand_left, float):
                            if res_final == 0:
                                res_final = float('nan')
                            elif res_final > 0:
                                res_final = float('inf')
                            else:
                                res_final = float('-inf')
                        # otherwise, it is an error
                        else:
                            raise DynamicException(ErrorXQUERY.FOAR0001,
                                                   " Try to divide "
                                                   + str(res_final)
                                                   + " by zero")
                    else:
                        res_final = res_final / operand_left
                # int div
                elif operation == 'idiv':
                    if operand_left == 0:
                        raise DynamicException(ErrorXQUERY.FOAR0001,
                                               " Try to divide "
                                               + str(res_final)
                                               + " by zero")
                    else:
                        res_final = res_final // operand_left

        return res_final

    def visitAdditiveExpr(self, ctx: XQueryParser.AdditiveExprContext):
        if len(ctx.multiplicativeExpr()) <= 1:
            return self.visitChildren(ctx)

        operation = None

        res_final = None
        n = ctx.getChildCount()
        for i in range(n):

            c = ctx.getChild(i)
            if isinstance(c, TerminalNodeImpl):
                operation = c.getText()
            elif isinstance(c, XQueryParser.MultiplicativeExprContext):
                left_part = self.visitMultiplicativeExpr(c)
                operand_left = DrbQueryFuncUtil.get_numeric_value(left_part,
                                                                  True)

                if res_final is None:
                    res_final = operand_left
                elif operation == '+':
                    res_final = res_final + operand_left
                elif operation == '-':
                    res_final = res_final - operand_left

        return res_final

    def visitAbbrevReverseStep(self,
                               ctx: XQueryParser.AbbrevReverseStepContext):
        if ctx.DDOT() is not None:
            self.current_axe.is_parent = True

        return ''

    def visitAbbrevForwardStep(self,
                               ctx: XQueryParser.AbbrevForwardStepContext):
        at = ctx.AT()
        res = ''
        if at is not None:
            res = str(at)
            self.current_axe.is_attribute = True
            self.current_axe.is_node = False

        name = self.visitChildren(ctx)
        if name is not None:
            res = res + name

        return res

    def visitEqName(self, ctx: XQueryParser.EqNameContext):
        return self.visitChildren(ctx)

    def visitNameTest(self, ctx: XQueryParser.NameTestContext):
        if ctx.wildcard() is not None:
            self.current_axe.is_wildcard = True
            return '*'
        return self.visitChildren(ctx)

    def visitQName(self, ctx: XQueryParser.QNameContext):
        if ctx.ncName() is not None:
            return self.visitChildren(ctx)

        if ctx.FullQName() is not None:
            test = ctx.getText().split(':')

            prefix_namespace = test[0]
            self.current_axe.set_namespace_full(
                self.get_namespace_full_name(
                    prefix_namespace), prefix_namespace)
            self.current_axe.name = test[1]

            return ctx.getText()

        return self.visitChildren(ctx)

    def visitNcName(self, ctx: XQueryParser.NCName):
        self.current_axe.name = ctx.getText()

        return ctx.getText()

    def visitRangeExpr(self, ctx: XQueryParser.RangeExprContext):
        if ctx.KW_TO() is None:
            return self.visitChildren(ctx)

        left = self.visitAdditiveExpr(ctx.additiveExpr(0))
        right = self.visitAdditiveExpr(ctx.additiveExpr(1))

        left = DrbQueryFuncUtil.get_numeric_value(left)
        right = DrbQueryFuncUtil.get_numeric_value(right)

        res = list(range(left, right + 1))
        return res

    def visit_the_list_of_predicate(self,  predicate_list, context_list):
        self.static_context.is_in_predicate = True
        result = context_list
        for predicate_exp in predicate_list:
            res_predicate = self.visitPredicateContext(predicate_exp,
                                                       context_list)
            result = []

            DrbQueryVisitor.append_object_or_index(
                context_list, res_predicate, result)

            context_list = result
        self.static_context.is_in_predicate = False
        return result

    def visitCommonContent(self, ctx: XQueryParser.CommonContentContext):
        if ctx.expr() is not None:
            res = self.visitExpr(ctx.expr())
        else:
            res = html.unescape(ctx.getText())
            res = res.replace("{{", "{")
            res = res.replace("}}", "}")

        return res

    def visitDirAttributeValueApos(self, ctx: XQueryParser.
                                   DirAttributeValueAposContext):
        result = ''
        index = 0
        if ctx.children is not None:
            for item in ctx.children:
                index = index + 1

                if isinstance(item,
                              XQueryParser.DirAttributeContentQuotContext) \
                        and item.expr() is not None:
                    result = result + \
                             DrbQueryFuncUtil.get_string(
                                 self.visitExpr(item.expr()))
                else:
                    if not ((index == 1 or index == len(ctx.children)) and
                            (item.getText() == '"' or item.getText() == "'")):
                        result = result + item.getText()
        if result.find('<') >= 0:
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "char '<' can not be in attributes values")
        return result

    def visitDirAttributeValueQuot(self, ctx: XQueryParser.
                                   DirAttributeValueQuotContext):
        result = ''
        index = 0

        if ctx.children is not None:
            for item in ctx.children:
                index = index + 1

                if isinstance(item,
                              XQueryParser.DirAttributeContentAposContext) \
                        and item.expr() is not None:
                    result = result + \
                             DrbQueryFuncUtil.get_string(
                                 self.visitExpr(item.expr()))
                else:
                    if not ((index == 1 or index == len(ctx.children)) and
                            (item.getText() == '"' or item.getText() == "'")):
                        result = result + item.getText()
        if result.find('<') >= 0:
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "char '<' can not be in attributes values")
        return result

    def getAttributeValueList(self,
                              ctx: XQueryParser.DirAttributeListContext,
                              node: DrbXqueryItem):
        attributes: Dict[Tuple[str, str], Any] = {}
        if ctx.children is not None:
            attribute_full_name = ''
            for item in ctx.children:
                if isinstance(item, XQueryParser.QNameContext):
                    attribute_full_name = self.visitQName(item)
                elif isinstance(item, XQueryParser.DirAttributeValueContext):
                    namespace, attribute_name = DrbQueryFuncUtil.\
                        split_namespace_name(attribute_full_name)
                    value_attribute = self.visitDirAttributeValue(item)

                    if namespace == 'xmlns':
                        ns_full = value_attribute.strip('"')
                        self.dynamic_context.add_namespace(
                            self.static_context,
                            attribute_name,
                            ns_full)
                    else:
                        if attribute_name == 'xmlns':
                            if node.namespace_uri is None \
                                    or len(node.namespace_uri) == 0:
                                node.namespace_uri = value_attribute.\
                                    strip('"')
                                NamespaceMap.check_is_predefined_namespace(
                                    None, node.namespace_uri)

                                self.dynamic_context.namespace_default_elt = \
                                    node.namespace_uri
                        else:
                            if namespace is not None:
                                namespace = self.\
                                    get_namespace_full_name(namespace)
                            attributes[attribute_name, namespace] = \
                                value_attribute
        return attributes

    def visitNoQuotesNoBracesNoAmpNoLAng(self,
                                         ctx:
                                         XQueryParser.
                                         NoQuotesNoBracesNoAmpNoLAngContext):
        result = ''
        index_previous = ctx.start.tokenIndex - 1

        if self.tokens is not None:
            previous = self.tokens.get(index_previous)
            while previous.channel == 2:
                result = previous.text + result
                index_previous = index_previous - 1
                previous = self.tokens.get(index_previous)

            for index in range(ctx.start.tokenIndex, ctx.stop.tokenIndex+1):
                test_tokens = self.tokens.get(index)
                result = result + test_tokens.text

            index_after = ctx.stop.tokenIndex+1
            after = self.tokens.get(index_after)
            while after.channel == 2:
                result = result + after.text
                index_after = index_after + 1
                after = self.tokens.get(index_after)
        result = html.unescape(result)

        return result

    def visitDirElemContent(self, ctx: XQueryParser.DirElemContentContext):
        if ctx.noQuotesNoBracesNoAmpNoLAng() is not None:
            return self.visitNoQuotesNoBracesNoAmpNoLAng(
                ctx.noQuotesNoBracesNoAmpNoLAng())
        elif ctx.directConstructor() is not None:
            return self.visitDirectConstructor(ctx.directConstructor())
        # elif ctx.CDATA() is not None:
        #     node = XmlNode(XML(ctx.getText()))
        #     return DynamicContext(node)
        return self.visitChildren(ctx)

    def get_elem_cons_name_and_attributes(self, ctx, q_name: str):
        (namespace, name) = DrbQueryFuncUtil. \
            split_namespace_name(q_name)

        namespace_full = None
        node = DrbXqueryItem(None, name, namespace, namespace_full)
        self.dynamic_context = DynamicContext(
            node, dynamic_context_prev=self.dynamic_context)

        if ctx.dirAttributeList() is not None:
            attributes_node = self.getAttributeValueList(
                ctx.dirAttributeList(), node)
            for key in attributes_node.keys():
                node @= (key[0], key[1], attributes_node[key])

        if namespace is not None:
            node.namespace_uri = self.get_namespace_full_name(namespace)
        elif node.namespace_uri is None and \
                len(self.dynamic_context.namespace_default_elt) > 0:
            node.namespace_uri = self.dynamic_context.namespace_default_elt

        return node

    def visitDirElemConstructorOpenClose(self, ctx: XQueryParser.
                                         DirElemConstructorOpenCloseContext):
        if len(ctx.qName()) == 0:
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "Name expected for direct contructor")

        dynamic_context_old = self.dynamic_context

        q_name = ctx.qName(0).getText()
        if len(ctx.qName()) > 1:
            q_name_end = ctx.qName(1).getText()
            if q_name_end != q_name:
                raise StaticException(ErrorXQUERY.XPST0003,
                                      "The name " + q_name + " of element " +
                                      " tag constructor  differ " +
                                      q_name_end)

        node = self.get_elem_cons_name_and_attributes(ctx, q_name)

        value = None
        for item in ctx.dirElemContent():
            result_value = self.visitDirElemContent(item)
            if not isinstance(result_value, list):
                result_value = [result_value]

            value_content = None
            for item_value in result_value:
                node.order_elt.append(item_value)
                if isinstance(item_value, DrbNode):
                    node[None] = item_value
                if isinstance(item_value, DynamicContext):
                    if item_value.is_attribute():
                        node @= (
                            item_value.name,
                            item_value.namespace_uri,
                            item_value.value
                        )
                    else:
                        node[None] = item_value.node
                elif value_content is None:
                    value_content = item_value
                else:
                    value_content = \
                        DrbQueryFuncUtil.get_string(value_content) + ' ' + \
                        DrbQueryFuncUtil.get_string(item_value)

            if value_content is not None:
                if value is None:
                    value = value_content
                else:
                    value = DrbQueryFuncUtil.get_string(value) + \
                            DrbQueryFuncUtil.get_string(value_content)
        node.value = value

        context_to_return = self.dynamic_context

        self.dynamic_context = dynamic_context_old

        return context_to_return

    def visitDirElemConstructorSingleTag(self, ctx: XQueryParser.
                                         DirElemConstructorSingleTagContext):
        if ctx.qName() is None:
            return ''
        dynamic_context_old = self.dynamic_context

        node = self.get_elem_cons_name_and_attributes(ctx,
                                                      ctx.qName().getText())

        context_to_return = self.dynamic_context
        self.dynamic_context = dynamic_context_old

        return context_to_return

    def visitDirectConstructor(self, ctx: XQueryParser.
                               DirectConstructorContext):
        if self.dynamic_context.namespace_default_elt is None or \
                len(self.dynamic_context.namespace_default_elt) == 0:
            self.dynamic_context.namespace_default_elt = \
                self.static_context.namespace_default_elt

        if ctx.dirElemConstructorSingleTag() is not None:
            result = self.visitDirElemConstructorSingleTag(
                ctx.dirElemConstructorSingleTag())
        elif ctx.dirElemConstructorOpenClose() is not None:
            result = self.visitDirElemConstructorOpenClose(
                ctx.dirElemConstructorOpenClose())
        else:
            if ctx.getText().startswith('<!--') and\
                    ctx.getText().endswith('-->'):
                return None
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "unable to find constructor" + ctx.getText())

        return result

    def visitContextItemExpr(self, ctx: XQueryParser.ContextItemExprContext):
        if ctx.DOT() is not None:
            return self.dynamic_context
        return self.visitChildren(ctx)

    def visitPredicate(self, ctx: XQueryParser.PredicateContext):
        return self.visitPredicateContext(ctx, self.list_context)

    def visitPredicateContext(self,
                              ctx: XQueryParser.PredicateContext,
                              list_context):
        # visitor = DrbQueryVisitor(self.dynamic_context, self.position)
        result = []
        index = 0
        for node in list_context:
            if isinstance(node, DynamicContext):
                nodeToVisit = node
            else:
                nodeToVisit = DynamicContext(node)

            nodeToVisit.size_context = len(list_context)
            nodeToVisit.position = index + 1

            visitor_exp = DrbQueryVisitor(nodeToVisit,
                                          static_context=self.static_context,
                                          external_var_map=self.
                                          external_var_map,
                                          tokens=self.tokens)
            res_partial = visitor_exp.visitExpr(ctx.expr())
            index = index + 1

            if isinstance(res_partial, list):
                if len(res_partial) > 0:
                    if isinstance(res_partial[0], DrbNode):
                        result.append(node)
                    elif isinstance(res_partial[0], DynamicContext) and \
                            res_partial[0].is_node():
                        result.append(node)
                    elif isinstance(res_partial[0], DynamicContext) and \
                            res_partial[0].is_attribute():
                        result.append(node)
                    else:
                        list_numeric = [s for s in res_partial
                                        if isinstance(s,
                                                      (int, float, Decimal))]
                        if len(list_numeric) == len(res_partial):
                            if index in res_partial:
                                result.append(node)
                        else:
                            raise DynamicException(
                               ErrorXQUERY.FORG0006,
                               "A sequence staring by other than "
                               "a node can not be used as predicate result")

            elif isinstance(res_partial, bool):
                if res_partial:
                    result.append(node)
            elif isinstance(res_partial, (int, float, Decimal)):
                if index == res_partial:
                    result.append(node)
            elif isinstance(res_partial, str):
                if len(res_partial) > 0:
                    result.append(node)
            elif res_partial is not None:
                result.append(node)

        return result

    def visitExprForName(self, ctx: XQueryParser.ExprContext):
        result = self.visitExpr(ctx)
        return DrbQueryFuncUtil.get_name_in_result(result)

    def visitExpr(self, ctx: XQueryParser.ExprContext):
        if ctx.COMMA() is None or len(ctx.COMMA()) == 0:
            return self.visitChildren(ctx)

        result = []

        list_context = self.list_context
        for single_exp in ctx.exprSingle():
            res_partial = self.visitExprSingle(single_exp)
            self.append_or_extend(res_partial, result)
            self.list_context = list_context
        return result

    # Visit a parse tree produced by XQueryParser#parenthesizedExpr.
    def visitParenthesizedExpr(self,
                               ctx: XQueryParser.ParenthesizedExprContext):
        if ctx.expr() is not None:
            return self.visitExpr(ctx.expr())
        return []

    def visitPostfixExpr(self, ctx: XQueryParser.PostfixExprContext):
        if len(ctx.predicate()) == 0:
            return self.visitChildren(ctx)

        result = self.visitPrimaryExpr(ctx.primaryExpr())

        predicate_list = ctx.predicate()
        if predicate_list is not None and len(predicate_list) > 0:
            if isinstance(result, list):
                list_context = result
            else:
                list_context = [result]

            result = self.visit_the_list_of_predicate(predicate_list,
                                                      list_context)

        return result

    def visitForwardAxis(self, ctx: XQueryParser.ForwardAxisContext):
        if ctx.KW_CHILD() is not None:
            self.current_axe.navigation_step = NavigationStep.CHILD
            return ''
        if ctx.KW_ATTRIBUTE() is not None:
            self.current_axe.is_attribute = True
            self.current_axe.is_node = False
            return ''
        if ctx.KW_DESCENDANT_OR_SELF():
            self.current_axe.navigation_step = \
                NavigationStep.DESCENDANT_OR_SELF
            return ''
        if ctx.KW_DESCENDANT():
            self.current_axe.navigation_step = \
                NavigationStep.DESCENDANT
            return ''
        raise NotImplementedError(
            'Unsupported Axis operator :' + ctx.getText())

    def visitReverseAxis(self, ctx: XQueryParser.ReverseAxisContext):
        if ctx.KW_PARENT() is not None:
            self.current_axe.is_parent = True
            return ''

        raise NotImplementedError(
            'Unsupported Axis operator :' + ctx.getText())

    @staticmethod
    def get_attributes_node(node, name, namespace, list_result):
        try:
            value_attr = node.get_attribute(
                name,
                namespace)

            return value_attr
        except Exception as Error:
            pass
        return None

    @staticmethod
    def get_attributes(node, current_axe, list_result):
        if current_axe.is_wildcard:
            for key in node.attributes.keys():
                list_result.append(
                    DynamicContext(key, value=node.attributes[key],
                                   parent=node,
                                   attribute=True,
                                   position=len(list_result) + 1))
        else:
            name_attribute = current_axe.name
            namespace_attribute = current_axe.namespace
            value_attr = DrbQueryVisitor.get_attributes_node(
                node,
                name_attribute,
                namespace_attribute,
                list_result)
            if value_attr is None and namespace_attribute is not None and \
                    not current_axe.namespace_resolved and \
                    not isinstance(node, XmlNode):
                name_attribute = namespace_attribute + ':' + name_attribute
                namespace_attribute = None
                value_attr = DrbQueryVisitor.get_attributes_node(
                    node,
                    name_attribute,
                    namespace_attribute,
                    list_result)

            if value_attr is not None:
                list_result.append(DynamicContext(
                    (name_attribute, namespace_attribute),
                    value=value_attr, parent=node,
                    attribute=True,
                    position=len(list_result) + 1))

        return list_result

    @staticmethod
    def get_children_node(node, name, namespace):
        try:
            if node.has_child(name, namespace):
                if isinstance(node, DrbXqueryItem):
                    return node.get_named_child_list(name, namespace)
                else:

                    return node[name, namespace, :]
        except Exception:
            pass
        return []

    @staticmethod
    def get_children(node, current_axe, list_result,
                     static_context: StaticContext):
        next_nodes = []
        if current_axe.is_wildcard:
            next_nodes = node.children
        else:
            next_nodes = DrbQueryVisitor.get_children_node(
                node,
                current_axe.name,
                current_axe.namespace)
            if len(next_nodes) == 0 and \
                    current_axe.namespace is not None and \
                    not current_axe.namespace_resolved and \
                    not isinstance(node, XmlNode):
                child_name = current_axe.namespace + ':' + current_axe.name
                next_nodes = DrbQueryVisitor.get_children_node(
                    node, child_name, None)
        if static_context is not None:
            static_context.list_children_open.extend(next_nodes)
        for node_drb in next_nodes:
            list_result.append(DynamicContext(
                node_drb,
                position=len(list_result) + 1))

        return list_result

    def get_descendant(self, node, current_axe, result, or_self):
        children_of_node = node.children
        if self.current_axe.is_attribute:
            if or_self:
                self.get_attributes(node, current_axe, result)
        else:
            self.get_children(node, self.current_axe, result,
                              self.static_context)

        for child in children_of_node:
            result = self.get_descendant(child, current_axe, result, True)
        return result

    def visitAxisStep(self, ctx: XQueryParser.AxisStepContext):
        list_result = []
        self.current_axe = AxeNode(self.current_axe.navigation_step)

        if ctx.reverseStep() is not None:
            self.visitReverseStep(ctx.reverseStep())
        if ctx.forwardStep() is not None:
            self.visitForwardStep(ctx.forwardStep())

        for context in self.list_context:
            if context is None:
                continue
                # raise DynamicException(ErrorXQUERY.XPTY0020, "Error ")
            if isinstance(context, DynamicContext):
                node = context.node
            else:
                node = context
            next_nodes = []

            if self.current_axe.is_parent:
                if isinstance(node, DrbNode):
                    parent = node.parent
                else:
                    parent = context.parent

                if parent is not None:
                    list_result.append(DynamicContext(
                        parent,
                        position=len(list_result) + 1))
                continue

            if not isinstance(node, DrbNode):
                raise DynamicException(ErrorXQUERY.XPTY0020, "Error ")

            try:
                if self.current_axe.navigation_step == NavigationStep.\
                        DESCENDANT_OR_SELF:
                    if self.current_axe.is_wildcard or \
                            self.current_axe.name == node.name and \
                            (self.current_axe.namespace is None or
                             self.current_axe.namespace == node.namespace_uri):
                        list_result.append(DynamicContext(
                            node,
                            position=len(list_result) + 1))
                    self.get_descendant(node,
                                        self.current_axe,
                                        list_result,
                                        or_self=True)
                elif self.current_axe.navigation_step == NavigationStep. \
                        DESCENDANT:
                    self.get_descendant(node,
                                        self.current_axe,
                                        list_result,
                                        or_self=False)
                elif self.current_axe.is_attribute:
                    self.get_attributes(node, self.current_axe, list_result)
                elif self.current_axe.navigation_step == NavigationStep.CHILD:
                    self.get_children(node, self.current_axe, list_result,
                                      self.static_context)
            except Exception as Error:
                # no  node or attribute with this name.
                pass
        list_node_to_test = list_result

        list_predicate = ctx.predicateList()

        if len(list_node_to_test) == 0:
            return []
        if list_predicate is not None:
            list_result = self.visit_the_list_of_predicate(
                list_predicate.predicate(), list_node_to_test
            )

        return list_result

    # Visit a parse tree produced by XQueryParser#relativePathExpr.
    def visitRelativePathExpr(self, ctx: XQueryParser.RelativePathExprContext):
        if (ctx.SLASH is None or len(ctx.SLASH()) == 0) and \
                (ctx.DSLASH() is None or len(ctx.DSLASH()) == 0):
            return self.visitChildren(ctx)

        result = []
        step_nav = NavigationStep.CHILD

        for exp in ctx.children:
            if isinstance(exp, TerminalNodeImpl):
                if exp.getText() == '/':
                    step_nav = NavigationStep.CHILD
                elif exp.getText() == '//':
                    step_nav = NavigationStep.DESCENDANT_OR_SELF
            elif isinstance(exp, XQueryParser.StepExprContext):
                result = []
                index = 0
                for node in self.list_context:
                    if not isinstance(node, DynamicContext):
                        node = DynamicContext(node=node)

                    visitor_exp = DrbQueryVisitor(
                        node, step_nav=step_nav,
                        static_context=self.static_context,
                        external_var_map=self.external_var_map,
                        tokens=self.tokens)
                    result_partial = visitor_exp.visitStepExpr(exp)
                    index = index + 1
                    if result_partial is not None:
                        if isinstance(result_partial, list):
                            result.extend(result_partial)
                        else:
                            result.append(result_partial)

                self.list_context = result
        return result

        # Visit a parse tree produced by XQueryParser#enclosedContentExpr.

    def visitEnclosedExpression(self,
                                ctx: XQueryParser.EnclosedExpressionContext):
        if ctx.expr() is not None:
            return self.visitExpr(ctx.expr())
        return self.visitChildren(ctx)

    def visitCompAttrConstructor(self,
                                 ctx: XQueryParser.CompAttrConstructorContext):
        if ctx.KW_ATTRIBUTE() is None:
            return self.visitChildren(ctx)

        name = None
        if ctx.eqName() is not None:
            name = self.visitEqName(ctx.eqName())
        elif ctx.expr() is not None:
            name = self.visitExprForName(ctx.expr())
        if name is None:
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "Comp attribute with no name in " +
                                  ctx.getText())

        (namespace, name) = DrbQueryFuncUtil.split_namespace_name(name)

        value_attr = None
        if ctx.enclosedExpression() is not None:
            value_attr = self.visitEnclosedExpression(
                ctx.enclosedExpression())
            value_attr = DrbQueryFuncUtil.get_string(value_attr)

        if namespace is not None:
            namespace = self.get_namespace_full_name(namespace)

        return DynamicContext((name, namespace), value=value_attr,
                              namespace=namespace,
                              attribute=True)

    def visitCompElemConstructor(
            self, ctx: XQueryParser.CompElemConstructorContext):
        if ctx.KW_ELEMENT() is None:
            return self.visitChildren(ctx)
        name = None
        if ctx.eqName() is not None:
            name = self.visitEqName(ctx.eqName())
        elif ctx.expr() is not None:
            name = self.visitExprForName(ctx.expr())

        if name is None:
            raise StaticException(ErrorXQUERY.XPST0003,
                                  "Comp element with no name in " +
                                  ctx.getText())

        (namespace, name) = DrbQueryFuncUtil.split_namespace_name(name)
        namespace_full = None
        if namespace is not None:
            namespace_full = self.get_namespace_full_name(namespace)
        elif len(self.dynamic_context.namespace_default_elt) > 0:
            namespace_full = self.dynamic_context.namespace_default_elt
        node = DrbXqueryItem(None, name, namespace, namespace_full)

        if ctx.enclosedContentExpr() is not None:
            result = self.visitEnclosedContentExpr(ctx.enclosedContentExpr())
            if not isinstance(result, list):
                result = [result]

            value_node = None
            for res_item in result:
                if isinstance(res_item, DynamicContext):
                    if res_item.is_node():
                        res_item.node.parent = self
                        node[None] = res_item
                    elif res_item.is_attribute():
                        node @= (
                            res_item.name,
                            res_item.namespace_uri,
                            res_item.value
                        )
                    else:
                        if value_node is None:
                            value_node = DrbQueryFuncUtil.get_value(
                                res_item)
                        else:
                            value_node = str(value_node) + \
                                         DrbQueryFuncUtil.get_string(
                                             res_item)

                else:
                    if value_node is None:
                        value_node = DrbQueryFuncUtil.get_value(res_item)
                    else:
                        value_node = str(value_node) + \
                                     DrbQueryFuncUtil.get_string(res_item)

            node.value = value_node
        return DynamicContext(node=node)

    def visitLetBinding(self, ctx: XQueryParser.LetBindingContext):
        var_namespace = None
        varname = self.visitVarName(ctx.varName())
        type_var = None

        if ctx.typeDeclaration() is not None:
            type_var = self.visitTypeDeclaration(ctx.typeDeclaration())

        for current_scope_flwor in self.flwor_scope_list:
            self.static_context.in_scope_variables = current_scope_flwor
            var_value = self.visitExprSingle(ctx.exprSingle())
            self.static_context.add_var(varname,
                                        XqueryVariable(varname,
                                                       var_namespace,
                                                       value=var_value,
                                                       type_var=type_var))

    def visitReturnClause(self, ctx: XQueryParser.ReturnClauseContext):
        if self.flwor_scope_list is None:
            return self.visitChildren(ctx)

        result = []

        for current_scope_flwor in self.flwor_scope_list:
            self.static_context.in_scope_variables = current_scope_flwor
            self.list_context = [self.dynamic_context]

            res_partial = self.visitChildren(ctx)
            DrbQueryFuncUtil.append_or_extend(res_partial, result)

        return result

    def visitForBinding(self, ctx: XQueryParser.ForBindingContext):
        if self.flwor_scope_list is None:
            return self.visitChildren(ctx)

        list_context = self.list_context
        var_name = self.visitVarName(ctx.varName())

        # TODO Type declaration
        type_var = None
        if ctx.typeDeclaration() is not None:
            type_var = self.visitTypeDeclaration(ctx.typeDeclaration())

        scope_new = []

        var_position = None
        if ctx.positionalVar() is not None:
            var_position = self.visitVarName(ctx.positionalVar().varName())

        for scope in self.flwor_scope_list:
            self.static_context.in_scope_variables = scope
            ret_partial = self.visitExprSingle(ctx.exprSingle())
            key_name = self.static_context.get_key_var(var_name)

            if isinstance(ret_partial, list):
                index = 1
                for item in ret_partial:
                    current_scope = scope.copy()
                    current_scope[key_name] = XqueryVariable(
                        var_name,
                        value=item,
                        type_var=type_var)
                    if var_position is not None:
                        current_scope[None, var_position] = XqueryVariable(
                            var_position, value=index, type_var=type_var)
                    scope_new.append(current_scope)
                    index = index + 1
            else:
                current_scope = scope.copy()
                current_scope[key_name] = XqueryVariable(
                    var_name,
                    value=ret_partial,
                    type_var=type_var)
                scope_new.append(current_scope)
            self.list_context = list_context

        self.flwor_scope_list = scope_new

        return ''

    def visitWhereClause(self, ctx: XQueryParser.WhereClauseContext):
        if self.flwor_scope_list is None:
            return self.visitChildren(ctx)

        scope_new = []

        for scope in self.flwor_scope_list:
            self.static_context.in_scope_variables = scope
            ret_partial = self.visitExprSingle(ctx.exprSingle())
            if DrbQueryFuncUtil.get_effective_boolean_value(ret_partial):
                scope_new.append(scope)
        self.flwor_scope_list = scope_new

    # Visit a parse tree produced by XQueryParser#flworExpr.
    def visitFlworExpr(self, ctx: XQueryParser.FlworExprContext):
        old_scop = self.static_context.in_scope_variables
        old_context = self.list_context
        old_scope_list = self.flwor_scope_list

        self.flwor_scope_list = [old_scop.copy()]

        res = self.visitChildren(ctx)

        self.flwor_scope_list = old_scope_list
        self.static_context.in_scope_variables = old_scop
        self.list_context = old_context
        return res

    def visitIfExpr(self, ctx: XQueryParser.IfExprContext):
        if ctx.KW_IF is None:
            return self.visitChildren(ctx)

        visitor = DrbQueryVisitor(self.dynamic_context,
                                  static_context=self.static_context,
                                  external_var_map=self.external_var_map,
                                  tokens=self.tokens)
        res = visitor.visitExpr(ctx.expr())
        if DrbQueryFuncUtil.get_effective_boolean_value(res):
            return self.visitExprSingle(ctx.thenExpr)
        else:
            return self.visitExprSingle(ctx.elseExpr)

    def visitInstanceOfExpr(self, ctx: XQueryParser.InstanceOfExprContext):
        if ctx.sequenceType() is None:
            return self.visitChildren(ctx)

        node = self.visitTreatExpr(ctx.treatExpr())
        if not isinstance(node, list):
            node = [node]

        type = self.visitSequenceType(ctx.sequenceType())
        (type_ns, type_name) = DrbQueryFuncUtil.split_namespace_name(type)
        if type_ns == 'xs' or type_ns is None:
            for item in node:
                if not DrbQueryFuncCall.xs_instance_func[type_name](
                        type_name, None, None, item):
                    return False
            return True

        return False


class DrbXqueryParserErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise StaticException(ErrorXQUERY.XPST0003,
                              "ERROR: when parsing " + str(offendingSymbol) +
                              " line " + str(line) +
                              " column " + str(column) + " : " + msg)
