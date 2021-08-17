"""Untappd API Feed Calls
"""
from typing import Optional

from UntappdAPI import Dict, UntappdAPI


class UntappdFeed(UntappdAPI):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)

    def friend_feed(self, max_id: Optional[str] = None, limit: Optional[int] = None) -> Dict:
        """Returns the friends' check-in feed

        Parameters
        ----------
        max_id: str, default=None
            Check-in id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of the friends' check-in feed
        """
        method = 'checkin/recent'
        auth = self._get_access_token()
        params = {}
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def user_feed(self, username: str, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the check-in feed of a specific user

        Parameters
        ----------
        username: str
            The username of the user
        max_id: int, default=None
            Check-in id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of a users' check-in feed
        """
        method = 'user/checkin/' + username
        auth = self._get_api_auth_token()
        params = {}
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def pub_feed(self, min_id: Optional[str], lng: Optional[str], lat: Optional[str], radius: Optional[int], max_id: Optional[int], limit: Optional[int]) -> Dict:
        """Returns the public feed of a location

        Parameters
        ----------
        min_id: str, default=None
            The checkin id of the most recent checkin (optional)
        lng: str, default=None
            The longitude of the public feed (optional)
        lat: str, default=None
            The latitude of the public feed (optional)
        radius: int, default=None
            The max radius the checkins start from (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of the public feed
        """
        method = 'thepub/local'
        auth = self._get_api_auth_token()
        params = {}
        if min_id:
            params['min_id'] = min_id
        if lng:
            params['lng'] = lng
        if lat:
            params['lat'] = lat
        if radius:
            params['radius'] = radius
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def venue_feed_id(self, venue_id: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a venue by id

        Parameters
        ----------
        venue_id: str
            The id of the venue
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary containing the feed of our venue_id
        """
        method = "venue/checkins/" + venue_id
        auth = self._get_api_auth_token()
        params = {}
        if min_id:
            params['min_id'] = min_id
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def venue_feed_name(self, venue_name: str, address: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a venue by name

        Parameters
        ----------
        venue_name: str
            The name of the venue
        address: str
            The street address of the venue
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of the feed of our venue name
        """
        venue_id = str(self._find_venue_id(venue_name, address))
        return self.venue_feed_id(venue_id, min_id, max_id, limit)

    def beer_feed_id(self, beer_id: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a beer by id

        Parameters
        ----------
        beer_id: str
            The id of the beer
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary containing the feed of our beer id
        """
        method = "beer/checkins/" + beer_id
        auth = self._get_api_auth_token()
        params = {}
        if min_id:
            params['min_id'] = min_id
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def beer_feed_name(self, beer_name: str, brewery_name: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a beer by name

        Parameters
        ----------
        beer_name: str
            The name of the beer
        brewery_name: str
            The name of the brewery
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary containing the feed our beer name
        """
        beer_id = str(self._find_beer_id(beer_name, brewery_name))
        return self.beer_feed_id(beer_id, min_id, max_id, limit)

    def brewery_feed_id(self, brewery_id: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a brewery by id

        Parameters
        ----------
        brewery_id: str
            The id of the brewery
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary containing the feed of our brewery id
        """
        method = "brewery/checkins/" + brewery_id
        auth = self._get_api_auth_token()
        params = {}
        if min_id:
            params['min_id'] = min_id
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def brewery_feed_name(self, brewery_name: str, min_id: Optional[int] = None, max_id: Optional[int] = None, limit: Optional[int] = None) -> Dict:
        """Returns the feed of a brewery by name

        Parameters
        ----------
        brewery_name: str
            The name of the brewery
        min_id: int, default=None
            The checkin id of the most recent checkin (optional)
        max_id: int, default=None
            Checkin id the results will start with (optional)
        limit: int, default=None
            Number of results to return (optional)

        Returns
        -------
        A dictionary of containing the feed of our brewery name
        """
        brewery_id = self._find_brewery_id(brewery_name)
        return self.brewery_feed_id(brewery_id, min_id, max_id, limit=limit)