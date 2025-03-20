from dataclasses import dataclass, field
from typing import Dict, List
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
                has_api_change = one_api_config == one_new_api_config

                if has_api_change:
                    self.change_detail.change_statistical.update += 1
                    if one_new_api_config.url not in self.change_detail.apis:
                        self.change_detail.apis[one_new_api_config.url] = [HTTPMethod[one_new_api_config.http.request.method.upper()]]
                    else:
                        api_allow_methods = self.change_detail.apis[one_new_api_config.url]
                        api_allow_methods.append(HTTPMethod[one_new_api_config.http.request.method.upper()])
                        self.change_detail.apis[one_new_api_config.url] = api_allow_methods
            else:
                has_api_change = True

                new_api = all_new_api_configs[api_key]
                self.change_detail.change_statistical.add += 1
                if new_api.url not in self.change_detail.apis:
                    self.change_detail.apis[new_api.url] = [HTTPMethod[new_api.http.request.method.upper()]]
                else:
                    api_allow_methods = self.change_detail.apis[new_api.url]
                    api_allow_methods.append(HTTPMethod[new_api.http.request.method.upper()])
                    self.change_detail.apis[new_api.url] = api_allow_methods

        if len(api_keys) != len(new_api_keys):
            for api_key in api_keys:
                if api_key not in new_api_keys:
                    has_api_change = True
                    api = all_api_configs[api_key]
                    self.change_detail.change_statistical.delete += 1
                    if api_key not in self.change_detail.apis:
                        self.change_detail.apis[api.url] = [HTTPMethod[api.http.request.method.upper()]]
                    else:
                        api_allow_methods = self.change_detail.apis[api.url]
                        api_allow_methods.append(HTTPMethod[api.http.request.method.upper()])
                        self.change_detail.apis[api.url] = api_allow_methods
        return has_api_change
