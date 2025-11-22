import re
from bs4 import BeautifulSoup

def clean_html(raw):
    """
    Strip HTML tags, convert <a> tags to 'text (URL)',
    normalize whitespace, and return clean plain text.
    """
    if not raw:
        return ""

    # Parse HTML safely
    soup = BeautifulSoup(raw, "html.parser")

    # Convert <a href> tags
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        href = a.get("href", "")
        if href:
            a.replace_with(f"{text} ({href})")
        else:
            a.replace_with(text)

    # Extract text
    cleaned = soup.get_text(" ", strip=True)

    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
