from __future__ import annotations

from typing import Any, Dict, List
from fastapi import HTTPException, UploadFile, status
import json
import yaml

from ..config import import_max_file_bytes, import_max_items


def build_error_detail(message: str, *, errors: List[str] | None = None, **extra: Any) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"ok": False, "message": message, "errors": errors or []}
    detail.update(extra)
    return detail


def _load_serialized(text: str, fmt: str) -> Any:
    fmt_lower = (fmt or "json").lower()
    try:
        if fmt_lower == "yaml":
            return yaml.safe_load(text) or []
        if fmt_lower == "json":
            return json.loads(text)
    except (yaml.YAMLError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"Invalid {fmt_lower} payload.", errors=[str(exc)]),
        ) from exc
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail=build_error_detail(f"Unsupported format '{fmt}'."),
    )


def read_payload_source(
    payload: Any,
    *,
    body_format: str = "json",
    file: UploadFile | None = None,
    file_format: str | None = None,
) -> Any:
    """Return the raw Python structure decoded from the request payload."""
    if file is not None:
        raw = file.file.read()
        max_bytes = import_max_file_bytes()
        if max_bytes > 0 and len(raw) > max_bytes:
            raise HTTPException(
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=build_error_detail(
                    "Uploaded file exceeds the configured limit.",
                    limit_bytes=max_bytes,
                ),
            )
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=build_error_detail("Uploaded file must be UTF-8 encoded."),
            ) from exc
        use_fmt = file_format or body_format or "json"
        return _load_serialized(text, use_fmt)

    if isinstance(payload, str):
        fmt = (body_format or "json").lower()
        if fmt in {"yaml", "yml"}:
            return _load_serialized(payload, "yaml")
        if fmt == "json":
            return _load_serialized(payload, "json")
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"Unsupported format '{body_format}'."),
        )

    return payload


def normalize_items(data: Any, *, context: str) -> List[Dict[str, Any]]:
    """Normalize incoming data to a list of dict items."""
    if data is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"{context} import payload is empty."),
        )

    if isinstance(data, dict):
        items = data.get("items")
        if items is None:
            items = [data]
    elif isinstance(data, list):
        items = data
    else:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"{context} import payload must be a list or object."),
        )

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=build_error_detail(
                    f"Invalid {context} entry.",
                    errors=[f"Item at index {idx} must be an object."],
                ),
            )
        normalized.append(item)

    limit = import_max_items()
    if limit > 0 and len(normalized) > limit:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(
                f"{context.title()} import exceeds the limit of {limit} items.",
                count=len(normalized),
                limit=limit,
            ),
        )

    return normalized


def normalize_single(data: Any, *, context: str) -> Dict[str, Any]:
    """Normalize a payload to a single dict object."""
    if data is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"{context} payload is empty."),
        )

    if isinstance(data, dict):
        items = data.get("items")
        if items is None:
            return data
        data = items

    if isinstance(data, list):
        if len(data) != 1:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=build_error_detail(
                    f"{context.title()} payload must contain exactly one item.",
                    count=len(data),
                ),
            )
        candidate = data[0]
        if not isinstance(candidate, dict):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=build_error_detail(f"{context.title()} payload must be an object."),
            )
        return candidate

    if not isinstance(data, dict):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail(f"{context} payload must be an object."),
        )
    return data


def validation_errors_to_messages(errors: List[dict]) -> List[str]:
    messages: List[str] = []
    for err in errors:
        loc = err.get("loc") or []
        loc_path = ".".join(str(part) for part in loc if part not in {"__root__"})
        msg = err.get("msg") or "Invalid value."
        messages.append(f"{loc_path}: {msg}" if loc_path else msg)
    return messages
