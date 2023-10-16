# -*- coding:utf-8 -*-

import unittest
from datetime import datetime
from django.utils import timezone
from knob.dt import *


class TestDT(unittest.TestCase):
    def setUp(self):
        pass

    def test_local_time(self):
        for raw_time, expected_str in [
            ('20230101', '2023-01-01 00:00:00'),
            (timezone.make_aware(datetime(year=2023, month=1, day=1, hour=0), timezone=timezone.utc), '2023-01-01 08:00:00'),
        ]:
            t = local_time(raw_time)
            t_str = t.strftime('%Y-%m-%d %H:%M:%S')
            self.assertEqual(expected_str, t_str)
            self.assertEqual(t.tzinfo, timezone.get_current_timezone())
            self.assertTrue(timezone.is_aware(t))

        now = local_now()
        converted = local_time(now)
        self.assertTrue(timezone.is_aware(converted))