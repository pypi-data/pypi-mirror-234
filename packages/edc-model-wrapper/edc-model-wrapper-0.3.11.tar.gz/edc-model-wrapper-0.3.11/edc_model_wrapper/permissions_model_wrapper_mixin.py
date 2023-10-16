from __future__ import annotations

from typing import Any


class PermissionsModelWrapperMixin:
    def __init__(self, request: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    @property
    def has_add_permission(self) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.add_{model_name}")

    @property
    def has_change_permission(self) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.change_{model_name}")

    @property
    def has_delete_permission(self) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.delete_{model_name}")

    @property
    def has_view_permission(self) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.view_{model_name}")
