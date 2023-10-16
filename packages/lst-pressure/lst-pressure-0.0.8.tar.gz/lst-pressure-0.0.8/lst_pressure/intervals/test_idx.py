import pytest
from .idx import Idx

test_data = [
    {
        "lst_schedule": [
            {"id": 1, "begin": 1, "end": 2},
            {"id": 2, "begin": 1, "end": 4},
            {"id": 3, "begin": 1.1, "end": 2},
        ]
    }
]


@pytest.mark.parametrize("test", test_data)
def test_IntervalTree(test):
    idx = Idx()
    for interval in test.get("lst_schedule"):
        begin = interval.get("begin")
        end = interval.get("end")
        idx.insert(begin, end, interval)

    print(idx.envelop(1.05, 8))
