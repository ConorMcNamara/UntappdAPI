from typing import Dict, Optional

from UntappdAPI import UntappdAPI


class UntappdUserActions(UntappdAPI):

    def __init__(self, client_id: str, client_secret: str):
        super().__init__(client_id, client_secret)

    def checkin(self,
                gmt_offset: int,
                timezone: str,
                beer_id: str,
                foursquare_id: Optional[str],
                geolat: Optional[int],
                geolng: Optional[int],
                shout: Optional[str],
                rating: Optional[float],
                facebook: Optional[bool],
                twitter: Optional[bool],
                foursquare: Optional[bool],
                instagram: Optional[bool]) -> Dict:
        """Checks in a beer for a user

        Parameters
        ----------
        gmt_offset: int
            The numeric offset the user is away from GMT
        timezone: str
            The timezone of the user
        beer_id: str
            The id of the beer the user is checking in
        foursquare_id: str
            MD5 hash of the venue id (optional)
        geolat: int
            The numeric latitude of the user, required if adding location (optional)
        geolng: int
            The numeric longitude of the user, required if adding location (optional)
        shout: str
            Text to be added as a comment to the checkin (optional)
        rating: float
            The numeric rating for the beer being checked in (optional)
        facebook: bool
            Pass "on" to post the checkin to Facebook (optional)
        twitter: bool
            Pass "on" to post the checkin to Twitter (optional)
        foursquare: bool
            Pass "on" to post the checkin to Foursquare (optional)
        instagram: bool
            Pass "on" to post the checkin to Instagram (optional)

        Returns
        -------
        A dictionary of our check-in
        """
        method = "checkin/add"
        auth = self._get_access_token()
        params = {
            "gmt_offset": gmt_offset,
            "timezone": timezone,
            "bid": beer_id
        }
        if foursquare_id:
            params['foursquare_id'] = foursquare_id
        if geolat:
            params['geolat'] = geolat
        if geolng:
            params['geolng'] = geolng
        if shout:
            if len(shout) > 256:
                raise ValueError(f"Check-in shout is {len(shout)} characters whereas Untappd only supports shouts up to 256 characters")
            params["shout"] = shout
        if rating:
            if rating > 5:
                raise ValueError(f"Check-in rating is {rating} whereas Untappd only supports ratings up to 5")
        if facebook:
            params['facebook'] = 'on'
        if twitter:
            params['twitter'] = 'on'
        if foursquare:
            params['foursquare'] = 'on'
        if instagram:
            params['instagram'] = 'on'
        return self._do_post(method, auth, params)

    def add_comment(self, checkin_id: str, comment: str) -> Dict:
        """Adds a comment to a checkin

        Parameters
        ----------
        checkin_id: str
            The id of the checkin to add a comment to
        comment: str
            The text to add as a comment

        Returns
        -------
        A dictionary of our comment to our check-in
        """
        method = "checkin/addcomment/" + checkin_id
        auth = self._get_access_token()
        if len(comment) > 140:
            raise ValueError(
                f"Check-in comment is {len(comment)} characters whereas Untappd only supports comments up to 140 characters")
        params = {
            "comment": comment
        }
        return self._do_post(method, auth, params)

    def remove_comment(self, comment_id: str) -> Dict:
        """Removes a comment on a checkin

        Parameters
        ----------
        comment_id: str
            The id of the comment to be removed

        Returns
        -------
        A dictionary of us removing our comment
        """
        method = "checkin/deletecomment/" + comment_id
        auth = self._get_access_token()
        return self._do_post(method, auth, {})

    def toast(self, checkin_id: str) -> Dict:
        """Toggles the toast option on a checkin for a user

        Parameters
        ----------
        checkin_id: str
            The id of the checkin to toggle the toast option

        Returns
        -------
        A dictionary of us toasting a checkin
        """
        method = "checkin/toast/" + checkin_id
        auth = self._get_access_token()
        return self._do_post(method, auth, {})

    def add_to_wishlist(self, beer_id: str) -> Dict:
        """Adds a beer to a users wishlist

        Parameters
        ----------
        beer_id: str
            The beer id of the beer to add to the wishlist

        Returns
        -------
        A dictionary of us adding a beer to our wishlist
        """
        method = "user/wishlist/add"
        auth = self._get_access_token()
        params = {
            "bid": beer_id
        }
        return self._do_get(method, auth, params)

    def remove_from_wishlist(self, beer_id: str):
        """Removes a beer from a users wishlist

        Parameters
        ----------
        beer_id: str
            The beer id of the beer to remove from the wishlist

        Returns
        -------
        A dictionary of us removing a beer from our wishlist
        """
        method = "user/wishlist/delete"
        auth = self._get_access_token()
        params = {
            "bid": beer_id
        }
        return self._do_get(method, auth, params)