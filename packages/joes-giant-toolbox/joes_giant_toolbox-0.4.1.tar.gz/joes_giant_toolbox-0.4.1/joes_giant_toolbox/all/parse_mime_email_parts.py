"""
This script defines the function parse_mime_email_parts()
"""

import base64
from typing import Any


# pylint: disable=too-many-nested-blocks
def parse_mime_email_parts(
    mime_parts: list[Any],
    _collected_parts: dict[str, Any] | None = None,
) -> dict[str, list[str]]:
    """Extracts parts from an email that is in MIME format

    Parameters
    ----------
    mime_parts : list[Any]
        list of MIME parts
    _collected_parts : dict[str, Any] | None
        This parameter is used for recursion (i.e. for internal function use)

    Example Output
    --------------
    {
        "text/plain" : ["...raw text of email body appears here..."],
        "text/html" : ["...html representation of email contents appears here..."],
        'attachment_ids': {
            'application/pdf': ['ANGjdJ-oLlW5JDE6IGPBKGD_BCGkT'],
            'text/csv': ['QvlsG07tcZset9U6bHj_2grxKZ8q3'],
            'application/vnd.ms-powerpoint': ['2grxKZ8q3_QvlsG07tcZset9U6bHj'],
        },
    }
    """
    if _collected_parts is None:
        _collected_parts = {
            "text/plain": [],
            "text/html": [],
            "attachment_ids": {},
        }
    for part in mime_parts:
        mime_type: str = part.get("mimeType")
        body: dict[str, Any] = part.get("body")
        data = body.get("data")
        part_headers: list[dict[str, Any]] = part.get("headers")
        if part.get("parts"):
            # if we hit a part itself containing parts, recursively call this function
            parse_mime_email_parts(
                mime_parts=part.get("parts"), _collected_parts=_collected_parts
            )
        if mime_type in ("text/plain", "text/html"):
            if data:
                _collected_parts[mime_type].append(
                    base64.urlsafe_b64decode(data).decode()
                )
        else:
            for part_header in part_headers:
                part_header_name: str | None = part_header.get("name")
                part_header_value: str | None = part_header.get("value")
                if part_header_name == "Content-Disposition":
                    if (
                        part_header_value is not None
                        and "attachment" in part_header_value
                    ):
                        if mime_type not in _collected_parts["attachment_ids"]:
                            _collected_parts["attachment_ids"][mime_type] = []
                        _collected_parts["attachment_ids"][mime_type].append(
                            body.get("attachmentId")
                        )

    return _collected_parts
