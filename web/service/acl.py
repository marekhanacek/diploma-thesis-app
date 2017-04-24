from dip import settings


def can_user_access_offer(user, offer):
    protected_states = [
        settings.STATUS_DELETED,
        settings.STATUS_AWAITING_APPROVAL,
        settings.STATUS_READY_TO_EXCHANGE,
        settings.STATUS_FINISHED
    ]
    if offer.status.id in protected_states:
        return user.is_authenticated() and offer.is_user_attached(user)
    else:
        return True
