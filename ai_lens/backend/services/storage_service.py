import uuid
import json
import os
from typing import Dict, Optional

# File where we persist the store
STORE_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "outputs", "store.json")
)

# Ensure the outputs folder exists
os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)

# Load existing documents if the file is there
if os.path.exists(STORE_FILE):
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            _store: Dict[str, dict] = json.load(f)
    except json.JSONDecodeError:
        _store = {}
else:
    _store = {}

# Track last uploaded document
_last_doc_id: Optional[str] = next(reversed(_store)) if _store else None


def _save_to_disk() -> None:
    try:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(_store, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving store: {e}")


def save_document(text: str) -> str:
    global _last_doc_id

    doc_id = str(uuid.uuid4())

    _store[doc_id] = {
        "text": text
    }

    _last_doc_id = doc_id
    _save_to_disk()

    return doc_id


def get_document(doc_id: str | None) -> str | None:
    target_id = doc_id or _last_doc_id

    if not target_id:
        return None

    doc = _store.get(target_id)

    if not doc:
        return None

    return doc.get("text")