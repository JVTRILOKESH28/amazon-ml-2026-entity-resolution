import re
import unicodedata
import pandas as pd


LEGAL_SUFFIXES = {
    "private limited",
    "pvt ltd",
    "pvt limited",
    "private ltd",
    "limited",
    "ltd",
    "incorporated",
    "inc",
    "llc",
    "pllc",
    "llp",
}


def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Lowercase
    text = text.lower()

    # Remove URL artifacts
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Preserve letters, combining marks, numbers and whitespace.
    # Replace punctuation/symbols with spaces.
    text = "".join(
        char
        if (
            unicodedata.category(char).startswith(("L", "M", "N"))
            or char.isspace()
        )
        else " "
        for char in text
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_name(name):
    text = normalize_text(name)

    if not text:
        return ""

    # Remove legal suffix only when it occurs at the end
    for suffix in sorted(LEGAL_SUFFIXES, key=len, reverse=True):
        if text.endswith(" " + suffix):
            text = text[:-(len(suffix) + 1)].strip()
            break

    return text


def normalize_address(address):
    if pd.isna(address):
        return ""

    text = str(address)

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Lowercase
    text = text.lower()

    # Remove URL artifacts
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Preserve letters, combining marks, numbers and whitespace.
    text = "".join(
        char
        if (
            unicodedata.category(char).startswith(("L", "M", "N"))
            or char.isspace()
        )
        else " "
        for char in text
    )

    # Remove literal missing-value tokens
    text = re.sub(r"\b(null|none|nan)\b", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_country(country):
    if pd.isna(country):
        return ""

    text = unicodedata.normalize("NFKC", str(country))
    text = text.lower().strip()

    return text