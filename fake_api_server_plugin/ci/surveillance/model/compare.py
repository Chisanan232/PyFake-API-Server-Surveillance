from dataclasses import dataclass

from fake_api_server import FakeAPIConfig


@dataclass
class CompareInfo:
    local_model: FakeAPIConfig
    remote_model: FakeAPIConfig

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
