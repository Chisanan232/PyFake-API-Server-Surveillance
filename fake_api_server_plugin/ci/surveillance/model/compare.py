"""
This module is responsible for comparing local and remote API configurations
to detect and summarize any differences. It provides functionality to identify
API changes, including additions, updates, and deletions, and records these
changes with statistical and detailed summaries.

!!! tip ""

    This module is new in version 0.2.0.

Classes:

- APIChangeType: Enum defining the types of changes (add, update, delete).

- ChangeStatistical: Records the count for each type of API change.

- ChangeSummary: Tracks detailed changes for each API, grouped by type.

- ChangeDetail: Combines statistical and detailed summaries, with methods
  to record changes.

- CompareInfo: Handles comparison between local and remote API configurations,
  detecting changes and updating the ChangeDetail instance.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from fake_api_server.model import MockAPI

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server import FakeAPIConfig


class APIChangeType(Enum):
    """
    Represents the types of API changes.

    This enumeration defines constants representing the different types
    of changes that can occur within an API. It can be used to provide a
    clear distinction between additions, updates, and deletions for better
    management and understanding of API modifications.

    :ivar ADD: Represents the addition of a new element (e.g., endpoint or feature) in the API.
    :type ADD: str
    :ivar UPDATE: Represents the modification or update of an existing element in the API.
    :type UPDATE: str
    :ivar DELETE: Represents the removal or deprecation of an element in the API.
    :type DELETE: str
    """

    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"


@dataclass
class ChangeStatistical:
    """
    Represents statistical data for changes, including additions, deletions,
    and updates.

    This class is used to track the count of different types of changes that may
    occur in a given process or dataset. The attributes include additions,
    deletions, and updates. The class can serve as a container for this data
    and provide an organized way to manage the statistics.

    :ivar add: The number of additions made.
    :type add: int
    :ivar delete: The number of deletions made.
    :type delete: int
    :ivar update: The number of updates made.
    :type update: int
    """

    add: int = 0
    delete: int = 0
    update: int = 0


@dataclass
class ChangeSummary:
    """
    Represents a summary of changes applied to HTTP methods across various endpoints.

    This class is designed to organize and store the information about additions,
    deletions, and updates of HTTP methods for specific endpoints. By categorizing
    changes into `add`, `delete`, and `update`, it facilitates tracking and managing
    modifications made to an application's API.

    :ivar add: Records newly added HTTP methods for specific endpoints. Each key
        represents an endpoint, and the corresponding value is a list of
        added HTTP methods.
    :type add: Dict[str, List[HTTPMethod]]
    :ivar delete: Keeps track of HTTP methods that were removed for specific endpoints.
        Each key represents an endpoint, and the value is a list of deleted
        HTTP methods.
    :type delete: Dict[str, List[HTTPMethod]]
    :ivar update: Holds information about HTTP methods that were updated for specific
        endpoints. Each key represents an endpoint, and the value is a list of
        updated HTTP methods.
    :type update: Dict[str, List[HTTPMethod]]
    """

    add: Dict[str, List[HTTPMethod]] = field(default_factory=dict)
    delete: Dict[str, List[HTTPMethod]] = field(default_factory=dict)
    update: Dict[str, List[HTTPMethod]] = field(default_factory=dict)


@dataclass
class ChangeDetail:
    """
    Encapsulates details of changes, including statistical data and summary information.

    This class is responsible for maintaining detailed records of changes, including
    tracking statistical data and summarizing changes for specific types of API changes.
    It uses `ChangeStatistical` and `ChangeSummary` as components to store this information
    and provides a method for recording new changes by their type and association with a
    specific API context.

    :ivar statistical: Tracks the statistical counts of changes categorized by change type.
    :type statistical: ChangeStatistical
    :ivar summary: Provides a summary of the changes categorized by change type, mapping
        API URLs to the respective HTTP methods affected.
    :type summary: ChangeSummary
    """

    statistical: ChangeStatistical = field(default_factory=ChangeStatistical)
    summary: ChangeSummary = field(default_factory=ChangeSummary)

    def record_change(self, api: MockAPI, change_type: APIChangeType) -> None:
        """
        Records and tracks changes in API statistics and summaries based on the reported
        change type and HTTP request method. This method updates the statistical counts
        and summaries for specific APIs with their associated change types.

        :param api: MockAPI object representing the API whose changes are being
            recorded.
        :param change_type: Enum `APIChangeType` indicating the type of change occurred
            (e.g., CREATE, UPDATE, DELETE).
        :return: None
        """
        api_change_statistical = getattr(self.statistical, change_type.value)
        setattr(self.statistical, change_type.value, api_change_statistical + 1)

        api_http_method = HTTPMethod[api.http.request.method.upper()]
        api_with_change_type: Dict[str, List[HTTPMethod]] = getattr(self.summary, change_type.value)
        if api.url not in api_with_change_type:
            api_with_change_type[api.url] = [api_http_method]
            setattr(self.summary, change_type.value, api_with_change_type)
        else:
            api_allow_methods = api_with_change_type[api.url]
            api_allow_methods.append(api_http_method)
            api_with_change_type[api.url] = api_allow_methods
            setattr(self.summary, change_type.value, api_with_change_type)


@dataclass
class CompareInfo:
    """
    Represents a comparison between local and remote API configurations.

    CompareInfo is designed to compare two API configurations (local and remote)
    and identify any differences between them. It also records changes such as
    added, updated, or deleted APIs.

    :ivar local_model: The local API configuration to be compared.
    :type local_model: FakeAPIConfig
    :ivar remote_model: The remote API configuration to be compared.
    :type remote_model: FakeAPIConfig
    :ivar change_detail: Records details about changes identified during comparison.
    :type change_detail: ChangeDetail
    """

    local_model: FakeAPIConfig
    remote_model: FakeAPIConfig
    change_detail: ChangeDetail = field(default_factory=ChangeDetail)

    def has_different(self) -> bool:
        """
        Checks if there are differences between the API configurations of the local model
        and the remote model. The function compares both the existence and content of
        the APIs in each model and flags any discrepancies.

        :raises AssertionError: If any API configuration in either local or remote
            model is `None`, indicating an unexpected state.

        :return: A boolean indicating whether there are differences between the local
            and remote API configurations.
        :rtype: bool
        """
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
        self.change_detail.record_change(api, APIChangeType.ADD)

    def _record_update_api(self, api: MockAPI) -> None:
        self.change_detail.record_change(api, APIChangeType.UPDATE)

    def _record_api_delete(self, api: MockAPI) -> None:
        self.change_detail.record_change(api, APIChangeType.DELETE)
