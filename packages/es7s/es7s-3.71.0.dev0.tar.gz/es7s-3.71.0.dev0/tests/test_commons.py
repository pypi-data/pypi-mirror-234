# -----------------------------------------------------------------------------
#  pytermor [ANSI formatted terminal output toolset]
#  (c) 2022-2023. A. Shavykin <0.delameter@gmail.com>
#  Licensed under GNU Lesser General Public License v3.0
# -----------------------------------------------------------------------------
from __future__ import annotations

import io
import logging
import re
from collections import deque
from logging import StreamHandler, DEBUG
from time import sleep

from es7s.commons import measure


class TestMeasure:
    _hndr: StreamHandler
    _buf: io.StringIO

    @classmethod
    def setup_class(cls):
        cls._buf = io.StringIO()
        cls._hndr = StreamHandler(cls._buf)
        cls._hndr.setLevel(DEBUG)

        logger = logging.getLogger('es7s.commons')
        logger.addHandler(cls._hndr)
        logger.setLevel(DEBUG)

    def setup_method(self):
        self.__class__._buf.seek(0)
        self.__class__._buf.truncate()

    @classmethod
    def teardown_class(cls):
        cls._buf.close()
        logging.getLogger('es7s.commons').removeHandler(cls._hndr)

    def test_measure_with_callable(self):
        self._decorated_with_callable()
        self.__class__._buf.seek(0)
        record = self.__class__._buf.readline()
        assert re.match(r'result: 5\dms', record)

    def test_measure_without_fmter(self):
        self._decorated_without_fmter()
        self.__class__._buf.seek(0)
        assert not self.__class__._buf.readline()

    @classmethod
    def _decorated(cls):
        sleep(0.05)

    @classmethod
    @measure(fmter=lambda s, *_: [f"result: {s}"])
    def _decorated_with_callable(cls, *_, **__):
        cls._decorated()

    @classmethod
    @measure(fmter=lambda *_: None)
    def _decorated_without_fmter(cls, *_, **__):
        cls._decorated()
