from typing import Dict, Optional

from UntappdAPI import UntappdAPI


class UntappdUserInfo(UntappdAPI):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)

    def user_badges(self, username: str, offset: Optional[int] = None) -> Dict:
        """Returns a dictionary of the users badges

        Parameters
        ----------
        username: str
            The username of the user
        offset: int, default=None
            The numeric offset where the results start (optional)

        Returns
        -------
        A dictionary of the users' badges
        """
        method = "user/badges/" + username
        auth = self._get_access_token()
        params = {}
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_friends(self, username: str, offset: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns a dictionary of the users' friends

        Parameters
        ----------
        username: str
            The username of the user
        offset: int, default=None
            The numeric offset where the results start (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of the users' friends
        """
        method = "user/friends/" + username
        auth = self._get_api_auth_token()
        params = {}
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def user_wishlist(self, username: str, sort: Optional[str] = None, offset: Optional[int] = None) -> Dict:
        """Returns a dictionary of the users wishlisted beers

        Parameters
        ----------
        username: str
            The username of the user
        sort: str, default=None
            The value by which to sort the list (optional)
        offset: int, default=None
            The numeric offset where the results start (optional)

        Returns
        -------
        A dictionary of the users' wishlisted beers
        """
        method = "user/wishlist/" + username
        auth = self._get_api_auth_token()
        params = {}
        if sort:
            params['sort'] = sort
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_distinct_beers(self, username: str, sort: Optional[str] = None, offset: Optional[int] = None):
        """Returns a list of the distinct beers a user has had

        Parameters
        ----------
        username: str
            The username of a user
        sort: str, default=None
            The value by which to sort the list (optional)
        offset: int, default=None
            The numeric offset where the results start (optional)

        Returns
        -------
        A dictionary of the distinct beers a users has had
        """
        method = "user/beers/" + username
        auth = self._get_api_auth_token()
        params = {}
        if sort:
            params['sort'] = sort
        if offset:
            params['offset'] = offset
        return self._do_get(method, auth, params)

    def user_notifications(self) -> Dict:
        """Returns a dictionary of notifications for a user
        """
        method = "notifications"
        auth = self._get_access_token()
        return self._do_get(method, auth, {}, None)