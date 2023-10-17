from django.apps import (
    AppConfig,
)
from django.db.backends import (
    utils as backutils,
)

from m3_db_utils.settings import (
    SQL_LOG,
)
from m3_db_utils.wrappers import (
    DBUtilsCursorDebugWrapper,
)


class M3DBUtilsConfig(AppConfig):
    name = 'm3_db_utils'
    verbose_name = 'Утилиты для работы с БД'

    def ready(self):
        super().ready()

        if SQL_LOG:
            backutils.CursorDebugWrapper = DBUtilsCursorDebugWrapper
            backutils.CursorWrapper = DBUtilsCursorDebugWrapper
