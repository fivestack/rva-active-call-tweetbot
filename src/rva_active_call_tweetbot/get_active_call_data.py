import time

import pandas as pd

RVA_ACTIVE_CALLS_URL = "https://apps.richmondgov.com/applications/activecalls/home/activecalls"


def get_current_snapshot() -> 'pd.DataFrame':
    snapshot = pd.read_html(io=RVA_ACTIVE_CALLS_URL)[0]
    columns = {
        "Time Received": "received",
        "Agency": "agency",
        "Dispatch Area": "dispatch_area",
        "Unit": "unit",
        "Call Type": "call_type",
        "Location": "address",
        "Status": "status"
    }
    snapshot.rename(columns=columns, inplace=True)
    return snapshot


def get_snapshot_delta(previous_snapshot: 'pd.DataFrame', next_snapshot: 'pd.DataFrame') -> pd.DataFrame:
    assert set(next_snapshot.columns) == set(previous_snapshot.columns)
    diffs = next_snapshot.merge(previous_snapshot, on=["received", "agency", "unit"], how="left", indicator=True)
    diffs = diffs[diffs["_merge"] == "left_only"]
    columns = {c: c[:-2] for c in diffs.columns if c.endswith("_x")}
    diffs.rename(columns=columns, inplace=True)
    diffs = diffs[next_snapshot.columns]
    return diffs


def sample_active_calls(sample_period: int) -> 'pd.DataFrame':
    first_sample = get_current_snapshot()
    time.sleep(sample_period)
    second_sample = get_current_snapshot()
    return get_snapshot_delta(first_sample, second_sample)


if __name__ == "__main__":
    print(sample_active_calls(5))
