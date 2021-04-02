from profiles.models import Friendship, Profile
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
    # Append the friendship id to each
    for i, friendship in enumerate(friendship_query):
        friend_list[i].friendship_id = friendship.id

    return friend_list

def get_friend_suggestions(user):
    """
        :param user: Must be an instance of the profile object
        :return: A list of users that are in the same city that have not been friend requested.
    """
    profile_is_in_same_city = Q(city=user.city)
    user_is_requester = Q(requester=user)
    user_is_requestee = Q(requestee=user)

    friendship_suggestion_query = Profile.objects.filter()

    return friendship_suggestion_query
