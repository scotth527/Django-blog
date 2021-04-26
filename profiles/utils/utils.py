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


def get_friend_suggestions(user, suggestion_count=5):
    """
    :param user: Must be an instance of the profile object
    :return: A list of users that are in the same city that have not been friend requested.
    """
    profile = user.profile
    profile_is_in_same_city = Q(city=profile.city)
    profile_is_in_same_state = Q(state=profile.state)
    is_not_user = ~Q(id=user.id)
    user_is_requester = Q(requester=user)
    user_is_requestee = Q(requestee=user)

    friendship_query = Friendship.objects.filter(user_is_requester | user_is_requestee)
    friend_list = [(friendship.requestee if friendship.requestee != user else friendship.requester) for friendship in
                   friendship_query]

    friendship_suggestion_query = Profile.objects.exclude(user__in=friend_list).filter(
        profile_is_in_same_city & profile_is_in_same_state & is_not_user)[:5]
    friendship_suggestion_length = len(friendship_suggestion_query)
    if friendship_suggestion_length < suggestion_count:
        # Concatenate those in their same city/state with others not in their city up to 5
        remaining_suggestion_count = suggestion_count - friendship_suggestion_length
        people_not_in_user_city = Profile.objects.exclude(user__in=friend_list).filter(is_not_user)[
                                  :remaining_suggestion_count]
        friendship_suggestion_query = friendship_suggestion_query | people_not_in_user_city

    # Get a list of users in the same city and same state and not already friend requested
    # If there is less than 5 remove the same city and same state

    return friendship_suggestion_query


def get_mutual_friends(user, target_user):
    """
    Function requires two users, it will return a queryset that contains which
    :param user:
    :param target_user:
    :return:
    """
    user_friend_list = get_friendlist(user)
    target_user_friend_list = get_friendlist(target_user)
    mutual_friends = set(user_friend_list) & set(target_user_friend_list)
    return mutual_friends


def check_friendship_status(user, target_user):
    user_is_requester = Q(requester=user)
    user_is_requestee = Q(requestee=user)
    target_user_is_requester = Q(requester=target_user)
    target_user_is_requestee = Q(requestee=target_user)
    return Friendship.objects.filter(
        (user_is_requester & target_user_is_requestee) | (user_is_requestee & target_user_is_requester))
