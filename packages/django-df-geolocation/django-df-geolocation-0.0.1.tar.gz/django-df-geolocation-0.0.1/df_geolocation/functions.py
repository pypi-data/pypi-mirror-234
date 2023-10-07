from typing import Any

from django.db.models import Field, Func, Lookup, fields


class LLToEarth(Func):
    function = "ll_to_earth"
    arg_joiner = ", "
    arity = 2  # The number of arguments the function accepts.

    def __init__(
        self, *expressions: Any, output_field: Any = None, **extra: Any
    ) -> None:
        if output_field is None:
            output_field = fields.Field()
        super().__init__(*expressions, output_field=output_field, **extra)


class EarthBox(LLToEarth):
    function = "earth_box"
    arg_joiner = ", "


class EarthDistance(LLToEarth):
    function = "earth_distance"
    arg_joiner = ", "


@Field.register_lookup
class Near(Lookup):
    lookup_name = "in_georange"
    operator = "@>"

    def as_sql(self, compiler: Any, connection: Any) -> tuple[str, Any]:
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s @> %s" % (lhs, rhs), params
