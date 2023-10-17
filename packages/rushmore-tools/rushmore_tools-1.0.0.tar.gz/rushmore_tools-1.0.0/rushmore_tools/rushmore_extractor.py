"""Module for extracting data from the IHS Markit Rushmore API.

The module abstracts the operation of extracting data from the API,
allowing for swift retrieval of data from specific performance reviews.
Includes possibility for passing filters to fetch only desired data.

  Typical usage example:
  >>> ex = RushmoreExtractor(${API key})
  >>> # Get all completions
  >>> completions = ex.completions.get()
  >>> # Get all drill wells in Norway
  >>> flt = 'Location.Country eq "Norway"'
  >>> drilling_norway = ex.drilling.get(filter=flt)

"""

import logging
from typing import Literal, Optional

from ._api.api import RushmoreReport

logger = logging.getLogger(__name__)


class RushmoreExtractor:
    """Class used to extract raw data from the Rushmore API.

    Typical usage:
        >>> e = RushmoreExtractor(${API-KEY})
        >>> drilling_data = e.drilling.get()

    Args:
        api_key: The X-API-Key provided to Rushmore participants that
          allows access to the Rushmore API.
    """

    def __init__(
        self,
        api_key: str,
    ) -> None:
        self._api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        if isinstance(value, str):
            self._api_key = value
        else:
            raise ValueError("Not a valid API key.")

    def report(
        self,
        report: Literal["APR", "CPR", "DPR"],
        page_size: int = 1000,
        api_version: Optional[str] = "v0.1",
    ):
        return RushmoreReport(
            report,
            api_key=self._api_key,
            page_size=page_size,
            api_version=api_version,
        )
