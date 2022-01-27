# Tests for github script

import os
from unittest import mock
import requests
from ruamel.yaml import YAML
import pytest


# TODO:  if we import tests this way we aren't necessarily testing the dev
# version depending upon how abc is installed
import abcclassroom.auth as auth


# Fixtures
@pytest.fixture()
def create_token(tmp_path):
    """Create a token file for testing"""
    # Write file to the "home" dir
    the_path = os.path.join(tmp_path, ".abc-classroom.tokens.yml")
    with open(the_path, "w") as token_file:
        # token_file = open(the_path, "w")
        token_text_list = [
            "github:\n",
            "  access_token: ac09c4d040ffb190c3eef285eac2faea5b403eb6bd",
        ]
        token_file.writelines(token_text_list)


@pytest.fixture()
def create_broken_token(tmp_path):
    """Create a token file for testing"""
    # Write file to the "home" dir
    the_path = os.path.join(tmp_path, ".abc-classroom.tokens.yml")
    with open(the_path, "w") as token_file:
        # token_file = open(the_path, "w")
        token_text_list = [
            "github:\n",
            "  party_ppl_access_token: "
            "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd",
        ]
        token_file.writelines(token_text_list)


@pytest.fixture
def mock_auth_return():
    """this is the faked return from the github API when you get a users
    information"""
    status = 200
    body = {
        "login": "test-user",
        "id": 123456,
        "node_id": "randomestring=2",
        "avatar_url": "https://avatars.githubusercontent.com/u/123456?v=4",
        "gravatar_id": "",
    }
    return status, body


@pytest.fixture
def mock_login_200():
    """A fixture that recreates the response for a login to the GitHub API."""
    # Recreate the requests response
    r = requests.Response()
    r.status_code = 200
    fake_data = {
        "device_code": "somebigstringonumbers234560be8d6744c088",
        "user_code": "D123-D456",
        "verification_uri": "https://github.com/login/device",
        "expires_in": 899,
        "interval": 5,
    }

    # The object in the requests response containing the json response is a
    # method so recreate the method here and return the data as expected.
    def json_func():
        return fake_data

    r.json = json_func
    return r


# TODO - this fixture is actually the same as teh one above but with different
# data. i wonder if i can create a fixture from a function that processes the
# varying json output
@pytest.fixture()
def mock_token_200():
    """A fixture that recreates the response for a login to the GitHub API."""
    # Recreate the requests response
    r = requests.Response()
    r.status_code = 200
    fake_token_return = {
        "access_token": "some_fake_token_data_123",
        "token_type": "bearer",
        "scope": "",
    }

    # The object in the requests response containing the json response is a
    # method so recreate the method here and return the data as expected.
    def json_func():
        return fake_token_return

    r.json = json_func
    return r


# Test that the get_github_auth returns token information when the file exists
def test_get_github_auth_exists(tmp_path, monkeypatch, create_token):
    """Test that when a valid token file exists, it is correctly returned"""

    os.chdir(tmp_path)
    create_token
    # Replace expanduser with blank path so it directs to the tmp_path
    # NOTICE the redundancy of patching os.expanduser over and over in this
    # suite
    # monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    with mock.patch("os.path.expanduser"):
        # TODO - tihs is not doing what i think it's doing - revisit this test
        os.path.expanduser.return_value = ""
        t_auth = auth.get_github_auth()

    assert (
        t_auth["access_token"] == "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd"
    )


def test_get_github_auth_noexist(tmp_path, monkeypatch):
    """Test that when no token file exists, it is returns {}"""

    os.chdir(tmp_path)
    # Replace expanduser with blank path so it directs to the tmp_path
    # monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    with mock.patch("os.path.expanduser"):
        os.path.expanduser.return_value = ""
        # This doesn't raise FileNotFound it just catches the exception
        # and returns {}
        a = auth.get_github_auth()
    assert a == {}


# Test set_github_auth
def test_set_github_auth_no_file(tmp_path):
    """Test that set github auth can write an authentication file as
    expected.

    The auth information that this function expects is the
    return from get_github_auth: {"access_token": access_token}.
    Thus here we mock get_github_auth with the expected return.
    We also mock expanduser again because we don't want to overwrite a
    users token."""

    # os.path.expanduser is being patched differently from how i thought it
    # was behaving. i thought it would just remove the "adding the user" path
    # part of things but actually it is a blank slate ... i'm not sure how some
    # of the other tests are working given this realization so will revisit.

    # Ensure it's writing the file to tmp path not the users home
    os.chdir(tmp_path)
    yaml = YAML()
    with mock.patch("abcclassroom.auth.get_github_auth"), mock.patch(
        "os.path.expanduser"
    ):
        auth.get_github_auth.return_value = {}
        fake_token_value = "fake_token_values123"
        os.path.expanduser.return_value = ""
        auth_info = {"access_token": fake_token_value}
        auth.set_github_auth(auth_info)
    # Is there a file to open and does it contain the token value we wrote
    # to it?
    with open(".abc-classroom.tokens.yml") as f:
        config = yaml.load(f)

    assert config["github"]["access_token"] == fake_token_value


# Test set_github_auth
def test_set_github_auth_token_file_exists(tmp_path, create_token):
    """Test that when a token file exists, it still runs and overwrites the
    token in the file. Here it is assumed
     that we have retrieved token information and will just overwrite it.
    """

    # Ensure it's writing the file to tmp path not the users home
    os.chdir(tmp_path)
    create_token

    yaml = YAML()
    # TODO: SHOULD we test that if the token info is new it overwrites the
    #     existing token? this would require an assert prior to running the
    #     context manager of the create_token fixture as a sanity check.
    #     it's not
    #     actually testing the code rather confirming the test suite is
    #     doing what
    #     we think it's doing
    mock_token_val = "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd"
    # Created by the create_token fixture
    with open(".abc-classroom.tokens.yml") as f:
        config = yaml.load(f)
    assert config["github"]["access_token"] == mock_token_val

    yaml = YAML()
    with mock.patch("os.path.expanduser"):
        os.path.expanduser.return_value = ""
        new_fake_token_value = "fake_token_value234"
        auth_info = {"access_token": new_fake_token_value}
        auth.set_github_auth(auth_info)
    # Is there a file to open and does it contain the token value we wrote
    # to it?
    with open(".abc-classroom.tokens.yml") as f:
        config = yaml.load(f)

    assert config["github"]["access_token"] == new_fake_token_value


# TODO: ok i think i do need to patch around because when there is no token
#  it tries to get one i believe... revisit this later!
def test_get_access_token(tmp_path, capsys, create_token):
    """Test that get access token can open file and read key-value
    pairs

    Here we have to test that 1. if there is a token the file contains a
    token value. 2. the function checks that the token is valid. we can
    patch over that check because we will directly test that function in
    another test so i will patch _get_auth_user and pretend it returns a
    user"""

    # TODO this might become a fixture that returns a token depending on
    # how many times i use this exact set of code lines
    os.chdir(tmp_path)
    create_token
    # Patching around the users home dir to ensure we don't mess with their
    # existing token. We could run this if we assumed a valid token locally
    # and also created on in the home dir on the CI server so it's worth
    # discussing. but we aren't actually testing all that much here i think
    # just that it can read a file and fail gracefully.
    with mock.patch("abcclassroom.auth._get_authenticated_user"), mock.patch(
        "os.path.expanduser"
    ):
        # Skip actually hitting github to confirm a valid token and pretend
        # it is valid
        auth._get_authenticated_user.return_value = "auser"
        os.path.expanduser.return_value = ""
        t_auth = auth.get_access_token()
    captured = capsys.readouterr().out.splitlines()
    assert (
        captured[0] == "Access token is present and valid; successfully "
        "authenticated as user auser"
    )
    assert t_auth == "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd"


def test_get_access_token_no_user(
    tmp_path, create_broken_token, capsys, monkeypatch
):
    """Test that when a user isn't found, a KeyError is raised and caught by
    the function. Thus if this test runs, it is successful but does that
    make it fragile?

    Here we assume that the token is there but is missing a key. We still
    have to patch over _get_auth_user because it runs even if that key is
    bad from what i can tell?"""

    # TODO this might become a fixture that returns a token depending on
    # how many times i use this exact set of code lines
    os.chdir(tmp_path)
    create_broken_token

    # Replace expanduser with blank path so it directs to the tmp_path
    # This avoids us overwriting someone's actual token on their computer
    # while also allowing us to test on CI

    with mock.patch("os.path.expanduser"), mock.patch(
        "abcclassroom.auth._get_authenticated_user"
    ), mock.patch("abcclassroom.auth._get_login_code"), mock.patch(
        "abcclassroom.auth._poll_for_status"
    ):
        os.path.expanduser.return_value = ""
        auth._get_login_code.return_value = "clientidhere"
        auth._poll_for_status.return_value = "faketokengoeshere"
        # Pretend there is a user returned
        auth._get_authenticated_user.return_value = "fakeuser"
        auth.get_access_token()

    captured = capsys.readouterr().out.splitlines()
    assert captured[0].startswith("Generating new access")
    assert captured[1].startswith("Successfully authenticated as user")


def test_get_auth_user(mock_auth_return):
    """Test that when authentication goes as planned, the username is
    returned"""
    # mock get_request as called in the auth module - it lives in utils
    with mock.patch("abcclassroom.auth.get_request") as mock_get_request:
        mock_get_request.return_value = mock_auth_return

        user = auth._get_authenticated_user("fake_token")
        assert user == "test-user"


# THIS Excepts a keyerror but never raises it... need to see how this is used
# in the workflow
def test_get_auth_user_no_username(mock_auth_return):
    """Test that when authentication goes as planned, the username is
    returned"""
    status, body = mock_auth_return
    del body["login"]
    print("body is", body)
    mock_auth_return = (status, body)
    with mock.patch("abcclassroom.auth.get_request") as mock_get_request:
        mock_get_request.return_value = mock_auth_return
        # This has a broken dictionary but the code just has it fail quietly
        auth._get_authenticated_user("fake_token")


def test_get_login_code(mock_login_200, capsys):
    """Tests that a login code can be properly processed and provides the
    user with the expected prompts.

    Here we are preventing requests for actually sending anything to the
    API. Instead we are assuming that transaction was successful and we
    create the expected response."""

    with mock.patch("requests.post"), mock.patch(
        "builtins.input", return_value="DUDE"
    ):
        requests.post.return_value = mock_login_200
        auth._get_login_code("client-id-here")
    captured_output = capsys.readouterr().out.splitlines()
    assert captured_output[0].startswith("To authorize this app,")


def test_get_login_code_not_200(mock_login_200, capsys):
    """Tests that a login code that isn't 200 returns the expected json
    output"""
    # Force a status code that isn't 200
    mock_login_200.status_code = 0
    with mock.patch("requests.post"), mock.patch(
        "builtins.input", return_value="DUDE"
    ):
        requests.post.return_value = mock_login_200
        auth._get_login_code("client-id-here")
    captured_output = capsys.readouterr().out.splitlines()
    assert captured_output[0].startswith("{'device_code': ")


# TODO i'm not sure what to test in terms of breaking this
def test_poll_for_status(tmp_path, mock_token_200):
    """Test that poll for status returns token data returned from github api"""

    # Once again ensure we aren't overwriting the users token file
    os.chdir(tmp_path)
    # This called set_access_token so want to patch expand users too
    # Mock over the call to github
    with mock.patch("requests.post", return_value=mock_token_200), mock.patch(
        "os.path.expanduser", return_value=""
    ):

        token = auth._poll_for_status(
            client_id="idhere", device_code="device_id_here"
        )

        assert token == "some_fake_token_data_123"
