"""Untappd API Feed Calls
"""
from UntappdAPI import UntappdAPI


class UntappdFeed(UntappdAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def friend_feed(self, max_id=None, limit=None):
        """Returns the friends checkin feed
        Parameters
        ----------
        max_id: str
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
        """
        method = 'checkin/recent'
        auth = self._get_access_token()
        params = {}
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def user_feed(self, username, max_id=None, limit=None):
        """Returns the checkin feed of a specific user
        Parameters
        ----------
        username: str
            The username of the user
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
        """
        method = 'user/checkin/' + username
        auth = self._get_api_auth_token()
        params = {}
        if max_id:
            params['max_id'] = max_id
        if limit:
            params['limit'] = limit
        return self._do_get(method, auth, params)

    def pub_feed(self, **kwargs):
        """Returns the checkin feed of around a location
        Parameters
        ----------
        min_id: str
            The checkin id of the most recent checkin (optional)
        lng: str
            The longitude of the public feed (optional)
        lat: str
            The latitude of the public feed (optional)
        radius: int
            The max radius the checkins start from (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
        """
        method = 'thepub/local'
        auth = self._get_api_auth_token()
        params = {}
        if 'min_id' in kwargs:
            params['min_id'] = kwargs['min_id']
        if 'lng' in kwargs:
            params['lng'] = kwargs['lng']
        if 'lat' in kwargs:
            params['lat'] = kwargs['lat']
        if 'radius' in kwargs:
            params['radius'] = kwargs['radius']
        if 'max_id' in kwargs:
            params['max_id'] = kwargs['max_id']
        if 'limit' in kwargs:
            params['limit'] = kwargs['limit']
        return self._do_get(method, auth, params)

    def venue_feed_id(self, venue_id, min_id=None, max_id=None, limit=None):
        """Returns the feed of a venue by id
        Parameters
        ----------
        venue_id: str
            The id of the venue
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
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

    def venue_feed_name(self, venue_name, address, min_id=None, max_id=None, limit=None):
        """Returns the feed of a venue by name
        Parameters
        ----------
        venue_name: str
            The name of the venue
        address: str
            The street address of the venue
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
        """
        venue_id = self._find_venue_id(venue_name, address)
        return self.venue_feed_id(venue_id, min_id, max_id, limit)

    def beer_feed_id(self, beer_id, min_id=None, max_id=None, limit=None):
        """Returns the feed of a beer by id
        Parameters
        ----------
        beer_id: str
            The id of the beer
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
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

    def beer_feed_name(self, beer_name, brewery_name, min_id=None, max_id=None, limit=None):
        """Returns the feed of a beer by name
        Parameters
        ----------
        beer_name: str
            The name of the beer
        brewery_name: str
            The name of the brewery
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
        """
        beer_id = self._find_beer_id(beer_name, brewery_name)
        return self.beer_feed_id(beer_id, min_id, max_id, limit)

    def brewery_feed_id(self, brewery_id, min_id=None, max_id=None, limit=None):
        """Returns the feed of a brewery by id
        Parameters
        ----------
        brewery_id: str
            The id of the brewery
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
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

    def brewery_feed_name(self, brewery_name, min_id=None, max_id=None, limit=None):
        """Returns the feed of a brewery by name
        Parameters
        ----------
        brewery_name: str
            The name of the brewery
        min_id: int
            The checkin id of the most recent checkin (optional)
        max_id: int
            Checkin id the results will start with (optional)
        limit: int
            Number of results to return (optional)
            """
        brewery_id = self._find_brewery_id(brewery_name)
        return self.brewery_feed_id(brewery_id, min_id, max_id, limit=limit)
