from decimal import Decimal
from typing import Optional

from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.types import NUMERIC, TypeDecorator

from atlantiscore.types.evm import EVMAddress as PythonEVMAddress, LiteralEVMAddress

PRECISION = 49


class EVMAddress(TypeDecorator):
    impl = NUMERIC
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> Numeric:
        return dialect.type_descriptor(NUMERIC(PRECISION))

    def process_bind_param(
        self,
        value: Optional[PythonEVMAddress | LiteralEVMAddress],
        dialect: Dialect,
    ) -> int:
        if value is None:
            return value
        return int(PythonEVMAddress(value))

    def process_result_value(
        self,
        value: Optional[int | Decimal],
        dialect: Dialect,
    ) -> PythonEVMAddress:
        if value is None:
            return value
        return PythonEVMAddress(int(value))
