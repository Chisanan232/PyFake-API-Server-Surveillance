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
        all_new_api_configs = self.remote_model.apis.apis
        for api_key in all_new_api_configs.keys():
            if api_key in all_api_configs.keys():
                one_api_config = all_api_configs[api_key]
                one_new_api_config = all_new_api_configs[api_key]
                assert one_api_config is not None, "It's strange. Please check it."
                assert one_new_api_config is not None, "It's strange. Please check it."
                has_api_change = one_api_config == one_new_api_config
            else:
                has_api_change = True
                break
        return has_api_change
