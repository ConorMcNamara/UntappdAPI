from typing import Dict

from UntappdAPI import UntappdAPI


class UntappdFriends(UntappdAPI):

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)

    def pending_friends(self) -> Dict:
        """Returns a dictionary of all the pending friend requests for a user
        """
        method = "user/pending"
        auth = self._get_access_token()
        return self._do_get(method, auth, {}, None)

    def accept_friend(self, target_user: str) -> Dict:
        """Accepts the friend request for a user

        Parameters
        ----------
        target_user: str
            The username of the friend request we are accepting

        Returns
        -------
        A dictionary of our POST request for accepting a friend request
        """
        method = "friend/accept/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def reject_friend(self, target_user: str) -> Dict:
        """Rejects the friend request for a user

        Parameters
        ----------
        target_user: str
            The username of the friend request we are rejecting

        Returns
        -------
        A dictionary of our POST request for denying a friend request
        """
        method = "friend/reject/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def remove_friend(self, target_user: str) -> Dict:
        """Removes a friend

        Parameters
        ----------
        target_user: str
            The username of the friend we are removing

        Returns
        -------
        A dictionary of the POST request for removing a friend
        """
        method = "friend/remove/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)

    def request_friend(self, target_user: str) -> Dict:
        """Requests friendship to a user

        Parameters
        ----------
        target_user: str
            The username of the friend we are sending a friend request to

        Returns
        -------
        A dictionary of the POST request for the user we are friending
        """
        method = "friend/request/" + target_user
        auth = self._get_access_token()
        return self._do_post(method, auth, {}, None)