import json

from typing import Dict, Optional

import urllib3
import pandas as pd

from urllib.parse import urlencode


class UntappdAPI:
    def __init__(self, client_id: str, client_secret: str) -> None:
        """ Base class for getting data from Untappd

        Parameters
        -----------
        client_id: str
            The Untappd API Client ID
        client_secret: str
            The Untappd API Client Secret
        """
        self.url = 'https://api.untappd.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = None
        self.user_auth_params = None
        self.https = urllib3.PoolManager()

    def set_auth(self, auth: str) -> None:
        """Method to set the auth token for a request given by Untappd's API after user authorization

        Parameters
        ----------
        auth: str
            Untappd API access token
        """
        self.auth = auth

    def _get_api_auth_token(self) -> str:
        """Internal function to get the access token if set, or the client ID and secret
        """
        if self.auth:
            return "access_token=" + self.auth
        else:
            return "client_id=" + self.client_id + "&client_secret=" + self.client_secret

    def _get_access_token(self) -> str:
        """Internal function to return the authed users access token
        """
        return "access_token=" + self.auth

    def _do_get(self, method: str, auth: str, params: Dict, fields: Optional[Dict] = None) -> Dict:
        """Internal Function to send GET requests

        Parameters
        -----------
        method: str
            Untappd API method
        auth: str
            URL encoding of Untappd API authorization tokens
        params: dictionary, default=None
            Params for the API request
        fields: dictionary
            Fields that we want returned from our request (optional)

        Returns
        -------
        A dictionary of our GET request
        """
        url = self.url + method + "?" + auth

        if params:
            params = urlencode(params)
            url = url + "&" + params
        if fields:
            response = self.https.request("GET", url, fields=fields)
        else:
            response = self.https.request("GET", url)
        return json.loads(response.data.decode('utf-8'))

    def _do_post(self, method: str, auth: str, params: Dict, fields: Optional[Dict] = None):
        """Internal Function to send POST requests

        Parameters
        ----------
        method: str
            Untappd API method
        auth: str
            URL encoding of Untappd API authorization tokens
        params: dictionary
            Params for the API request
        fields: dictionary, default=None
            Fields that we want returned from our request (optional)

        Returns
        -------
        A dictionary of our POST request
        """
        url = self.url + method + "?" + auth
        if params:
            params = urlencode(params)
            url = url + "&" + params
        if fields:
            response = self.https.request("POST", url, fields=fields)
        else:
            response = self.https.request("POST", url)
        return json.loads(response.data.decode('utf-8'))

    def _find_venue_id(self, venue_name: str, address: str) -> str:
        """Returns the venue id given a name and an address

        Parameters
        ----------
        venue_name: str
            The name of the venue
        address: str
            The street address of the venue

        Returns
        -------
        The venue_id of our given venue
        """
        data = self.venue_search(venue_name)
        address_df = pd.DataFrame()
        for j in range(data['response']['venues']['count']):
            address_df = pd.concat([address_df, pd.DataFrame.from_dict(data['response']['venues']['items'][j])])
        return address_df.loc[address_df['venue_address'] == address]['venue_id'][0]

    def _find_beer_id(self, beer_name: str, brewery_name: str) -> str:
        """Returns the beer id given the beer name and brewery name

        Parameters
        ----------
        beer_name: str
            The name of the beer
        brewery_name: str
            The name of the brewery that brewed this beer

        Returns
        -------
        The beer_id given our beer name and brewery name
        """
        data = self.beer_search(beer_name, fields={"brewery_name": brewery_name})
        return data['response']['beers']['items'][0]['beer']['bid']

    def _find_brewery_id(self, brewery_name: str) -> str:
        """Returns the brewery id given the brewery name

        Parameters
        ----------
        brewery_name: str
            The name of the brewery

        Returns
        -------
        The brewery_id given the brewery name
        """
        data = self.brewery_search(brewery_name)
        return data['response']['brewery']['items'][0]['brewery']['brewery_id']

    def brewery_search(self, query: str, fields: Optional[Dict] = None) -> Dict:
        """Returns the breweries matching a query

        Parameters
        ----------
        query: str
            The search term to search by
        fields: dict, default=None
            The specific values that we wish to filter our result by

        Returns
        -------
        A dictionary containing any breweries matching our query
        """
        method = "search/brewery"
        auth = self._get_api_auth_token()
        params = {
            "q": query
        }
        return self._do_get(method, auth, params, fields)

    def beer_search(self, query: str, sort: Optional[str] = None, fields: Optional[Dict] = None):
        """Returns the beer matching a query

        Parameters
        ----------
        query: str
            The search term to search by
        sort: str, default=None
            The value by which to sort the list (optional)
        fields: dict, default=None
            The specific values that we wish to filter our result by

        Returns
        -------
        A dictionary containing any beers that match our query
        """
        method = "search/beer"
        auth = self._get_api_auth_token()
        params = {
            "q": query
        }
        if sort:
            params['sort'] = sort
        return self._do_get(method, auth, params, fields)

    def venue_search(self, query: str, sort: Optional[str] = None, fields: Optional[Dict] = None):
        """Returns the venue matching the query

        Parameters
        ----------
        query: str
            The search term to search by
        sort: str, default=None
            The value by which to sort the list (optional)
        fields: dict, default=None
            The specific values we wish to filter our result by

        Returns
        -------
        A dictionary containing any venues that match our query
        """
        method = "search/venue"
        auth = self._get_api_auth_token()
        params = {
            "q": query
        }
        if sort:
            params['sort'] = sort
        return self._do_get(method, auth, params, fields)

    def foursquare_venue_search(self, venue_id: str) -> Dict:
        """Converts a Foursquare v2 ID in to a Untappd Venue ID

        Parameters
        ----------
        venue_id: str
            The Foursquare v2 ID you wish to convert

        Returns
        -------
        A dictionary with the converted Untappd Venue ID
        """
        method = "venue/foursquare_lookup/" + venue_id
        auth = self._get_api_auth_token()
        return self._do_get(method, auth, {})

    def beer_trending(self) -> Dict:
        """Returns the trending macro and micro beers
        """
        method = "beer/trending"
        auth = self._get_api_auth_token()
        return self._do_get(method, auth, {})