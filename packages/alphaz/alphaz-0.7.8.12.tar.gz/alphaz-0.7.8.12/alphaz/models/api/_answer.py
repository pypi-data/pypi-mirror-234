from dataclasses import (
    dataclass,
    field,
)
from ..main import _base

from ...libs import json_lib


@dataclass
class ApiPagination(_base.AlphaDataclass):
    total: int | None = None
    total_pages: int | None = None
    page: int | None = None
    previous_page: int | None = None
    next_page: int | None = None
    per_page: int | None = None


@dataclass
class ApiAnswer(_base.AlphaDataclass):
    token_status: str = "success"
    status: str = "success"
    error: int = 0
    warning: int = 0
    status_code: int = 200
    status_description: str = ""
    requester: str = "unknow"
    data: dict = field(default_factory=lambda: {})
    pagination: ApiPagination = field(default_factory=lambda: {})

    def to_json(self):
        return json_lib.jsonify_data(self.get_fields_dict())

    def set_error(self, description: str):
        self.error = 1
        self.status = "error"
        self.status_code = 520
        self.status_description = description
