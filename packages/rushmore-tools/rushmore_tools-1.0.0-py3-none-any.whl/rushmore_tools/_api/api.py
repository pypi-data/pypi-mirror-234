"""API functions and related classes for RushmoreExtractor."""

import logging
from typing import Any, Dict, List, Optional, TypedDict, Union

import requests

logger = logging.getLogger(__name__)


class RushmoreResponse(TypedDict):
    """Type class for Rushmore Response."""

    TotalWells: int
    TotalPages: int
    PageInfo: dict[str, Any]
    Data: list[dict[str, Any]]


class RushmoreReport:
    """Basic class for adding reports as subclasses to RushmoreExtractor."""

    def __init__(
        self,
        report_name: str,
        api_key: str,
        page_size: Optional[int] = 1000,
        api_version: Optional[str] = "v0.2",
    ):
        self._api_key = api_key
        self._report_name = report_name.lower()
        self._page_size = page_size
        self._api_version = api_version

    @property
    def page_size(self):
        """For making page_size an editable property."""
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        if value > 0 and isinstance(value, int):
            self._page_size = value
        elif not isinstance(value, int):
            raise TypeError("Incorrect type. Specify a positive integer for page size.")
        else:
            raise ValueError(
                "Incorrect value. Specify a positive integer for page size."
            )

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, value):
        if isinstance(value, str):
            self._api_version = value
        else:
            raise ValueError("Incorrect value. Specify a string with API version.")

    def get(
        self,
        filter: Optional[str] = None,
        max_pages: Optional[int] = None,
        exclude_time_depth: Optional[bool] = True,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Retrieves all raw data from relevant Rushmore Review.

        Args:
            data_filter: Filtering string according to API specification.
            full_response: Pass True to retrieve full response from Rushmore.
              False retrieves only the well data list component.
            max_pages: Optional argument to reduce number of pages retrieved
              from Rushmore, for testing purposes.

        Returns:
            List of dicts where each dict describes an entry in the Rushmore
            Review.

        """

        output: Optional[RushmoreResponse] = None
        page = 1
        while True:
            logger.info(f"Fetching page {page} from {self._report_name}")
            response = self._get_page(
                page=page, filter=filter, exclude_time_depth=exclude_time_depth
            )

            # Response checker catches error / failure responses
            self._check_response(response)

            logger.info(f"Fetched {len(response['Data'])} rows.")
            if output:
                output["Data"].extend(  # pylint: disable=unsubscriptable-object
                    response["Data"]
                )
            else:
                output = response

            # Determine number of pages to fetch.
            if not max_pages:
                num_pages = response["TotalPages"]
            else:
                num_pages = min(max_pages, response["TotalPages"])

            if num_pages > page:
                page += 1
            else:
                logger.info(
                    f"Extraction complete. {len(output['Data']):,} rows fetched."
                )
                return output["Data"]

    def _get_page(
        self,
        page: Optional[int] = 1,
        filter: Optional[str] = None,
        exclude_time_depth: bool = True,
    ) -> RushmoreResponse:
        """Queries data from Rushmore.

        Args:
            page_size: Number of rows requested per page.
            page: The page number that is requested.
            data_filter: Custom filters for what data to include.

        Returns:
            One page of data from Rushmore as a JSON serializable
            dictionary with keys according to the standard API payload.
        """
        # Rushmore API uses X-API-key authorization.
        header = {"X-API-key": self._api_key}
        url = (
            "https://data-api.rushmorereviews.com/"
            + f"{self._api_version}/wells/{self._report_name}"
        )
        params = {"page": page, "pagesize": self.page_size, "filter": filter}

        if exclude_time_depth:
            params["excludeTimeDepth"] = True

        response = requests.get(url=url, headers=header, params=params)

        # Checks for non-2xx responses
        response.raise_for_status()

        return response.json()

    def _check_response(self, response: Dict[str, Any]) -> None:
        """Simple check for overflow error in response.

        Args:
            response: Rushmore API response.

        Raises:
            ValueError if page size causes response to overflow.
        """
        logger.debug("Checking response for error messages.")
        try:
            response["fault"]
        except KeyError:
            pass
        else:
            error: str = response["fault"]["faultstring"]
            if error == "Body buffer overflow":
                raise ValueError("Response too large. Reduce page size.")
        try:
            response["error"]
        except KeyError:
            pass
        else:
            error: str = response["error_description"]
            raise Exception(f"Error was thrown: {error}.")
