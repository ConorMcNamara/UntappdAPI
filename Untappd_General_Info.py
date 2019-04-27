from UntappdAPI import UntappdAPI


class UntappdGeneralInfo(UntappdAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def brewery_info_id(self, brewery_id, compact=None):
        """Returns the information of a brewery
        Parameters
        ----------
        brewery_id: str
            The id of the brewery
        compact: bool
            Pass "true" to return a compact listing of the brewery (optional)
        """
        method = "brewery/info/" + brewery_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params['compact'] = compact
        return self._do_get(method, auth, params)

    def brewery_info_name(self, brewery_name, compact=None):
        brewery_id = self._find_brewery_id(brewery_name)
        return self.brewery_info_id(brewery_id, compact)

    def beer_info_id(self, beer_id, compact=None):
        """
        Returns the information of a beer
        Arguments:
            beer_id = the id of the beer
            compact = pass "true" to return a compact listing of the beer (optional)
        """
        method = "beer/info/" + beer_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params['compact'] = compact
        return self._do_get(method, auth, params)

    def beer_info_name(self, beer_name, brewery_name, compact=None):
        beer_id = self._find_beer_id(beer_name, brewery_name)
        return self.beer_info_id(beer_id, compact)

    def venue_info_id(self, venue_id, compact=None):
        """Returns the information of a venue
        Parameters
        ----------
        venue_id: str
            The id of the venue
        compact: bool
            Pass "true" to return a compact listing of the venue (optional)
        """
        method = "venue/info/" + venue_id
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params['compact'] = compact
        return self._do_get(method, auth, params)

    def venue_info_name(self, venue_name, address, compact=None):
        venue_id = self._find_venue_id(venue_name, address)
        return self.venue_info_id(venue_id, compact)

    def checkin_info(self, checkin_id):
        """
        Returns the information of a checkin
        Arguments:
            checkin_id = the id of the checkin
        """
        method = "checkin/view/" + checkin_id
        auth = self._get_api_auth_token()
        return self._do_get(method, auth, {})

    def user_info(self, username, compact=None):
        """Returns the information of a user
        Parameters
        ----------
        username: str
            The username that the person goes by
        compact: bool
            Pass "true" to return a compact listing of the user (optional)
        """
        method = "user/info/" + username
        auth = self._get_api_auth_token()
        params = {}
        if compact:
            params['compact'] = compact
        return self._do_get(method, auth, params)

