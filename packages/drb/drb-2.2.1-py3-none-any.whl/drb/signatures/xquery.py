from drb.core.node import DrbNode
from drb.core.signature import Signature
from drb.xquery.drb_xquery_utils import DrbQueryFuncUtil


class XquerySignature(Signature):
    """
    Allowing to check if a DRB Node match a specific XQuery.
    """
    def __init__(self, query: str):
        self._query_str = query
        # workaround to avoid circular import (due to signature initialization)
        from drb.xquery import DrbXQuery
        self._xquery = DrbXQuery(self._query_str)

    def matches(self, node: DrbNode) -> bool:

        result = self._xquery.execute(node)
        if result is not None and len(result) > 0:
            return DrbQueryFuncUtil.get_effective_boolean_value(result)
        return False

    def to_dict(self) -> dict:
        return {self.get_name(): self._query_str}

    @staticmethod
    def get_name():
        return 'xquery'
