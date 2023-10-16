from typing import Optional
from typing import Union

import attrs

from tecton.identities import api_keys
from tecton.identities import okta
from tecton_core import conf
from tecton_core import errors
from tecton_core.id_helper import IdHelper


@attrs.frozen
class ServiceAccountProfile:
    id: str
    name: str
    description: str
    created_by: str
    is_active: bool
    obscured_key: str


def set_credentials(tecton_api_key: Optional[str] = None, tecton_url: Optional[str] = None) -> None:
    """Explicitly override tecton credentials settings.

    Typically, Tecton credentials are set in environment variables, but you can
    use this function to set the Tecton API Key and URL during an interactive Python session.

    :param tecton_api_key: Tecton API Key
    :param tecton_url: Tecton API URL
    """
    if tecton_api_key:
        conf.set("TECTON_API_KEY", tecton_api_key)
    if tecton_url:
        conf.validate_api_service_url(tecton_url)
        conf.set("API_SERVICE", tecton_url)


def clear_credentials() -> None:
    """Clears Tecton API key and Tecton URL overrides."""
    for key in ("TECTON_API_KEY", "API_SERVICE"):
        try:
            conf.unset(key)
        except KeyError:
            pass


def test_credentials() -> None:
    """Test credentials and throw an exception if unauthenticated."""
    # First, check if a Tecton URL is configured.
    api_service = conf.get_or_none("API_SERVICE")
    if not api_service:
        msg = "Tecton URL not set. Please configure API_SERVICE or use tecton.set_credentials(tecton_url=<url>)."
        raise errors.TectonAPIInaccessibleError(msg)
    tecton_url = api_service[:-4] if api_service.endswith("/api") else api_service

    # Next, determine how the user is authenticated (Okta or Service Account).
    profile = who_am_i()
    auth_mode = None
    if isinstance(profile, ServiceAccountProfile):
        auth_mode = f"Service Account {profile.id} ({profile.name})"
    elif isinstance(profile, okta.UserProfile):
        auth_mode = f"User Profile {profile.email}"
    else:
        # profile can be None if TECTON_API_KEY is set, but invalid.
        if conf.get_or_none("TECTON_API_KEY"):
            msg = f"Invalid TECTON_API_KEY configured for {tecton_url}. Please update TECTON_API_KEY or use tecton.set_credentials(tecton_api_key=<key>)."
            raise errors.TectonAPIInaccessibleError(msg)
        msg = f"No user profile or service account configured for {tecton_url}. Please configure TECTON_API_KEY or use tecton.set_credentials(tecton_api_key=<key>)."
        raise errors.FailedPreconditionError(msg)

    print(f"Successfully authenticated with {tecton_url} using {auth_mode}.")


def who_am_i() -> Optional[Union[ServiceAccountProfile, okta.UserProfile]]:
    """Introspect the current User or API Key used to authenticate with Tecton.

    Returns:
      The UserProfile or ServiceAccountProfile of the current User or API Key (respectively) if the introspection is
      successful, else None.
    """
    user_profile = okta.get_user_profile()
    if user_profile:
        return user_profile
    else:
        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            try:
                introspect_result = api_keys.introspect(token)
            except PermissionError:
                print("Permissions error when introspecting the Tecton API key")
                return None
            if introspect_result is not None:
                return ServiceAccountProfile(
                    id=IdHelper.to_string(introspect_result.id),
                    name=introspect_result.name,
                    description=introspect_result.description,
                    created_by=introspect_result.created_by,
                    is_active=introspect_result.active,
                    obscured_key=f"****{token[-4:]}",
                )
    return None
