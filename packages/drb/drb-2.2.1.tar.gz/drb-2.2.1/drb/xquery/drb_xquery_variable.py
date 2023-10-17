from .drb_xquery_utils import DrbQueryFuncUtil
from .execptions import DynamicException, ErrorXQUERY
from drb.xquery.drb_xquery_func import DrbQueryFuncCall


class XqueryBuildIn:
    def __init__(self, name,
                 exp_func,
                 namespace=None,
                 specific_context=None):
        self.name = name
        self.namespace = namespace
        self.exp_func = exp_func
        self.specific_context = specific_context


class XqueryVariable:

    def __init__(self, name, namespace=None, external=False,
                 value=None, type_var=None):
        self.namespace = namespace
        self.name = name
        self.external = external
        self.value = value
        self.arg_min = 1
        self.arg_max = 0
        if type_var is not None:
            if isinstance(type_var, tuple):
                self.arg_min = type_var[1]
                self.arg_max = type_var[2]
                type_var_full = type_var[0]
            else:
                type_var_full = type_var
            self.type_var_namespace, self.type_var = \
                DrbQueryFuncUtil.split_namespace_name(type_var_full)
        else:
            self.type_var_namespace, self.type_var = (None, None)
        self._typed_value = None

    def get_value(self):
        if self._typed_value is None:
            self._typed_value = self.get_value_typed(self.type_var,
                                                     self.type_var_namespace,
                                                     self.value,
                                                     arg_min=self.arg_min,
                                                     arg_max=self.arg_max)
        return self._typed_value

    @staticmethod
    def get_value_typed(type_var, type_var_namespace, value,
                        arg_min: int = 1,
                        arg_max: int = 0,
                        func_msg: str = ''):
        if type_var is not None:
            if value is None:
                if arg_min == 0:
                    return ''
                else:
                    raise DynamicException(ErrorXQUERY.XPTY0004,
                                           func_msg +
                                           " empty value instead of" +
                                           type_var_namespace + ':' + type_var)
            if type_var_namespace == 'xs':
                if isinstance(value, list) and arg_max > 1:
                    result = []
                    for item in value:
                        result.append(DrbQueryFuncCall.xs_type_func[type_var](
                            type_var, None, None, item))
                else:
                    if isinstance(value, list):
                        if len(value) == 0:
                            if arg_min == 0:
                                return value
                            else:
                                raise DynamicException(ErrorXQUERY.XPTY0004,
                                                       func_msg +
                                                       " empty" +
                                                       " sequence " +
                                                       "but it is not " +
                                                       "allowed by definition")
                        if len(value) > 1:
                            raise DynamicException(ErrorXQUERY.XPTY0004,
                                                   func_msg +
                                                   " more than one " +
                                                   "but it is not " +
                                                   "allowed by definition")
                        value = value[0]
                    result = DrbQueryFuncCall.xs_type_func[type_var](
                        type_var, None, None, value)
                if result is not None or arg_min == 0:
                    return result
            raise DynamicException(ErrorXQUERY.XPST0051,
                                   func_msg +
                                   "Type " +
                                   type_var +
                                   "is unknown with namespace " +
                                   type_var_namespace)

        return value
