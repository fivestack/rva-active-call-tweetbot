from datetime import datetime, timedelta
from random import randint, choice
from string import ascii_letters
from typing import List

import pandas as pd

from .conftest import get_active_call_data


def generate_random_word(length: int = 10, include_spaces: bool = False):
    letters = ascii_letters
    if include_spaces:
        letters += ' '
    return ''.join(choice(letters) for i in range(length))


def get_new_df(records: 'List[dict]' = None) -> 'pd.DataFrame':
    columns = [
        "received",
        "agency",
        "dispatch_area",
        "unit",
        "call_type",
        "address",
        "status"
    ]
    data = pd.DataFrame(columns=columns)
    if records:
        data.append(records)
    return data


def generate_random_records(n: int = 1) -> 'List[dict]':
    records = []
    for i in range(n):
        record = {
            "received": datetime.now() + timedelta(minutes=randint(0, 100)),
            "agency": generate_random_word(length=randint(3, 5)),
            "dispatch_area": generate_random_word(length=randint(7, 10), include_spaces=True),
            "unit": generate_random_word(length=5),
            "call_type": generate_random_word(length=randint(10, 30), include_spaces=True),
            "address": generate_random_word(length=randint(10, 30), include_spaces=True),
            "status": generate_random_word(length=2)
        }
        records.append(record)
    return records


def test_get_current_snapshot():
    snapshot = get_active_call_data.get_current_snapshot()
    expected_columns = get_new_df()
    assert set(snapshot.columns) == set(expected_columns.columns)
    assert len(snapshot) > 1
    assert not snapshot.iloc[0].equals(snapshot.iloc[1])


def test_get_snapshot_delta():
    size = randint(10, 20)
    records_to_drop = randint(1, 4)
    records_to_add = randint(1, 4)

    test_records = generate_random_records(size)
    previous_snapshot = get_new_df(records=test_records[:records_to_add])
    next_snapshot = get_new_df(records=test_records[records_to_drop:])
    expected_diff = get_new_df(records=test_records[:-records_to_add])
    actual_diff = get_active_call_data.get_snapshot_delta(previous_snapshot=previous_snapshot,
                                                          next_snapshot=next_snapshot)
    pd.testing.assert_frame_equal(expected_diff, actual_diff)
