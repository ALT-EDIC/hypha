from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase, override_settings

from ..social_auth_pipeline import grant_oidc_superuser_for_keycloak_group


@override_settings(SOCIAL_AUTH_OIDC_SUPERUSER_GROUP="hypha-admins")
class TestGrantOidcSuperuserForKeycloakGroup(SimpleTestCase):
    def setUp(self):
        self.backend = SimpleNamespace(name="oidc")

    def make_user(self):
        return SimpleNamespace(is_staff=False, is_superuser=False, save=Mock())

    def test_new_user_in_configured_keycloak_group_becomes_superuser(self):
        user = self.make_user()

        grant_oidc_superuser_for_keycloak_group(
            backend=self.backend,
            user=user,
            response={"groups": ["hypha-admins", "other-group"]},
            is_new=True,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        user.save.assert_called_once_with(update_fields=("is_staff", "is_superuser"))

    def test_existing_user_is_not_promoted(self):
        user = self.make_user()

        grant_oidc_superuser_for_keycloak_group(
            backend=self.backend,
            user=user,
            response={"groups": ["hypha-admins"]},
            is_new=False,
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        user.save.assert_not_called()

    def test_other_backend_is_not_promoted(self):
        user = self.make_user()

        grant_oidc_superuser_for_keycloak_group(
            backend=SimpleNamespace(name="google-oauth2"),
            user=user,
            response={"groups": ["hypha-admins"]},
            is_new=True,
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        user.save.assert_not_called()

    def test_nonmatching_group_is_not_promoted(self):
        user = self.make_user()

        grant_oidc_superuser_for_keycloak_group(
            backend=self.backend,
            user=user,
            response={"groups": ["hypha-admin"]},
            is_new=True,
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        user.save.assert_not_called()
