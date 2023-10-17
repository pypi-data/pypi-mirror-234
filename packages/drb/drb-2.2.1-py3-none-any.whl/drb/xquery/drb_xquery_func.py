from .drb_xquery_item import DrbXqueryItem
from .drb_xquery_res_to_string import XQueryResToString
from .drb_xquery_utils import DrbQueryFuncUtil
from .execptions import DynamicException, ErrorXQUERY
from .drb_xquery_context import DynamicContext, StaticContext
from drb.core.node import DrbNode
from decimal import Decimal
from dateutil.parser import parse
import datetime
import math
import re
import drb.topics.resolver as resolver


def check_arg(func, number_expected, *args):
    if len(args) != number_expected:
        msg_error = func + " calls wtih " + str(len(args)) \
                    + " args instead of " + str(number_expected)
        raise DynamicException(ErrorXQUERY.FOAP0001, msg_error)


def is_int(arg_numeric):
    if arg_numeric[0] in ('-', '+'):
        return arg_numeric[1:].isnumeric()
    return arg_numeric.isnumeric()


def get_numeric_or_string(func, arg_numeric, other=None):
    arg_numeric = DrbQueryFuncUtil.get_value(arg_numeric)

    if isinstance(arg_numeric, (int, float, Decimal)):
        if other is not None:
            if isinstance(other, float):
                return float(arg_numeric)
            elif isinstance(other, str):
                raise DynamicException(ErrorXQUERY.FORG0006,
                                       func +
                                       " called with not numeric operand "
                                       + str(arg_numeric))
        return arg_numeric
    elif isinstance(arg_numeric, str):
        if other is not None and isinstance(other, (int, float, Decimal)):
            try:
                if is_int(arg_numeric):
                    return int(arg_numeric)
                # elif arg_numeric.isdigit():
                #     return Decimal(arg_numeric)
                else:
                    return float(arg_numeric)
            except Exception:
                raise DynamicException(ErrorXQUERY.FORG0006,
                                       func +
                                       " called with not numeric operand "
                                       + str(arg_numeric))
        else:
            return arg_numeric


def get_numeric(func, arg_numeric, other=None):
    arg_numeric = DrbQueryFuncUtil.get_value(arg_numeric)

    if isinstance(arg_numeric, (int, float, Decimal)):
        if other is not None and isinstance(other, float):
            return float(arg_numeric)
        else:
            return arg_numeric

    # if isinstance(arg_numeric, Decimal):
    #     return float(arg_numeric)
    elif isinstance(arg_numeric, str):
        try:
            if is_int(arg_numeric):
                return int(arg_numeric)
            # elif arg_numeric.isdigit():
            #     return Decimal(arg_numeric)
            else:
                return float(arg_numeric)
        except Exception:
            raise DynamicException(ErrorXQUERY.FORG0006,
                                   func + " called with not numeric operand "
                                   + str(arg_numeric))
    raise DynamicException(ErrorXQUERY.FORG0006,
                           func + " called with not numeric operand "
                           + str(arg_numeric))


def check_arg_max(func, number_max, *args):
    if len(args) > number_max:
        msg_error = func + " calls wtih " + str(len(args)) \
                    + " args"
        raise DynamicException(ErrorXQUERY.FOAP0001, msg_error)


def check_arg_min(func, number_min, *args):
    if len(args) < number_min:
        msg_error = func + " calls wtih " + str(len(args)) \
                    + " args"
        raise DynamicException(ErrorXQUERY.FOAP0001, msg_error)


def check_arg_min_max(func, number_min, number_max, *args):
    if len(args) > number_max or len(args) < number_min:
        msg_error = func + " calls wtih " + str(len(args)) \
                    + " args"
        raise DynamicException(ErrorXQUERY.FOAP0001, msg_error)


def doc(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if is_elt_empty(args[0]):
        return ''
    try:
        url_str = DrbQueryFuncUtil.get_string(args[0])
    except Exception:
        raise DynamicException(ErrorXQUERY.FODC0005, "Unable to get url "
                               + str(args[0]))

    try:
        node_doc = resolver.create(url_str)
    except Exception:
        try:
            signature, n = resolver.resolve(source=url_str)
        except Exception:
            raise DynamicException(ErrorXQUERY.FODC0005, "Unable to resolve :"
                                   + str(args[0]))
        try:
            node_doc = signature.factory.create(n)
            n.close()
        except Exception:
            raise DynamicException(ErrorXQUERY.FODC0002,
                                   "Unable to create node with url :"
                                   + str(args[0]))

    return DynamicContext(node_doc)


def current_date_time(func, current_node, static_context, *args):
    check_arg_max(func, 0, *args)

    return datetime.datetime.now()


def current_time(func, current_node, static_context, *args):
    check_arg_max(func, 0, *args)

    return datetime.datetime.now().time()


def data(func, current_node, static_context, *args):
    check_arg_max(func, 1, *args)

    if len(args) == 1:
        node_to_evaluate = args[0]
    else:
        node_to_evaluate = current_node

    if not isinstance(node_to_evaluate, list):
        node_to_evaluate = [node_to_evaluate]

    result = []
    for item in node_to_evaluate:
        value = DrbQueryFuncUtil.get_value(item)
        if value is None:
            raise DynamicException(ErrorXQUERY.FOTY0012,
                                   " Error " +
                                   DrbQueryFuncUtil.get_string(
                                       item) +
                                   " have no value")
        result.append(value)

    return result


def get_last(func, current_node, static_context):
    if current_node is None:
        raise DynamicException(ErrorXQUERY.XPDY0002, func)
    return current_node.size_context


def count(func, current_node, static_context, elt_to_count):
    if isinstance(elt_to_count, list):
        return len(elt_to_count)
    else:
        return 1


def get_position(func, current_node, static_context):
    if current_node is None:
        raise DynamicException(ErrorXQUERY.XPDY0002, func)
    return current_node.position


def get_name(func, current_node, static_context, elt=None):
    if elt is None:
        elt = current_node
    elif isinstance(elt, list):
        if len(elt) == 0:
            return ''
        elt = elt[0]

    if isinstance(elt, DynamicContext):
        if elt.is_node():
            elt = elt.node

    if isinstance(elt, DrbXqueryItem):
        if elt.prefix is not None and len(elt.prefix) > 0:
            return elt.prefix + ':' + elt.name
    elif isinstance(elt, (DrbNode, DynamicContext)):
        namespace = elt.namespace_uri
        if namespace is not None and len(namespace) > 0:
            ns = static_context.get_namespace_prefix_name(namespace)
            if ns is not None and len(ns) > 0:
                return ns + ':' + elt.name
    return elt.name


def get_namespace_uri(func, current_node, static_context, elt=None):
    if elt is None:
        elt = current_node
    elif isinstance(elt, list):
        if len(elt) > 0:
            elt = elt[0]
    if elt is None:
        raise DynamicException(ErrorXQUERY.XPDY0002, func)
    if not isinstance(elt, DynamicContext):
        raise DynamicException(ErrorXQUERY.XPTY0004,
                               func + " arg is not Node")
    if elt.namespace_uri is None:
        return ''

    if elt.is_node() or elt.is_attribute():
        return elt.namespace_uri
    return static_context.get_namespace_full_name(elt.namespace_uri)


def drb_xml(func, current_node, static_context, elt=None):
    if elt is None:
        elt = current_node
    elif isinstance(elt, list):
        if len(elt) == 0:
            return ''
        result = drb_xml(func, current_node, static_context, elt[0])
        for item in elt[1:]:
            result += ' ' + drb_xml(func, current_node, static_context, item)
        return result

    if isinstance(elt, DrbNode):
        return XQueryResToString.drb_node_to_xml(
            elt.node,
            namespace_declared=[],
            dynamic_context=None,
            context=static_context)
    elif isinstance(elt, DynamicContext):
        if elt.is_node():
            return XQueryResToString.drb_node_to_xml(
                elt.node,
                context=static_context,
                namespace_declared=[],
                dynamic_context=elt)
        elif elt.is_attribute():
            return XQueryResToString.drb_attribute_to_xml(
                elt,
                context=static_context,
                namespace_declared=[],
                dynamic_context=elt)
        elif elt.name is not None and len(elt.name) > 0:
            return f'<{elt.name}>{DrbQueryFuncUtil.get_string(elt)}' \
                     f'</{elt.name}>'

    return DrbQueryFuncUtil.get_string(elt)


def is_empty_list(elt1):
    if isinstance(elt1, list) and len(elt1) == 0:
        return True


def is_elt_empty(elt1):
    if elt1 is None:
        return True
    if isinstance(elt1, list) and len(elt1) == 0:
        return True


def starts_with(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return False
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])

    return str1.startswith(str2)


def ends_with(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return False
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])

    return str1.endswith(str2)


def contains(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]):
        return False
    if is_elt_empty(args[1]):
        return True
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])

    return str2 in str1


def substring(func, current_node, static_context, *args):
    check_arg_min_max(func, 2, 3, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return ''
    str1 = DrbQueryFuncUtil.get_string(args[0])
    start = DrbQueryFuncUtil.get_numeric_value(args[1])

    if isinstance(start, float) and math.isnan(start):
        return ''
    if start > len(str1):
        return ''
    if isinstance(start, float) and start == float('+inf'):
        return ''

    if len(args) == 3:
        len_sub = DrbQueryFuncUtil.get_numeric_value(args[2])
        if isinstance(len_sub, float) and math.isnan(len_sub):
            return ''

        if isinstance(start, float) and start == float('-inf'):
            return ''
        if not isinstance(len_sub, float) or not len_sub == float('inf'):
            end_pos = DrbQueryFuncUtil.get_round_int_value(len_sub)
            start_pos = DrbQueryFuncUtil.get_round_int_value(start)
            end_pos = start_pos + end_pos
            if end_pos < 1:
                return ''

            if start_pos < 1:
                start_pos = 1

            return str1[start_pos - 1:end_pos - 1]

    start_pos = DrbQueryFuncUtil.get_round_int_value(start)
    if start_pos < 1:
        start_pos = 1
    return str1[start_pos - 1:]


def substring_after(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return False
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])
    if len(str2) == 0:
        return str1

    list_sub = str1.split(str2, 1)
    if list_sub is None or len(list_sub) < 2:
        return ''

    return list_sub[1]


def substring_before(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return ''
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])
    if len(str2) == 0:
        return ''

    if str1.find(str2) < 0:
        return ''

    list_sub = str1.split(str2, 1)
    if list_sub is None or len(list_sub) < 1:
        return ''

    return list_sub[0]


def string_length(func, current_node, static_context, *args):
    if len(args) == 0:
        arg_one = current_node
    else:
        check_arg(func, 1, *args)
        arg_one = args[0]

    if is_elt_empty(arg_one):
        return 0
    str1 = DrbQueryFuncUtil.get_string(arg_one)

    return len(str1)


def string_join(func, current_node, static_context, *args):
    check_arg_min_max(func, 1, 2, *args)

    if not isinstance(args[0], list):
        return DrbQueryFuncUtil.get_string(args[0])

    if len(args[0]) == 0:
        return ''

    separator = ''
    if len(args) == 2 and args[1] is not None:
        separator = DrbQueryFuncUtil.get_string(args[1])
    str_result = None
    for arg_list in args[0]:
        str1 = DrbQueryFuncUtil.get_string(arg_list)
        if str_result is None:
            str_result = str1
        else:
            str_result = str_result + separator + str1

    return str_result


def string_concat(func, current_node, static_context, *args):
    check_arg_min(func, 2, *args)

    str_result = ''
    for arg_list in args:
        str1 = DrbQueryFuncUtil.get_string(arg_list)
        if str1 is not None and isinstance(str1, str):
            str_result = str_result + str1

    return str_result


def string_compare(func, current_node, static_context, *args):
    check_arg_min_max(func, 2, 3, *args)
    if len(args) == 3:
        raise DynamicException(ErrorXQUERY.FOCH0002,
                               " func " + func +
                               " not support collation")

    if is_empty_list(args[0]) or is_empty_list(args[1]):
        return []

    # if is_elt_empty(args[0]):
    #     if is_elt_empty(args[1]):
    #         return 0
    #     else:
    #         return -1
    # if is_elt_empty(args[1]):
    #     return 1
    str1 = DrbQueryFuncUtil.get_string(args[0])
    str2 = DrbQueryFuncUtil.get_string(args[1])

    if str1 > str2:
        return 1
    elif str1 < str2:
        return -1

    return 0


def lower_case(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    if is_empty_list(args[0]):
        return []

    str1 = DrbQueryFuncUtil.get_string(args[0])

    return str1.lower()


def upper_case(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    if is_empty_list(args[0]):
        return []

    str1 = DrbQueryFuncUtil.get_string(args[0])

    return str1.lower()


def string_tokenize(func, current_node, static_context, *args):
    check_arg_min_max(func, 1, 2, *args)
    if is_empty_list(args[0]):
        return ''

    str1 = DrbQueryFuncUtil.get_string(args[0])
    if len(str1) == 0:
        return ''

    pattern_string = ' '
    if len(args) == 2 and args[1] is not None:
        pattern_string = DrbQueryFuncUtil.get_string(args[1])
        if len(pattern_string) == 0:
            raise DynamicException(ErrorXQUERY.FORX0003,
                                   " func " + func +
                                   " regex:" + pattern_string)
    try:
        pattern = re.compile(pattern_string)
    except Exception:
        raise DynamicException(ErrorXQUERY.FORX0002,
                               " func " + func +
                               " regex:" + pattern_string)
    return pattern.split(str1)


def string_replace(func, current_node, static_context, *args):
    check_arg(func, 3, *args)
    if is_empty_list(args[0]):
        return ''

    str1 = DrbQueryFuncUtil.get_string(args[0])
    if len(str1) == 0:
        return ''

    pattern_string = DrbQueryFuncUtil.get_string(args[1])
    if len(pattern_string) == 0:
        raise DynamicException(ErrorXQUERY.FORX0003,
                               " func " + func +
                               " regex:" + pattern_string)

    str3 = DrbQueryFuncUtil.get_string(args[2])

    try:
        pattern = re.compile(pattern_string)
    except Exception:
        raise DynamicException(ErrorXQUERY.FORX0002,
                               " func " + func +
                               " regex:" + pattern_string)
    # str_match = pattern.match(str3)
    # if str_match is None or len(str_match.group(0)) == 0:
    #     raise DynamicException(ErrorXQUERY.FORX0003,
    #                            " func " + func +
    #                            " regex match zero string:" + pattern_string)

    str3 = DrbQueryFuncUtil.replace_group_regex_to_python(str3)

    return pattern.sub(str3, str1)


def return_true(func, current_node, static_context):
    return True


def return_false(func, current_node, static_context):
    return False


def return_boolean(func, current_node, static_context, elt1):
    return DrbQueryFuncUtil.get_boolean_value(elt1)


def return_not(func, current_node, static_context, elt1):
    return not return_boolean(func, current_node, static_context, elt1)


def matches(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if is_elt_empty(args[0]) or is_elt_empty(args[1]):
        return False
    source_string = DrbQueryFuncUtil.get_string(args[0])
    pattern_string = DrbQueryFuncUtil.get_string(args[1])

    try:
        pattern = re.compile(pattern_string)
    except Exception:
        raise DynamicException(ErrorXQUERY.FORX0002,
                               " regex:" + pattern_string)

    if pattern.fullmatch(source_string):
        return True
    else:
        return False


def exists(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if args[0] is None:
        return True

    if is_elt_empty(args[0]):
        return False

    return True


def empty(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if is_elt_empty(args[0]):
        return True

    return False


def reverse(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if isinstance(args[0], list):
        args[0].reverse()

    return args[0]


def distinct_value(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if isinstance(args[0], list):
        list_uniq_values = []

        for item in args[0]:
            value = DrbQueryFuncUtil.get_value(item)
            if value not in list_uniq_values:
                list_uniq_values.append(value)
        return list_uniq_values

    return DrbQueryFuncUtil.get_value(args[0])


def deep_equal(func, current_node, static_context, *args):
    check_arg(func, 2, *args)

    if isinstance(args[0], list):
        if not isinstance(args[1], list):
            return False

        if len(args[0]) != len(args[1]):
            return False
        for i in range(len(args[0])):
            if not deep_equal(func, current_node,
                              static_context,
                              args[0][i], args[1][i]):
                return False
        return True

    left_value, right_value = \
        DrbQueryFuncUtil.convert_before_compare(args[0],
                                                args[1])
    if not DrbQueryFuncUtil.is_equal(left_value, right_value):
        return False

    node1 = args[0]
    node2 = args[1]

    if isinstance(args[0], DynamicContext):
        if not isinstance(args[1], DynamicContext):
            return False
        if args[0].name != args[1].name:
            return False
        node1 = DrbQueryFuncUtil.get_node(args[0])
        node2 = DrbQueryFuncUtil.get_node(args[1])

    elif isinstance(args[1], DynamicContext):
        return False

    if isinstance(node1, DrbNode):
        try:
            if not isinstance(node2, DrbNode):
                return False

            if node1.name != node2.name:
                return False

            if len(node1.children) != len(node2.children):
                return False
            for index in range(len(node1.children)):
                child1 = node1[index]
                if not deep_equal(func,
                                  current_node,
                                  static_context,
                                  child1,
                                  node2[index]):
                    return False

            if len(node1.attributes) != len(node2.attributes):
                return False
            for attribute_key in node1.attributes.keys():
                if not deep_equal(func, current_node, static_context,
                                  node1.get_attribute(attribute_key[0],
                                                      attribute_key[1]),
                                  node2.get_attribute(attribute_key[0],
                                                      attribute_key[1])):
                    return False
        except Exception:
            return False
    elif isinstance(node2, DrbNode):
        return False
    return True


def extend_arg_from_list(*args):
    list_arg = []
    for arg_item in args:
        if isinstance(arg_item, list):
            list_arg.extend(arg_item)
        else:
            list_arg.append(arg_item)
    return list_arg


def average(func, current_node, static_context, *args):
    check_arg_min(func, 1, *args)

    if is_elt_empty(args[0]):
        return ''

    list_arg = extend_arg_from_list(*args)

    average_result = None
    index = 0
    for operand in list_arg:
        numeric = get_numeric(func, operand, average_result)
        index = index + 1
        if average_result is None:
            average_result = numeric
        else:
            average_result = average_result + numeric
    if average_result is None:
        return 0

    return average_result / index


def f_sum(func, current_node, static_context, *args):
    check_arg_min(func, 1, *args)

    if args[0] is None:
        return 0

    if is_elt_empty(args[0]) and len(args) == 1:
        return 0

    list_arg = extend_arg_from_list(*args)

    sum_result = None
    for operand in list_arg:
        if is_elt_empty(operand):
            continue
        numeric = get_numeric(func, operand, sum_result)
        if sum_result is None:
            sum_result = numeric
        else:
            sum_result = sum_result + numeric
    if sum_result is None:
        return []

    return sum_result


def xquery_max(func, current_node, static_context, *args):
    check_arg_min(func, 1, *args)

    if is_elt_empty(args[0]):
        return ''

    list_arg = extend_arg_from_list(*args)

    max_result = None
    for operand in list_arg:
        numeric = get_numeric_or_string(func, operand, max_result)
        if max_result is None or max_result < numeric:
            max_result = numeric

    return max_result


def xquery_min(func, current_node, static_context, *args):
    check_arg_min(func, 1, *args)

    if is_elt_empty(args[0]):
        return ''

    list_arg = extend_arg_from_list(*args)

    min_result = None
    for operand in list_arg:
        numeric = get_numeric_or_string(func, operand, min_result)
        if min_result is None or min_result > numeric:
            min_result = numeric

    return min_result


def math_simple_func_keep_type_or_not(func_name, func_operation,
                                      keep_type, *args):
    check_arg(func_name, 1, *args)

    if is_elt_empty(args[0]):
        return []

    arg_0 = DrbQueryFuncUtil.get_value(args[0], True)
    numeric = get_numeric(func_name, arg_0)

    if func_name == 'round':
        if isinstance(numeric, Decimal):
            res = math.floor(numeric + Decimal(0.5))
        else:
            res = math.floor(numeric + 0.5)

    else:
        res = func_operation(numeric)

    if keep_type and isinstance(numeric, float):
        return float(res)
    if keep_type and isinstance(numeric, Decimal):
        return Decimal(res)
    if keep_type and isinstance(numeric, int):
        return int(res)
    return res


def math_simple_func(func_name, func_operation, *args):
    return math_simple_func_keep_type_or_not(func_name, func_operation,
                                             False, *args)


def math_simple_func_keep_type(func_name, func_operation, *args):
    return math_simple_func_keep_type_or_not(func_name, func_operation,
                                             True, *args)


def math_ceiling(func, current_node, static_context, *args):
    return math_simple_func_keep_type(func, math.ceil, *args)


def math_floor(func, current_node, static_context, *args):
    return math_simple_func_keep_type(func, math.floor, *args)


def math_abs(func, current_node, static_context, *args):
    return math_simple_func_keep_type(func, abs, *args)


def math_round(func, current_node, static_context, *args):
    return math_simple_func_keep_type(func, round, *args)


def math_square(func, current_node, static_context, *args):
    return math_simple_func(func, math.sqrt, *args)


def math_cos(func, current_node, static_context, *args):
    return math_simple_func(func, math.cos, *args)


def math_sin(func, current_node, static_context, *args):
    return math_simple_func(func, math.sin, *args)


def math_log(func, current_node, static_context, *args):
    return math_simple_func(func, math.log, *args)


def math_exp(func, current_node, static_context, *args):
    return math_simple_func(func, math.exp, *args)


def xs_int(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_int_value(args[0])


def xs_negativeInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_int_value(args[0])

    if value >= 0:
        raise DynamicException(ErrorXQUERY.FORG0001,
                               "Error type " + value +
                               " can  not be converted to " + func)
    return value


def xs_nonNegativeInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_int_value(args[0])

    if value < 0:
        raise DynamicException(ErrorXQUERY.FORG0001,
                               "Error type " + value +
                               " can  not be converted to " + func)
    return value


def xs_positiveInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_int_value(args[0])

    if value <= 0:
        raise DynamicException(ErrorXQUERY.FORG0001,
                               "Error type " + value +
                               " can  not be converted to " + func)
    return value


def xs_nonPositiveInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_int_value(args[0])

    if value > 0:
        raise DynamicException(ErrorXQUERY.FORG0001,
                               "Error type " + value +
                               " can  not be converted to " + func)
    return value


def xs_boolean(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_value(args[0])

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float, Decimal)):
        return value > 0

    if isinstance(value, str):
        if value.lower().strip() == 'false':
            return False
        if value.lower().strip() == 'true':
            return True
        try:
            return float(value) > 0
        except Exception:
            raise DynamicException(ErrorXQUERY.FORG0001, "unable to cast " +
                                   str(args[0]) + " into boolean")

    raise DynamicException(ErrorXQUERY.FORG0001, "unable to cast " +
                           str(args[0]) + " into boolean")


def xs_decimal(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_decimal_value(args[0])


def xs_float(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_float_value(args[0])


def xs_byte(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_byte_value(args[0])


def xs_string(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_string(args[0], True)


def xs_node(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    return DrbQueryFuncUtil.get_string(args[0])


def text(func, current_node, static_context, *args):
    check_arg(func, 0, *args)

    value = DrbQueryFuncUtil.get_value(current_node)
    if isinstance(value, str):
        return value
    else:
        return None


def node(func, current_node, static_context, *args):
    check_arg(func, 0, *args)

    value = DrbQueryFuncUtil.get_node(current_node)
    if not isinstance(value, DrbNode):
        return None
    if static_context.is_in_predicate:
        return current_node

    result = []
    index = 0
    for child in value.children:
        if isinstance(DrbQueryFuncUtil.get_node(child), DrbNode):
            n = DynamicContext(child, index)
            index = index + 1
            result.append(n)

    return result


def xs_anyAtomicType(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    value = DrbQueryFuncUtil.get_value(args[0])
    return value


def xs_untypedAtomic(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if isinstance(args[0], list):
        raise DynamicException(ErrorXQUERY.FOAP0001,
                               "xs_untypedAtomic : requires atomic")
    value = DrbQueryFuncUtil.get_value(args[0])
    return value


def xs_datetime(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if isinstance(args[0], datetime.datetime):
        return args[0]
    try:
        dt = parse(args[0])
        return dt
    except Exception:
        pass

    try:
        if '.' in args[0]:
            return datetime.datetime. \
                strptime(args[0], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            return datetime.datetime.\
                strptime(args[0], "%Y-%m-%dT%H:%M:%S")
    except Exception:
        try:
            if '.' in args[0]:
                return datetime.datetime. \
                    strptime(args[0], "%d-%b-%Y %H:%M:%S.%f")
            else:
                return datetime.datetime. \
                    strptime(args[0], "%d-%b-%Y %H:%M:%S")
        except Exception:
            raise DynamicException(ErrorXQUERY.FORG0001, "unable to cast " +
                                   args[0] + " into datatime")


def xs_is_int(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), int)


def xs_is_float(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), float)


def xs_is_decimal(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), Decimal)


def xs_is_boolean(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), bool)


def xs_is_string(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), str)


def xs_is_node(func, current_node, static_context, *args):
    check_arg(func, 1, *args)

    if isinstance(args[0], DrbNode):
        return True
    if isinstance(args[0], DynamicContext):
        return isinstance(args[0].node, DrbNode)

    return False


def xs_is_datetime(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    return isinstance(DrbQueryFuncUtil.get_value(args[0]), datetime.datetime)


def xs_is_negativeInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    value = DrbQueryFuncUtil.get_value(args[0])
    return isinstance(value, int) and value < 0


def xs_is_nonNegativeInteger(func, current_node, static_context, *args):
    return not xs_is_negativeInteger(func, current_node, static_context, *args)


def xs_is_positiveInteger(func, current_node, static_context, *args):
    check_arg(func, 1, *args)
    value = DrbQueryFuncUtil.get_value(args[0])
    return isinstance(value, int) and value > 0


def xs_is_nonPositiveInteger(func, current_node, static_context, *args):
    return not xs_is_positiveInteger(func, current_node, static_context,
                                     *args)


class DrbQueryFuncCall:
    xpath_func = {
        'last': get_last,
        'position': get_position,
        'count': count,
        'name': get_name,
        # TODO
        'node-name': get_name,
        'namespace-uri': get_namespace_uri,
        'starts-with': starts_with,
        'ends-with': ends_with,
        'contains': contains,
        'true': return_true,
        'false': return_false,
        'not': return_not,
        'boolean': return_boolean,
        # TODO
        'index': get_position,
        # TODO
        # 'avg': get_avg,
        'matches': matches,
        'string': xs_string,

        'substring': substring,
        'substring-after': substring_after,
        'substring-before': substring_before,
        'string-length': string_length,
        'string-join': string_join,
        'concat': string_concat,
        'compare': string_compare,
        'replace': string_replace,
        'tokenize': string_tokenize,

        'upper-case': upper_case,
        'lower-case': lower_case,

        'exists': exists,
        'empty': empty,
        'reverse': reverse,
        'distinct-values': distinct_value,
        'deep-equal': deep_equal,
        'avg': average,
        'sum': f_sum,
        'min': xquery_min,
        'max': xquery_max,
        'ceiling': math_ceiling,
        'floor': math_floor,
        'abs': math_abs,
        'round': math_round,
        'doc': doc,
        'data': data,
        'current-dateTime': current_date_time,
        'current-time': current_time,
        'text': text,
        'node': node,

    }

    math_func = {
        'abs': math_abs,
        'sqrt': math_square,
        'cos': math_cos,
        'sin': math_sin,
        'log': math_log,
        'exp': math_exp,
    }

    drb_func = {
        'xml': drb_xml,
    }

    xs_type_func = {
        'short': xs_int,
        'double': xs_float,
        'float': xs_float,
        'int': xs_int,
        'long': xs_int,
        'integer': xs_int,
        'decimal': xs_decimal,
        'byte': xs_int,
        'unsignedByte': xs_int,
        'unsignedShort': xs_int,
        'unsignedLong': xs_int,
        'unsignedInt': xs_int,
        'boolean': xs_boolean,
        'string': xs_string,
        'node': xs_node,
        'dateTime': xs_datetime,
        'negativeInteger': xs_negativeInteger,
        'nonNegativeInteger': xs_nonNegativeInteger,
        'nonPositiveInteger': xs_nonPositiveInteger,
        'positiveInteger': xs_positiveInteger,
        'anyAtomicType': xs_anyAtomicType,
        'untypedAtomic': xs_untypedAtomic

    }

    xs_instance_func = {
        'short': xs_is_int,
        'double': xs_is_float,
        'float': xs_is_float,
        'int': xs_is_int,
        'long': xs_is_int,
        'integer': xs_is_int,
        'decimal': xs_is_decimal,
        'byte': xs_is_int,
        'unsignedByte': xs_is_int,
        'unsignedShort': xs_is_int,
        'unsignedLong': xs_is_int,
        'unsignedInt': xs_is_int,
        'boolean': xs_is_boolean,
        'string': xs_is_string,
        'node': xs_is_node,
        'dateTime': xs_is_datetime,
        'negativeInteger': xs_is_negativeInteger,
        'positiveInteger': xs_is_positiveInteger,
        'nonNegativeInteger': xs_is_nonNegativeInteger,
        'nonPositiveInteger': xs_is_nonPositiveInteger,

    }

    @staticmethod
    def init_namespace_context(context: StaticContext):

        context.set_func_list_namespace('fn', DrbQueryFuncCall.xpath_func)
        context.set_func_list_namespace('xs', DrbQueryFuncCall.xs_type_func)
        context.set_func_list_namespace('math', DrbQueryFuncCall.math_func)
        context.set_func_list_namespace('drb', DrbQueryFuncCall.drb_func)

        context.namespace_default_func = 'fn'
        # "http://www.w3.org/2005/xpath-functions"
        context.namespace_default_elt = ''
