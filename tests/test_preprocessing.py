from business_entity_resolution.preprocessing import (
    normalize_text,
    normalize_name,
    normalize_address,
    normalize_country,
)


def test_normalize_name_lowercase():
    result = normalize_name("ABC TECHNOLOGIES")
    assert result == "abc technologies"


def test_normalize_name_legal_suffix():
    result = normalize_name("ABC Technologies Private Limited")
    assert result == "abc technologies"


def test_normalize_name_punctuation():
    result = normalize_name("WALKER AND KELLY (INC.)")
    assert result == "walker and kelly"


def test_normalize_address():
    result = normalize_address("650 LYNN AVE, ROMEOVVILLE, IL")
    assert result == "650 lynn ave romeovville il"


def test_normalize_address_null_token():
    result = normalize_address("17/427 MELADOOR, NULL, Kerala")
    assert result == "17 427 meladoor kerala"


def test_normalize_address_unicode():
    result = normalize_address(
        "H.no 829 D-225vivek Vihar, Delhi, दिल्ली"
    )
    assert result == "h no 829 d 225vivek vihar delhi दिल्ली"


def test_normalize_country():
    result = normalize_country("  India  ")
    assert result == "india"


def test_normalize_missing_values():
    assert normalize_name(None) == ""
    assert normalize_address(None) == ""
    assert normalize_country(None) == ""