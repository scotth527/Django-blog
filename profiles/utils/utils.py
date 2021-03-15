from profiles.models import Friendship
from django.db.models import Q

def get_friendlist(user):
    """
    :param user: Must be an instance of the user object
    :return: A list of users that have accepted the friend request.
    """
    user_is_requester = Q(requester=user)
    user_is_requestee = Q(requestee=user)
    friendship_accepted = Q(status="Accept")
    friendship_query = Friendship.objects.filter((user_is_requester | user_is_requestee) & friendship_accepted)
    friend_list = [(friendship.requestee if friendship.requestee != user else friendship.requester) for friendship in
                   friendship_query]
    return friend_list