# Copyright 2019 Robert Bosch GmbH
# Copyright 2021 Christophe Bedard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
import unittest

from tracetools_launch.action import Trace


class TestTraceAction(unittest.TestCase):

    def __init__(self, *args) -> None:
        super().__init__(
            *args,
        )

    def test_has_profiling_events(self) -> None:
        events_lists_match: List[List[str]] = [
            [
                '*',
                'ros2:*',
            ],
            [
                'lttng_ust_cyg_profile:*',
            ],
            [
                'lttng_ust_cyg_profile_fast:*',
            ],
            [
                'lttng_ust_cyg_profile_fast:func_entry',
                'hashtag:yopo',
            ],
            [
                'lttng_ust_cyg_profile:func_entry',
                'some_other_event',
                'lttng_ust_cyg_profile:func_exit',
            ],
        ]
        events_lists_no_match: List[List[str]] = [
            [
                'ros2:*',
            ],
            [
                'lttng_ust_statedump:bin_info',
                'ros2:event',
            ],
            [],
        ]
        for events in events_lists_match:
            self.assertTrue(Trace.has_profiling_events(events))
        for events in events_lists_no_match:
            self.assertFalse(Trace.has_profiling_events(events))

    def test_has_ust_memory_events(self) -> None:
        events_lists_match: List[List[str]] = [
            [
                '*',
                'ros2:*',
            ],
            [
                'lttng_ust_libc:*',
            ],
            [
                'hashtag:yopo',
                'lttng_ust_libc:malloc',
                'lttng_ust_libc:realloc',
            ],
            [
                'lttng_ust_libc:still_a_match',
            ],
        ]
        events_lists_no_match: List[List[str]] = [
            [
                'ros2:*',
            ],
            [
                'my_random:event',
                'lttng_ust_whatever'
            ],
            [],
        ]
        for events in events_lists_match:
            self.assertTrue(Trace.has_ust_memory_events(events))
        for events in events_lists_no_match:
            self.assertFalse(Trace.has_ust_memory_events(events))


if __name__ == '__main__':
    unittest.main()
