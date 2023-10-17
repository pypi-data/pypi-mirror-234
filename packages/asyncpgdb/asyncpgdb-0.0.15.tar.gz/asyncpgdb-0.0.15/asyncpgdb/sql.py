from typing import Iterable, Callable, Optional, List, Union
from dataclasses import dataclass
from functools import reduce
from json import dumps


FmtParam = Callable[[Union[list, dict, str]], str]
FmtParamName = Callable[[str], str]
FmtParamIndex = Callable[[int], str]
FmtParams = Callable[[Iterable[object]], List[str]]
FmtQuery = Callable[[str, dict], str]
FmtVars = Callable[[dict], List[str]]
Replace = Callable[[str, tuple[str, str]], str]
ReplaceMany = Callable[[str, Iterable[tuple[str, str]]], str]


fmt_param: FmtParam = lambda obj: dumps(obj) if isinstance(obj, (list, dict)) else obj
fmt_params: FmtParams = lambda params: list(map(fmt_param, params))

replace: Replace = lambda __str, lr: lr[1].join(__str.split(lr[0]))
replace_many: ReplaceMany = lambda __str, replacements: reduce(
    replace, replacements, __str
)

fmt_param_name: FmtParamName = lambda key: f"$({key})"
fmt_param_index: FmtParamIndex = lambda i: f"${i}"

iter_fmt_pairs = lambda keys: (
    (fmt_param_name(key), fmt_param_index(i)) for i, key in enumerate(keys, start=1)
)
if_none_then = lambda lhs, rhs: rhs if lhs is None else lhs
iter_repl_pairs = lambda keys, repl_map: if_none_then(repl_map, iter_fmt_pairs(keys))
repl_pairs = lambda x, y, z: replace_many(z, iter_repl_pairs(x, y))

fmt_query: FmtQuery = lambda query, keys: repl_pairs(keys, None, query)


@dataclass(frozen=True, order=True)
class SQLArgs:
    __slots__ = ("sql", "args")

    sql: str
    args: Optional[List[str]]

    def query_args(self):
        query = self.sql
        args = self.args
        return (query,) if args is None else (query, *args)

    def command_args(self):
        query = self.sql
        args = self.args
        return (query, args) if args else (query,)


def query_args(
    query: Optional[str] = None,
    command: Optional[str] = None,
    vars: Optional[dict] = None,
    vars_list: Optional[List[dict]] = None,
):
    args = None
    if query:
        sql = query
        if vars:
            sql = fmt_query(query, vars)
            args = fmt_params(vars.values()) if vars else None

    elif command:
        sql = command
        if vars_list:
            _vars = vars_list[0]
            keys = list(_vars.keys())
            sql = fmt_query(command, keys)
            args = [[fmt_param(vars[key]) for key in keys] for vars in vars_list]

    else:
        raise ValueError("unable to initialize query_args")
    return SQLArgs(sql=sql, args=args)
