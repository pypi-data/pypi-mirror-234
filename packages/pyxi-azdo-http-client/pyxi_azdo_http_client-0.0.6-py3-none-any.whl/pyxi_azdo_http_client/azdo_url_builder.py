from .url_builder import UrlBuilder
from typing import Optional


class AzdoUrlBuilder:
    def __init__(
        self,
        organization: str,
        project_name: str,
        default_api_version: Optional[str] = "7.0",
    ):
        self._organization = organization
        self._project_name = project_name
        self._default_api_version = default_api_version
        self._base_url = (
            f"https://dev.azure.com/{self._organization}/{self._project_name}/_apis/"
        )

    def base_url_builder(self):
        return UrlBuilder(self._base_url)

    def build_workitem_detail_url(self, work_item_id: int) -> str:
        builder = (
            self.base_url_builder()
            .add_path_segment("wit")
            .add_path_segment("workitems")
            .add_path_segment(str(work_item_id))
            .add_query_param("$expand", "all")
            .add_query_param("api-version", self._default_api_version)
        )

        return builder.build()

    def build_wiql_url(self) -> str:
        builder = (
            self.base_url_builder()
            .add_path_segment("wit")
            .add_path_segment("wiql")
            .add_query_param("api-version", self._default_api_version)
        )

        return builder.build()
