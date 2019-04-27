import UntappdAPI


class UntappdUserInfo(UntappdAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def user_badges(self, username, offset=None):
        """Returns a list of the users badges
        Parameters
        ----------
        username: str
            The username of the user
        offset: int
            The numeric offset where the results start (optional)
        """
        method = "user/badges/" + username
        auth = self._get_access_token()
        params = {}
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_friends(self, username, offset=None, limit=None):
        """Returns a list of the users friends
        Parameters
        ----------
        username: str
            The username of the user
        offset: int
            The numeric offset where the results start (optional)
        limit: int
            Number of results to return (optional)
        """
        method = "user/friends/" + username
        auth = self._get_api_auth_token()
        params = {}
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def user_wishlist(self, username, sort=None, offset=None):
        """Returns a list of the users wishlisted beers
        Parameters
        ----------
        username: str
            The username of the user
        sort: str
            The value by which to sort the list (optional)
        offset: int
            The numeric offset where the results start (optional)
        """
        method = "user/wishlist/" + username
        auth = self._get_api_auth_token()
        params = {}
        if sort:
            params['sort'] = sort
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_distinct_beers(self, username, sort=None, offset=None):
        """Returns a list of the distinct beers a user has had
        Parameters
        ----------
        username: str
            The username of a user
        sort: str
            The value by which to sort the list (optional)
        offset: int
            The numeric offset where the results start (optional)
        """
        method = "user/beers/" + username
        auth = self._get_api_auth_token()
        params = {}
        if sort:
            params['sort'] = sort
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_notifications(self):
        """Returns a list of notifications for a user
        """
        method = "notifications"
        auth = self._get_access_token()
        return self._do_get(method, auth, {}, None)
