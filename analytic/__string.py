import re

from string import *


def fromHtml(html=""):
    # Remove script and style tags (optional)
    cleaned_html = re.sub(
        r"<(script|style).*?</(script|style)>", "", html, flags=re.IGNORECASE
    )

    # Extract text between HTML tags (ignoring leading/trailing whitespace)
    text_without_tags = re.sub(r"<[^>]*>", "", cleaned_html).strip()

    return text_without_tags
