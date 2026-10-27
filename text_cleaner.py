import re


def clean_text(text):
    # Convert to lowercase
    text = text.lower()

    # Replace multiple spaces and new lines
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted characters
    text = re.sub(r"[^a-zA-Z0-9+#./\- ]", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()