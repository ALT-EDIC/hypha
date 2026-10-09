from django.conf import settings


def grant_superuser_privileges(
    backend, user=None, response=None, is_new=False, **kwargs
):
    """Grant full admin access to new OIDC users.

    IdP must return the groups claim from its UserInfo endpoint. This
    deliberately does not update existing accounts or users from other backends.
    """
    if not settings.SOCIAL_AUTH_OIDC_SUPERUSER_GROUP or getattr(backend, "name", None) != "oidc" or not is_new or user is None:
        return

    groups = (response or {}).get("groups", ())
    if isinstance(groups, str):
        groups = (groups,)

    if settings.SOCIAL_AUTH_OIDC_SUPERUSER_GROUP not in groups:
        return

    user.is_staff = True
    user.is_superuser = True
    user.save(update_fields=("is_staff", "is_superuser"))
