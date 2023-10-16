import pandas as pd

from fiddler.utils import general_checks


def test_is_greater_than_max_value_r_insig_large():
    assert not general_checks.is_greater_than_max_value(
        0.40310425941951944, 0.403104259419519
    )


def test_is_greater_than_max_value_r_sig_large():
    assert general_checks.is_greater_than_max_value(
        0.40311425941951944, 0.403104259419519
    )


def test_is_less_than_min_value_l_insig_smaller():
    assert not general_checks.is_less_than_min_value(
        -0.40310425941951944, -0.403104259419519
    )


def test_is_less_than_min_value_l_sig_smaller():
    assert general_checks.is_less_than_min_value(
        -0.41310425941951944, -0.403104259419519
    )


def test_type_enforce_valid():
    params = [
        '1',
        1,
        '1',
        {'asdf': '1'},
        pd.Series(data={'a': 1, 'b': 2, 'c': 3}, index=['a', 'b', 'c']),
    ]
    req_types = [int, str, float, dict, dict]

    for i in range(len(params)):
        param = params[i]
        req_type = req_types[i]
        out = general_checks.type_enforce('_', param, req_type)
        assert type(out) == req_type


def test_type_enforce_invalid():
    # Cannot convert a list into a dictionary
    try:
        this_will_error = ['a', 'b', 'c']
        general_checks.type_enforce('this_will_error', this_will_error, dict)
    except Exception as e:
        assert "Parameter `this_will_error` must be of type <class 'dict'>" in str(e)
