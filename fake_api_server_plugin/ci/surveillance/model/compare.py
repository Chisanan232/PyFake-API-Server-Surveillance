from dataclasses import dataclass, field
from typing import Dict, List

from fake_api_server.model import MockAPI

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[assignment]

from fake_api_server import FakeAPIConfig


@dataclass
class ChangeStatistical:
    add: int = 0
    delete: int = 0
    update: int = 0


@dataclass
class ChangeDetail:
    change_statistical: ChangeStatistical = field(default_factory=ChangeStatistical)
    apis: Dict[str, List[HTTPMethod]] = field(default_factory=dict)

    def record_change(self, api: MockAPI) -> None:
        api_http_method = HTTPMethod[api.http.request.method.upper()]
        if api.url not in self.apis:
            self.apis[api.url] = [api_http_method]
        else:
            api_allow_methods = self.apis[api.url]
            api_allow_methods.append(api_http_method)
            self.apis[api.url] = api_allow_methods


@dataclass
class CompareInfo:
    local_model: FakeAPIConfig
    remote_model: FakeAPIConfig
    change_detail: ChangeDetail = field(default_factory=ChangeDetail)

    def has_different(self) -> bool:
        has_api_change = False
        all_api_configs = self.local_model.apis.apis
        api_keys = all_api_configs.keys()
        all_new_api_configs = self.remote_model.apis.apis
        new_api_keys = all_new_api_configs.keys()
        for api_key in all_new_api_configs.keys():
            if api_key in all_api_configs.keys():
                one_api_config = all_api_configs[api_key]
                one_new_api_config = all_new_api_configs[api_key]
                assert one_api_config is not None, "It's strange. Please check it."
                assert one_new_api_config is not None, "It's strange. Please check it."
                api_is_diff = one_api_config != one_new_api_config
                if api_is_diff:
                    has_api_change = True
                    self._record_update_api(one_new_api_config)
            else:
                has_api_change = True
                self._record_add_api(all_new_api_configs[api_key])

        if len(api_keys) != len(new_api_keys):
            for api_key in api_keys:
                if api_key not in new_api_keys:
                    has_api_change = True
                    self._record_api_delete(all_api_configs[api_key])
        return has_api_change

    def _record_add_api(self, api: MockAPI) -> None:
        self.change_detail.change_statistical.add += 1
        self.change_detail.record_change(api)

    def _record_update_api(self, api: MockAPI) -> None:
        self.change_detail.change_statistical.update += 1
        self.change_detail.record_change(api)

    def _record_api_delete(self, api: MockAPI) -> None:
        self.change_detail.change_statistical.delete += 1
        self.change_detail.record_change(api)
