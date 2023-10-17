from enum import Enum


class CreateDbDataSetRequestDbType(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    DB2 = "db2"
    SQLSERVER = "sqlserver"

    def __str__(self) -> str:
        return str(self.value)