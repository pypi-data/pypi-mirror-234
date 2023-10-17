# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_vendor.wrapt import register_post_import_hook

from contrast.patches.databases import dbapi2

MYSQL_CONNECTOR = "mysql.connector"
VENDOR = "MySQL"


def instrument_mysql_connector(mysql_connector):
    extra_cursors = [
        mysql_connector.cursor.CursorBase,
        mysql_connector.cursor.MySQLCursor,
    ]

    try:
        # The C extension is technically optional
        extra_cursors.append(mysql_connector.cursor_cext.CMySQLCursor)
    except AttributeError:
        pass

    dbapi2.instrument_adapter(
        mysql_connector,
        VENDOR,
        dbapi2.Dbapi2Patcher,
        extra_cursors=extra_cursors,
    )


def register_patches():
    register_post_import_hook(instrument_mysql_connector, MYSQL_CONNECTOR)
