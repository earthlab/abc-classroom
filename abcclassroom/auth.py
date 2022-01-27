"""
abc-classroom.auth
==================
"""

# Methods for setting up authorization to the GitHub API. See
# github.py for methods that use the API.

import requests
import os.path as op
from ruamel.yaml import YAML

from .utils import get_request


def get_github_auth():
    """
    Check for a YAML file with
    github authentication and load the authentication information.

    Returns
    -------
    ruamel.yaml.comments.CommentedMap
        Yaml object that contains the token and id for a github session.
        If yaml doesn't exists, return an empty dictionary.
    """
    yaml = YAML()
    try:
        with open(
            op.join(op.expanduser("~"), ".abc-classroom.tokens.yml")
        ) as f:
            config = yaml.load(f)
        return config["github"]

    except FileNotFoundError:
        return {}


def set_github_auth(auth_info):
    """
    Set the github authentication information. Put the token and id
    authentication information into a yaml file if it doesn't already exist.

    Parameters
    ----------
    auth_info : dictionary
        The token and id authentication information from github stored in a
        dictionary object.

    Returns
    -------
    Creates a file called .abc-classroom.tokens.yml in the users home dir.
    """
    yaml = YAML()
    config = {}

    # If conf file already exists, open it and get config file
    if get_github_auth():
        with open(
            op.join(op.expanduser("~"), ".abc-classroom.tokens.yml")
        ) as f:
            config = yaml.load(f)

    config["github"] = auth_info

    with open(
        op.join(op.expanduser("~"), ".abc-classroom.tokens.yml"), "w"
    ) as f:
        yaml.dump(config, f)


def get_access_token():
    """Get GitHub API access token stored in a yaml file in users home
    directory.

    # TODO does it actually generate the new token?
    First tries to read from local token file. If token does not exist,
    or is not valid, generates a new token using the OAuth Device Flow.
    https://docs.github.com/en/free-pro-team@latest/developers/apps/
    identifying-and-authorizing-users-for-github-apps#device-flow

    Returns an access token (string).
    """
    # First, check for saved token in the users home directory
    auth_info = get_github_auth()
    if auth_info:
        try:
            access_token = auth_info["access_token"]
            # if so, is it valid?
            user = _get_authenticated_user(access_token)
            if user is not None:
                print(
                    "Access token is present and valid; successfully "
                    "authenticated as user {}".format(user)
                )
                return access_token
        except KeyError:
            pass

    # otherwise, generate a new token
    print("Generating new access token")
    # client id for the abc-classroom-bot GitHub App
    client_id = "Iv1.8df72ad9560c774c"

    # TODO need to handle cases where the device call fails - wrong client_id,
    # the user could ^C or the internet could be out, or some other
    # unanticipated woe)
    device_code = _get_login_code(client_id)
    access_token = _poll_for_status(client_id, device_code)

    # test the new access token
    user = _get_authenticated_user(access_token)
    if user is not None:
        print("""Successfully authenticated as user {}""".format(user))
    return access_token


def _get_authenticated_user(token):
    """Test the validity of an access token.

    Given a github access token, test that it is valid by making an
    API call to get the authenticated user.

    Returns the GitHub username of the authenticated user if token valid,
    otherwise returns None.
    """

    url = "https://api.github.com/user"
    (status, body) = get_request(url, token)
    try:
        user = body["login"]
        return user
    except KeyError:
        return None


def _get_login_code(client_id):
    """Prompts the user to authorize abc-classroom-bot.

    First part of the Device Flow workflow. Asks user to visit a URL and
    enter the provided code. Waits for user to hit RETURN to continue.
    Returns the device code.

    Parameters
    ----------
    client_id : str
        String representing the ID for the abc-classroom bot.
    Returns
    -------
    device_code : str
        The device code for the response.
    """

    # make the device call
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"client_id": client_id}
    link = "https://github.com/login/device/code"
    r = requests.post(link, headers=header, json=payload)

    # process the response
    data = r.json()
    status = r.status_code
    if status != 200:
        # print the response if the call failed
        print(r.json())
        return None

    device_code = data["device_code"]
    uri = data["verification_uri"]
    user_code = data["user_code"]

    # prompt the user to enter the code
    print(
        "To authorize this app, go to {} and enter the code {}".format(
            uri, user_code
        )
    )
    input("\nPress RETURN to continue after inputting the code successfully")

    return device_code


def _poll_for_status(client_id, device_code):
    """Polls API to see if user entered the device code

    This is the second step of the device flow. Returns an access token, and
    also writes the token to a file in the user's home directory.

        Parameters
    ----------
    client_id : str
        A string representing the client code for the abc-classroom bot.
    device_code : str
        The device code returned from the API for the user's machine / device.
    Returns
    -------
    Access token provided by GitHub.
    Writes the token to a file in the user's home directory
    """

    header = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    r = requests.post(
        "https://github.com/login/oauth/access_token",
        headers=header,
        json=payload,
    )

    data = r.json()
    access_token = data["access_token"]
    set_github_auth({"access_token": access_token})
    return access_token
