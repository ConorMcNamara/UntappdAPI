from UntappdAPI import UntappdAPI


class UntappdFriends(UntappdAPI):

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

    def pending_friends(self):
        """Returns a list of all the pending friend requests for a user
        """
        method = "user/pending"
        auth = self._get_access_token()
        return self._do_get(method, auth, {}, None)

    def accept_friend(self, target_user):
        """Accepts the friend request for a user
        Parameters
        ----------
        target_user: str
            The username of the friend request we are accepting
        """
        method = "friend/accept/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def reject_friend(self, target_user):
        """Rejects the friend request for a user
        Parameters
        ----------
        target_user: str
            The username of the friend request we are rejecting
        """
        method = "friend/reject/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def remove_friend(self, target_user):
        """Removes a friend
        Parameters
        ----------
        target_user: str
            The username of the friend we are removing
        """
        method = "friend/remove/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def request_friend(self, target_user):
        """Requests friendship to a user
        Parameters
        ----------
        target_user: str
            The username of the friend we are sending a friend request to
        """
        method = "friend/request/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)
