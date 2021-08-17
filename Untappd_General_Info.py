from typing import Dict, Optional

from UntappdAPI import UntappdAPI


class UntappdGeneralInfo(UntappdAPI):
    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)

    def brewery_info_id(self, brewery_id: str, compact: Optional[bool] = None) -> Dict:
        """Returns the information of a brewery

        Parameters
        ----------
        brewery_id: str
            The id of the brewery
        compact: bool, default=None
            Pass "true" to return a compact listing of the brewery (optional)

        Returns
        -------
        A dictionary containing information about the brewery
        """
        method = "brewery/info/" + brewery_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params["compact"] = compact
        return self._do_get(method, auth, params)

    def brewery_info_name(
        self, brewery_name: str, compact: Optional[bool] = None
    ) -> Dict:
        """Returns the information of a brewery by name

        Parameters
        ----------
        brewery_name: str
            The name of the brewery
        compact: bool, default=None
            Pass "true" to return a compact listing of the beer (optional)

        Returns
        -------
        A dictionary containing information about the brewery
        """
        brewery_id = self._find_brewery_id(brewery_name)
        return self.brewery_info_id(brewery_id, compact)

    def beer_info_id(self, beer_id: str, compact: Optional[bool] = None) -> Dict:
        """Returns the information of a beer by id

        Parameters
        ----------
        beer_id: str
            The id of the beer
        compact: bool, default=None
            Pass "true" to return a compact listing of the beer (optional)

        Returns
        -------
        A dictionary containing information about the beer
        """
        method = "beer/info/" + beer_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params["compact"] = compact
        return self._do_get(method, auth, params)

    def beer_info_name(
        self, beer_name: str, brewery_name: str, compact: Optional[bool] = None
    ) -> Dict:
        """Returns the information of a beer by name

        Parameters
        ----------
        beer_name: str
            The name of the beer
        brewery_name: str
            The name of the brewery that the beer was brewed at
        compact: bool, default=None
            Pass "true" to return a compact listing of the beer (optional)

        Returns
        -------
        A dictionary containing information about the beer
        """
        beer_id = self._find_beer_id(beer_name, brewery_name)
        return self.beer_info_id(beer_id, compact)

    def venue_info_id(self, venue_id: str, compact: Optional[bool] = None) -> Dict:
        """Returns the information of a venue by id

        Parameters
        ----------
        venue_id: str
            The id of the venue
        compact: bool, default=None
            Pass "true" to return a compact listing of the venue (optional)

        Returns
        -------
        A dictionary containing information about the venue
        """
        method = "venue/info/" + venue_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params["compact"] = compact
        return self._do_get(method, auth, params)

    def venue_info_name(
        self, venue_name: str, address: str, compact: Optional[bool] = None
    ):
        """Returns the information of a venue by name

        Parameters
        ----------
        venue_name: str
            The name of the venue
        address: str
            The street address of the venue
        compact: bool, default=None
            Pass "true" to return a compact listing of the venue (optional)

        Returns
        -------
        A dictionary containing information about the venue
        """
        venue_id = self._find_venue_id(venue_name, address)
        return self.venue_info_id(venue_id, compact)

    def checkin_info(self, checkin_id: str) -> Dict:
        """Returns the information of a checkin

        Parameters
        ----------
        checkin_id: str
            The id of the checkin

        Returns
        -------
        A dictionary containing information about the check-in
        """
        method = "checkin/view/" + checkin_id
        auth = self._get_api_auth_token()
        return self._do_get(method, auth, {})

    def user_info(self, username: str, compact: Optional[bool] = None) -> Dict:
        """Returns the information of a user

        Parameters
        ----------
        username: str
            The username that the person goes by
        compact: bool, default=None
            Pass "true" to return a compact listing of the user (optional)

        Returns
        -------
        A dictionary containing information about the user
        """
        method = "user/info/" + username
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params["compact"] = compact
        return self._do_get(method, auth, params)
