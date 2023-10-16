from datetime import date

import pytest

from prism._common.const import DateType
from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def _build_event(
    datacomponentclass,
    dataitemid: int,
    datetype: str,
    package: str = None,
) -> DateType:
    return datetype


def test_datetype_param():
    assert _build_event(None, 1, datetype=None) is None
    assert _build_event(None, 1, "announceddate",
                        "Prism Market") == DateType.ANNOUNCEDDATE

    # check type
    assert isinstance(_build_event(None, 1, "announceddate", "Prism Market"), DateType)

    # valid datetype param
    assert _build_event("news", 1, "entereddate") == DateType.ENTEREDDATE
    assert _build_event("news", 2, "announceddate") == DateType.ANNOUNCEDDATE

    assert _build_event(
        "news", 3, datetype="entereddate") == DateType.ENTEREDDATE
    assert _build_event(
        "news", 4, datetype="announceddate") == DateType.ANNOUNCEDDATE


def test_wrong_datetype_param():
    # wrong value
    with pytest.raises(PrismValueError):
        assert _build_event("news", 1, datetype="")

    with pytest.raises(PrismValueError):
        assert _build_event("news", 1, datetype="1998/10/03")

    with pytest.raises(PrismValueError):
        assert _build_event("news", 1, datetype="2023.04.04")

    with pytest.raises(PrismValueError):
        assert _build_event(
            "news", 23, datetype="ENTEREDDATE") == DateType.ENTEREDDATE

    with pytest.raises(PrismValueError):
        assert _build_event(
            "news", 23, datetype="AnnouncedDate") == DateType.ANNOUNCEDDATE

    # wrong type
    with pytest.raises(PrismTypeError):
        assert _build_event("news", "123", datetype=None)

    with pytest.raises(PrismTypeError):
        assert _build_event("news", 1, datetype=20220101)

    with pytest.raises(PrismTypeError):
        assert _build_event("news", 1, datetype=date.today())
