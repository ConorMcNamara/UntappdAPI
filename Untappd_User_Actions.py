import UntappdAPI


class UntappdUserActions(UntappdAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def checkin(self, gmt_offset, timezone, beer_id, **kwargs):
        """
        Checks in a beer for a user
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
        facebook: str
            Pass "on" to post the checkin to Facebook (optional)
        twitter: str
            Pass "on" to post the checkin to Twitter (optional)
        foursquare: str
            Pass "on" to post the checkin to Foursquare (optional)
        instagram: str
            Pass "on" to post the checkin to Instagram (optional)
        """
        method = "checkin/add"
        auth = self._get_access_token()
        params = {
            "gmt_offset": gmt_offset,
            "timezone": timezone,
            "bid": beer_id
        }
        if "foursquare_id" in kwargs:
            params['foursquare_id'] = kwargs['foursquare_id']
        if "geolat" in kwargs:
            params["geolat"] = kwargs["geolat"]
        if "geolng" in kwargs:
            params["geolng"] = kwargs["geolng"]
        if "shout" in kwargs:
            params["shout"] = kwargs["shout"]
        if "rating" in kwargs:
            params["rating"] = kwargs["rating"]
        if "facebook" in kwargs:
            params["facebook"] = kwargs["facebook"]
        if "twitter" in kwargs:
            params["twitter"] = kwargs["twitter"]
        if "foursquare" in kwargs:
            params["foursquare"] = kwargs["foursquare"]
        if "instagram" in kwargs:
            params["instagram"] = kwargs["instagram"]
        return self._do_post(method, auth, params)

    def add_comment(self, checkin_id, comment):
        """Adds a comment to a checkin
        Parameters
        ----------
        checkin_id: str
            The id of the checkin to add a comment to
        comment: str
            The text to add as a comment
        """
        method = "checkin/addcomment/" + checkin_id
        auth = self._get_access_token()
        if len(comment) > 140:
            raise Exception("Comment has too many characters for Untappd")
        params = {
            "comment": comment
        }
        return self._do_post(method, auth, params)

    def remove_comment(self, comment_id):
        """Removes a comment on a checkin
        Parameters
        ----------
        comment_id: str
            The id of the comment to be removed
        """
        method = "checkin/deletecomment/" + comment_id
        auth = self._get_access_token()
        return self._do_post(method, auth, {})

    def toast(self, checkin_id):
        """Toggles the toast option on a checkin for a user
        Parameters
        ----------
        checkin_id: str
            The id of the checkin to toggle the toast option
        """
        method = "checkin/toast/" + checkin_id
        auth = self._get_access_token()
        return self._do_post(method, auth, {})

    def add_to_wishlist(self, beer_id):
        """Adds a beer to a users wishlist
        Parameters
        ----------
        beer_id: str
            The beer id of the beer to add to the wishlist
        """
        method = "user/wishlist/add"
        auth = self._get_access_token()
        params = {
            "bid": beer_id
        }
        return self._do_get(method, auth, params)

    def remove_from_wishlist(self, beer_id):
        """Removes a beer from a users wishlist
        Parameters
        ----------
        beer_id: str
            The beer id of the beer to remove from the wishlist
        """
        method = "user/wishlist/delete"
        auth = self._get_access_token()
        params = {
            "bid": beer_id
        }
        return self._do_get(method, auth, params)
