from decimal import Decimal
from drb.core.node import DrbNode
from .drb_xquery_context import DynamicContext
from .execptions import DynamicException, ErrorXQUERY
import datetime
import calendar
import math


class DrbQueryFuncUtil:

    @staticmethod
    def convert_before_compare(left_item, right_item):
        left_value = DrbQueryFuncUtil.get_value(left_item)
        right_value = DrbQueryFuncUtil.get_value(right_item)

        if not isinstance(left_value, type(right_value)):
            if isinstance(left_value, (float, int, Decimal)):
                right_value = DrbQueryFuncUtil.get_numeric_value(
                    right_value)
            elif isinstance(right_value, (float, int, Decimal)):
                left_value = DrbQueryFuncUtil.get_numeric_value(
                    left_value)
        return left_value, right_value

    @staticmethod
    def is_equal(left_value, right_value):
        return left_value == right_value or \
               str(left_value) == str(right_value)

    @staticmethod
    def get_value(node, only_one=False):
        if isinstance(node, list):
            if len(node) == 0:
                return None
            if len(node) > 1 and only_one:
                raise DynamicException(ErrorXQUERY.FOAP0001,
                                       "func : requires one parameter")
            node = node[0]

        if isinstance(node, (DrbNode, DynamicContext)):
            return node.value

        return node

    @staticmethod
    def get_float_value(node):
        value = DrbQueryFuncUtil.get_value(node)
        try:
            if isinstance(value, datetime.datetime):
                value = DrbQueryFuncUtil.get_epoch(value)
            if isinstance(value, (float, Decimal, str, int)):
                return float(value)
        except Exception as error:
            pass

        raise DynamicException(ErrorXQUERY.XPTY0004,
                               "Error type " + value +
                               " can  not be converted to float")

    @staticmethod
    def get_int_value(node):
        value = DrbQueryFuncUtil.get_value(node)
        if value is None:
            return ''
        if isinstance(value, datetime.datetime):
            value = DrbQueryFuncUtil.get_epoch(value)

        if isinstance(value, int):
            return value
        try:
            if isinstance(value, (float, Decimal, str)):
                return int(value)
        except Exception as error:
            pass
        raise DynamicException(ErrorXQUERY.XPTY0004,
                               "Error type " + value +
                               " can  not be converted to integer")

    @staticmethod
    def get_decimal_value(node):
        value = DrbQueryFuncUtil.get_value(node)
        if value is None:
            return ''
        if isinstance(value, Decimal):
            return value
        try:
            if isinstance(value, datetime.datetime):
                value = DrbQueryFuncUtil.get_epoch(value)

            if isinstance(value, (int, str)):
                return Decimal(value)
            if isinstance(value, float):
                return Decimal.from_float(value)

        except Exception as error:
            pass
        raise DynamicException(ErrorXQUERY.XPTY0004,
                               "Error type " + value +
                               " can  not be converted to decimal")

    @staticmethod
    def get_byte_value(node):
        value = DrbQueryFuncUtil.get_value(node)
        try:
            if isinstance(value, (float, Decimal, str)):
                value = int(value)
            if isinstance(value, int):
                return value.to_bytes(1, byteorder='big')

        except Exception as error:
            raise DynamicException(ErrorXQUERY.XPTY0004,
                                   "Error type " + value +
                                   " can  not be converted to byte")

    @staticmethod
    def get_numeric_value(node, only_one=False):
        value = DrbQueryFuncUtil.get_value(node, only_one)

        if isinstance(value,  (float, Decimal, int)):
            return value
        if isinstance(value, str):
            value_to_test = value
            if value_to_test.startswith('-') or value_to_test.startswith('+'):
                value_to_test = value_to_test[1:]
            if value_to_test.isnumeric():
                return int(value)
            try:
                return float(value)
            except Exception as error:
                raise DynamicException(ErrorXQUERY.XPTY0004,
                                       "Error type " + value +
                                       " can  not be converted to numeric")

    @staticmethod
    def get_epoch(date_time):
        # return date_time.timestamp()
        return calendar.timegm(date_time.timetuple())

    @staticmethod
    def get_round_int_value(node):
        value = DrbQueryFuncUtil.get_value(node)
        if isinstance(value, int):
            return value
        if isinstance(value, (float, Decimal, str)):
            return round(float(value))

    @staticmethod
    def get_nane(node):
        if isinstance(node, list):
            if len(node) == 0:
                return ''
            node = node[0]
        if isinstance(node, DrbNode):
            return node.name
        elif isinstance(node, DynamicContext):
            return node.name

        return ''

    @staticmethod
    def get_node(node):
        if isinstance(node, list):
            if len(node) == 0:
                return ''
            node = node[0]

        if isinstance(node, (DrbNode, str)):
            return node
        elif isinstance(node, DynamicContext):
            return node.node

        return node

    @staticmethod
    def get_effective_boolean_value(node):
        if node is None:
            return False
        if isinstance(node, list):
            if len(node) == 0:
                return False
            if len(node) == 1:
                node = node[0]
            else:
                return True

        if isinstance(node, DrbNode):
            return True

        if isinstance(node, DynamicContext) \
                and (node.is_node() or node.is_attribute()):
            return True

        if isinstance(node, bool):
            return node

        if isinstance(node, str):
            return len(node) != 0

        if isinstance(node, (int, float, Decimal)):
            if node == 0:
                return False
            if isinstance(node, float) and math.isnan(node):
                return False
            return True
        raise DynamicException(ErrorXQUERY.FORG0006,
                               "Error result of is not a boolean" +
                               str(node))

    @staticmethod
    def get_boolean_value(node):
        node = DrbQueryFuncUtil.get_node(node)
        if node is None:
            return False
        if isinstance(node, DrbNode):
            return True
        value = DrbQueryFuncUtil.get_value(node)

        if isinstance(value, bool):
            return node
        if isinstance(value, str):
            if len(value) == 0:  # or value == '0':
                return False
            else:
                return True

        if isinstance(value, (int, float, Decimal)):
            if isinstance(value, float):
                if math.isnan(value):
                    return False
            if isinstance(value, Decimal):
                if value.is_nan():
                    return False

            if value != 0:
                return True
        return False

    @staticmethod
    def get_name_in_result(result) -> str:
        if result is None:
            raise DynamicException(ErrorXQUERY.XPTY0004,
                                   "Error exp for name "
                                   "return None")

        if isinstance(result, list):
            if len(result) == 1:
                result = result[0]
            else:
                raise DynamicException(ErrorXQUERY.XPTY0004,
                                       "Error exp for name "
                                       "return more than "
                                       "one element")
        if isinstance(result, (DrbNode, DynamicContext)):
            result = result.value
        try:
            return str(result)
        except Exception as error:
            raise DynamicException(ErrorXQUERY.XPTY0004,
                                   "Error exp for name "
                                   "return non string "
                                   "element")

    @staticmethod
    def get_string(node, concat_child=False) -> str:
        value_string = ''
        if isinstance(node, list):
            if len(node) == 0:
                return ''
            result = DrbQueryFuncUtil.get_string(node[0])
            for item in node[1:]:
                result = result + ' ' + DrbQueryFuncUtil.get_string(item)
            return result

        if isinstance(node, DynamicContext) and isinstance(node.node, DrbNode):
            node = node.node

        if isinstance(node, DynamicContext):
            value_string = node.value
        elif isinstance(node, DrbNode):
            value_string = node.value
            if value_string is None:
                value_string = ''
            if concat_child:
                for child in node.children:
                    value_string = value_string + \
                                   DrbQueryFuncUtil.get_string(child)
        elif isinstance(node, str):
            value_string = node
        elif isinstance(node, datetime.datetime):
            # value_string = node.strftime('%d-%b-%Y %H:%M:%S.%f')
            if node.microsecond != 0:
                value_string = node.strftime('%Y-%m-%dT%H:%M:%SZ%f')
            else:
                value_string = node.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(node, float):
            if node.is_integer():
                value_string = str(int(node))
            else:
                value_string = str(node)
        else:
            value_string = str(node)
        if value_string is None:
            return ''

        return str(value_string)

    @staticmethod
    def is_object_in_list(object_to_find, list_object: list):
        for item in list_object:
            if DrbQueryFuncUtil.compare(object_to_find, item):
                return True
        return False

    @staticmethod
    def find_object_in_list(object_to_find, list_object: list):
        for item in list_object:
            if DrbQueryFuncUtil.compare(object_to_find, item):
                return item
        return None

    @staticmethod
    def append_if_object_not_in(object_to_append, list_object: list):
        if not DrbQueryFuncUtil.is_object_in_list(object_to_append,
                                                  list_object):
            list_object.append(object_to_append)

    @staticmethod
    def append_or_extend_if_not_in(object_to_append, list_object: list):
        if isinstance(object_to_append, list):
            for item in object_to_append:
                DrbQueryFuncUtil.append_if_object_not_in(item, list_object)
        else:
            DrbQueryFuncUtil.append_if_object_not_in(object_to_append,
                                                     list_object)

    @staticmethod
    def remove_duplicate(list_object: list):
        result = []
        for item in list_object:
            item_found = DrbQueryFuncUtil.find_object_in_list(item,
                                                              result)
            if item_found is None:
                result.append(item)
        return result

    @staticmethod
    def intersect(object_to_append, list_object: list):
        if list_object is None:
            if isinstance(object_to_append, list):
                return DrbQueryFuncUtil.remove_duplicate(object_to_append)
            else:
                return [object_to_append]

        result = []
        object_to_append = DrbQueryFuncUtil.remove_duplicate(object_to_append)
        if isinstance(object_to_append, list):
            for item in object_to_append:
                item_found = DrbQueryFuncUtil.find_object_in_list(item,
                                                                  list_object)
                if item_found is not None:
                    result.append(item_found)
        elif DrbQueryFuncUtil.is_object_in_list(object_to_append, list_object):
            result.append(object_to_append)
        return result

    @staticmethod
    def except_op(object_to_append, list_object: list):
        if list_object is None:
            if isinstance(object_to_append, list):
                return DrbQueryFuncUtil.remove_duplicate(object_to_append)
            else:
                return [object_to_append]

        if isinstance(object_to_append, list):
            for item in object_to_append:
                item_found = DrbQueryFuncUtil.find_object_in_list(item,
                                                                  list_object)
                if item_found is not None:
                    list_object.remove(item_found)
        else:
            item_found = DrbQueryFuncUtil.find_object_in_list(object_to_append,
                                                              list_object)
            if item_found is not None:
                list_object.remove(object_to_append)
        return list_object

    @staticmethod
    def union(object_to_append, list_object: list):
        if list_object is None:
            if isinstance(object_to_append, list):
                return DrbQueryFuncUtil.remove_duplicate(object_to_append)
            else:
                return [object_to_append]
        if isinstance(object_to_append, list):
            for item in object_to_append:
                item_found = DrbQueryFuncUtil.find_object_in_list(item,
                                                                  list_object)
                if item_found is None:
                    list_object.append(item)
        else:
            item_found = DrbQueryFuncUtil.find_object_in_list(object_to_append,
                                                              list_object)
            if item_found is None:
                list_object.append(object_to_append)
        return list_object

    @staticmethod
    def append_or_extend(object_to_append, list_object: list):
        if isinstance(object_to_append, list):
            for item in object_to_append:
                list_object.append(item)
        else:
            list_object.append(object_to_append)

    @staticmethod
    def compare_drb(node1: DrbNode, node2: DrbNode) -> bool:
        if node1 == node2:
            if len(node1) == len(node2):
                for index_child in range(len(node1)):
                    if not DrbQueryFuncUtil.compare_drb(node1[index_child],
                                                        node2[index_child]):
                        return False
                return True
        return False

    @staticmethod
    def compare(node1, node2) -> bool:
        if not isinstance(node1, type(node2)):
            return False

        if isinstance(node1, list):
            if len(node1) != len(node2):
                return False
            for item_list1, item_list2 in zip(node1, node2):
                if not DrbQueryFuncUtil.compare(item_list1, item_list2):
                    return False
            return True

        if isinstance(node1, DynamicContext):
            return DrbQueryFuncUtil.compare(node1.node, node2.node)
        elif isinstance(node1, DrbNode):
            return DrbQueryFuncUtil.compare_drb(node1, node2)
        else:
            return node1 == node2

    @staticmethod
    def split_namespace_name(nc_name):
        type_var_split = nc_name.split(':')
        if len(type_var_split) > 1:
            return type_var_split[0], type_var_split[1]
        else:
            return None, type_var_split[0]

    @staticmethod
    def replace_group_regex_to_python(patttern):
        previous = ' '
        in_group = False
        value_group = ''
        result = ''

        for char in patttern:

            if in_group:
                if char.isnumeric():
                    value_group = value_group + char
                else:
                    in_group = False
                    if len(value_group) != 0:
                        result = result + r'\g<' + value_group + '>'
                    else:
                        raise DynamicException(ErrorXQUERY.FORX0004,
                                               "Error in replace pattern:" +
                                               patttern)
            if not in_group:
                if char == '$':
                    if previous != '\\':
                        in_group = True
                        value_group = ''
                    else:
                        result = result + char
                else:
                    result = result + char

        if in_group:
            if len(value_group) != 0:
                result = result + r'\g<' + value_group + '>'
            else:
                raise DynamicException(ErrorXQUERY.FORX0004,
                                       "Error in replace pattern:" +
                                       patttern)

        return result
