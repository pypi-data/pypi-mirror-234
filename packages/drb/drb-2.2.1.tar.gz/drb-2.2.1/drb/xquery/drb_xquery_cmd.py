import io

import click
import drb.topics.resolver as resolver

from drb.xquery.drb_xquery_res_to_string import XQueryResToString
from drb.xquery.drb_xquery_utils import DrbQueryFuncUtil
from drb.xquery.drb_xquery_variable import XqueryVariable
from .drb_xquery import DrbXQuery


class OptionEatAll(click.Option):

    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(OptionEatAll, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or \
                         parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


@click.command()
@click.option('-s', '--string',
              default='',
              help=' Command line string to be evaluated as XQuery script. '
                   'This parameter cannot be used jointly with -f. '
                   'At least -s or -f is to be set.')
@click.option('-f',
              '--file',
              default='',
              help=' Path to a file containing the sctript to be evaluated. '
                   'This parameter cannot be used jointly '
                   'with -s. At least -f or -s is to be set..')
@click.option('-n',
              '--url-node',
              default='',
              help='Url to a node, in drb meaning, that give '
                   'the context of the query. It can be the path'
                   'of a xml file for example on which the xquery will'
                   'be executed')
@click.option('-V',
              '--verbose',
              is_flag=True)
@click.option('-v',
              '--variable',
              default=[],
              multiple=True,
              cls=OptionEatAll,
              help='Variable define -v <QName> <value> [ as <type>].'
                   'Pushes an external variable in the environment '
                   'prior to parse and evaluate the XQuery script. '
                   'The variable is pushed in the  the environment altough '
                   'it has not been declared has an external variable, '
                   'to provide it to the potential nested XQuerys '
                   '(e.g. a call to evaluate-uri() built-in function). '
                   '<QName> is the qualified name of the variable to declare '
                   'whether <value> is a string to bind as value '
                   'of the variable. '
                   'If <QName> matches a typed external variable '
                   'declared in the script, <value> is converted to that '
                   'type before being bound. '
                   'The trailing "as <type>" is optional and shall follow the '
                   'XQuery sequence type declaration (e.g. as xs:integer+ )')
def drb_xquery_cmd(string,
                   file,
                   variable,
                   url_node,
                   verbose):
    """This command evaluates the XQuery script provided as a string or
        a file. The output of the evaluation is printed out in the
        standard output. The output format may have several forms
        according to the resulting sequence. Basically the resulting
        nodes are output as XML fragments, the attributes not attached
        to nodes are written as in XML but prefixed with '@' symbol and
        finally, the atomic values are printed without decoration,
        according to the XML Schema lexical space definitions. All items
        of the output sequence are comma separated. A '()' result denotes
        the empty sequence.
        ."""

    if len(string) == 0 and len(file) == 0:
        ctx = click.get_current_context()
        ctx.fail("At least option query or query-file must be set")

    if len(string) > 0 and len(file) > 0:
        ctx = click.get_current_context()
        ctx.fail("Query and query url are mutually exclusive")

    node_query = None

    if len(file) > 0:
        if verbose:
            print('query_file :')
            print(file)
        node_query = resolver.create(file)
        buffer = node_query.get_impl(io.BufferedIOBase)
        string = buffer.read().decode('utf-8')
        buffer.close()

    node = None
    if len(url_node) > 0:
        node = resolver.create(url_node)

    variables = {}

    for var in variable:
        var = var.lstrip("(")
        var = var.rstrip(")")

        var_split = var.split(',')
        var = []
        for index in range(len(var_split)):
            var.append(var_split[index].strip(' ').strip("'"))
        if len(var) == 2:
            variables[var[0]] = var[1]
        elif len(var) != 4:
            ctx = click.get_current_context()
            ctx.fail("Typed variables " + str(var) + " is malformed")
        else:
            if var[2].lower() != 'as':
                ctx = click.get_current_context()
                ctx.fail("Typed variables " + str(var) + " is malformed")
            type_var_namespace, type_var = \
                DrbQueryFuncUtil.split_namespace_name(var[3])
            if type_var_namespace is None:
                type_var_namespace = 'xs'
            value = XqueryVariable.get_value_typed(type_var,
                                                   type_var_namespace,
                                                   var[1])
            variables[var[0]] = value

    if verbose:
        print('Query :')
        print(string)

        print('Variables :')
        print(variables)

    drb_query = DrbXQuery(string)
    res = drb_query.execute(node, **variables)
    if node:
        node.close()
    if node_query:
        node_query.close()
    first = True

    if isinstance(res, list) and (len(res)) == 0:
        print('()')
    else:
        for item in res:
            if first:
                first = False
            else:
                print(', ', end='')
            result_string = None
            result_string = XQueryResToString.add_item_to_result(
                result_string, item,
                context=drb_query.static_context)
            print(result_string, end='')
        print('')


if __name__ == '__main__':
    drb_xquery_cmd()
