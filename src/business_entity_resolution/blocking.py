import re
import unicodedata
import pandas as pd


def _normalize_for_blocking(text):
    if pd.isna(text):
        return ""

    text = unicodedata.normalize("NFKC", str(text)).lower()

    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def _first_tokens(text, n=2):
    if not text:
        return ""

    return " ".join(text.split()[:n])


def _last_tokens(text, n=2):
    if not text:
        return ""

    return " ".join(text.split()[-n:])


def _sorted_tokens(text, n=3):
    if not text:
        return ""

    tokens = text.split()

    return " ".join(sorted(tokens)[:n])


def make_block_key(text):
    text = _normalize_for_blocking(text)

    if not text:
        return ""

    return _first_tokens(text, 2)


def create_blocking_keys(df):
    result = df.copy()

    name = result["business_name"].fillna("").apply(
        _normalize_for_blocking
    )

    address = result["business_address"].fillna("").apply(
        _normalize_for_blocking
    )

    country = (
        result["country"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    result["name_block_key"] = name.apply(
        lambda x: _first_tokens(x, 2)
    )

    result["name_last_block_key"] = name.apply(
        lambda x: _last_tokens(x, 2)
    )

    result["name_sorted_block_key"] = name.apply(
        lambda x: _sorted_tokens(x, 3)
    )

    result["address_block_key"] = address.apply(
        lambda x: _first_tokens(x, 2)
    )

    result["address_last_block_key"] = address.apply(
        lambda x: _last_tokens(x, 2)
    )

    result["country_block_key"] = country

    return result