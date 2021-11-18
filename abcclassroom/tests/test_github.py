# Tests for github script
import sys
import os
import requests
from pathlib import Path
from unittest import mock
import subprocess
import pytest
import github3 as gh3

# TODO:  if we import tests this way we aren't necessarily testing the dev
# version depending upon how abc is installed
import abcclassroom.config as config
import abcclassroom.github as github


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


# TODO: evaluate using mock objects vs creating a mock.mock class object in
#  situ
# Creating an OrganizationObject that will run instead of
# github3.create_repository
class OrganizationObject(object):
    # TODO: Should this have a static decorator on it?
    # @staticmethod
    def create_repository(self, repository):
        if repository == "test_repo":
            return True


# Creating a MockResponse object to be returned when trying to log into github
class MockResponse(object):
    def repository(self, org, repository, token=None):
        if org == "earthlab" and repository == "abc-classroom":
            pass
        elif org == "earthlab" and repository == "test-student":
            pass
        else:
            raise Exception

    def organization(self, org):
        return OrganizationObject()


# Function to return Mock Response for login.
def mock_login(token=None):
    return MockResponse()


# Function to replace check_ssh
def mock_check_ssh():
    """Mock that returns a successful message following what Git returns."""
    # TODO: Lets see how often i use this fixture. would be easy to patch
    # via a mock object too...
    return sys.stdout.write(
        "Hi username! You've successfully authenticated \n"
    )


# TESTS FOR  get_access_token
# TODO: right now the get_github_auth function is in the config module
# it seems like it makes sense for all auth items to be in the same module?
# creating test here for now

# TODO this probably can be replaced with a mock object
def mock_set_token_path(tmp_path):
    """Rather than overwriting a file in the users home, write it to
    tmp_path for testing"""
    return ""


def test_get_access_token(tmp_path, capsys, monkeypatch, create_token):
    """Test that get access token can open file and read key-value
    pairs"""

    # TODO this might become a fixture that returns a token depending on
    # how many times i use this exact set of code lines
    os.chdir(tmp_path)
    create_token
    # Replace expanduser with blank path so it directs to the tmp_path
    monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    # Note - will need to patch _get_authenticated_user
    with mock.patch("abcclassroom.github._get_authenticated_user"):
        # skip actually hitting github with a valid token
        github._get_authenticated_user.return_value = "auser"
        t_auth = github.get_access_token()
    captured = capsys.readouterr().out.splitlines()
    assert (
        captured[0] == "Access token is present and valid; successfully "
        "authenticated as user auser"
    )
    assert t_auth == "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd"


def test_get_access_token_no_user(
    tmp_path, monkeypatch, create_broken_token, capsys
):
    """Test that when a user isn't found, a KeyError is raised"""

    # TODO this might become a fixture that returns a token depending on
    # how many times i use this exact set of code lines
    os.chdir(tmp_path)
    create_broken_token
    # Replace expanduser with blank path so it directs to the tmp_path
    # This avoids us overwriting someone's actual token on their computer
    # while also allowing us to test on CI
    monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    with mock.patch("abcclassroom.github._get_authenticated_user"), mock.patch(
        "abcclassroom.github._get_login_code"
    ), mock.patch("abcclassroom.github._poll_for_status"):

        # Skip hitting github API altogether and just test the workflow
        github._get_authenticated_user.return_value = "auser"
        github._get_login_code.return_value = "clientidhere"
        github._poll_for_status.return_value = "faketokengoeshere"

        a_token = github.get_access_token()

    captured = capsys.readouterr().out.splitlines()
    assert captured[1] == "Successfully authenticated as user auser"
    assert a_token == "faketokengoeshere"


# Test that the get_github_auth returns token information when the file exists
def test_get_github_auth_exists(tmp_path, monkeypatch, create_token):
    """Test that when a valid token file exists, it is correctly returned"""

    os.chdir(tmp_path)
    create_token
    # Replace expanduser with blank path so it directs to the tmp_path
    monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    t_auth = config.get_github_auth()

    assert (
        t_auth["access_token"] == "ac09c4d040ffb190c3eef285eac2faea5b403eb6bd"
    )


def test_get_github_auth_noexist(tmp_path, monkeypatch):
    """Test that when no token file exists, it is returns {}"""

    os.chdir(tmp_path)
    # Replace expanduser with blank path so it directs to the tmp_path
    monkeypatch.setattr(os.path, "expanduser", mock_set_token_path)
    # This doesn't actually raise FileNotFound it just catches the exception
    # and returns {}
    a = config.get_github_auth()
    assert a == {}


# This is the same test as above but using all unittest vs pytest monkeypatch
# def test_get_github_auth_noexist_unittest(tmp_path):
#     """Test that when no token file exists, it is returns {}.
#     this does th e same thing as the test above but it uses mock.patch"""
#
#     os.chdir(tmp_path)
#     # Replace expanduser with blank path so it directs to the tmp_path
#     # TODO above i use monkey patch. It could be that is simpler to read but
#     #  you don't know how it's patched
#     with mock.patch("os.path.expanduser"):
#         # Patch return value for  testing
#         os.path.expanduser.return_value = ""
#         a = config.get_github_auth()
#     assert a == {}


def test_remote_repo_exists_pass(monkeypatch):
    """If the remote repo exists, return True"""
    # Patch gh3.login with mock login function
    monkeypatch.setattr(gh3, "login", mock_login)
    assert github.remote_repo_exists("earthlab", "abc-classroom")


# TODO this test will fail with no token regardless.
def test_remote_repo_exists_fail(monkeypatch):
    """Test that a remote repository that doesn't exist fails."""
    monkeypatch.setattr(gh3, "login", mock_login)
    assert not github.remote_repo_exists("bad_org", "bad_repo")


# NOTE: Updated to run git status so it works universally
# TODO: i am cheating and mocking git status and forcing a return. is this
#  even useful?
def test_call_git_status(capsys):
    """Testing that _call_git helper function works"""
    with mock.patch("abcclassroom.github._call_git"):
        github._call_git.return_value = "On branch"
        ret = github._call_git("status")
        # st_out_txt = capsys.readouterr().out.splitlines()
    assert "On branch" in ret


# TODO: This test assumes a dir called "test_dir" exists and it doesnt exist.
# Is this a space for a fixture / temp dir setup?


@pytest.fixture()
def example_student_repo():
    """A fixture with an example student repo."""
    # TODO can a fixture take a variable like a function can?
    # or should this only create the git dir and let the calling function worry
    # about changing the directory?
    sample_dir = os.path.join("assignment-1", "course-test-student")
    if not os.path.isdir(sample_dir):
        os.makedirs(sample_dir)
    # do we need this to be a git repo? probably would be useful for other
    # tests


# def mock_clone(example_student_repo, a_directory, tmp_path, test):
#     """Takes a repo that has been mock cloned and places it in the intended
#     directory. """
#     # When it's mocking it seems to replace each variable in the function in
#     # a weird unexpected way. - example_student_repo = '-C', a_directory =
#     # 'assignment-1', tmp_path = 'clone', test =
#     # 'git@github.com:earthlab/course-test-student.git'
#
#     # TODO: make this so it's drops the example dir in the dir_path location
#     #tmp_path = "."
#     # Create the rep
#     #a_directory = "test_dir"
#     clone_path = os.path.join(tmp_path, a_directory)
#     print("clone_path is", clone_path)
#     os.chdir(clone_path)
#     # Move repo to location
#     return example_student_repo()

# stackoverflow.com/questions/25692440/mocking-a-subprocess-call-in-python


def test_clone_repo_pass_context_mgr(
    monkeypatch, example_student_repo, capsys
):

    # Fixture for demo student repo in desired repository
    example_student_repo
    # Replace check_github_ssh with a pass - using pytest monkeypatch
    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)

    # Mock the subprocess call using unittest.mock
    with mock.patch("subprocess.run"):
        # Creates a MagickMock() object
        # print(mock_subproc_run)
        github.clone_repo(
            organization="earth55lab", repo="earthpy", dest_dir="assignment-1"
        )
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    # assert captured.out starts with "cloning: git@github"
    # TODO do we also want to create a mock repo for it to check?
    assert lines[1].startswith("Successfully cloned: git@github")


# Here is the SAME TEST as above but using a decorator
# Note that you could use with mock.patch("subprocess.run") as mock_subproc_run
# Below you just create the object with the decorator and define it in the text
# function definition. They test the same thing however.
@mock.patch("subprocess.run")
def test_clone_repo_pass2(
    mock_subproc_run, monkeypatch, example_student_repo, capsys
):
    """Test that a successfully cloned repo returns the expected
    message.
    Using the mock patch decorator here and allowing the returned
    MagickMock object to just be returned so the test will continue
    running as it it were successful"""

    # This fixture will drop an example git
    # repo for us to check that it exists assignment-1/course-test-student"
    # TODO create a mock repo for it to check in the fixture below
    example_student_repo
    # Replace check_github_ssh with a pass (Assume that works - is that ok??)
    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)

    # Subprocess call from _call git will be mocked using the default (empty)
    # MagickMock object
    github.clone_repo(
        organization="earth55lab", repo="earthpy", dest_dir="assignment-1"
    )
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert lines[1].startswith("Successfully cloned: git@github")


# TODO: this will belong above IF we end up using it.
# TODO: could i pass *args or **args here to allow this to just work?
def mock_call_git(git_arg, dest_dir, git_command, url):
    # Here i think i need to mock the expected st error and stout output??
    # This right now isn't working like i think it should but i can revisit
    # this later.
    sys.stderr.write("Some git error here - test this")
    raise RuntimeError()


def test_clone_repo_bad_repo(monkeypatch, example_student_repo, capsys):
    """Test what happens when you clone into a directory that hasn't been
    created yet. This should return a RuntimeError"""

    # This fixture will drop an example git
    # repo for us to check that it exists assignment-1/course-test-student"

    example_student_repo
    # Replace check_github_ssh with a pass
    # TODO: Question - here i'm using monkeypatch below i'm using mock. is that
    #  ok?
    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)
    monkeypatch.setattr(github, "_call_git", mock_call_git)
    # If i keep match = "" (empty) it passes but clearly there is output

    # Testing match output from mock call git
    with pytest.raises(RuntimeError, match=""):
        github.clone_repo(
            organization="earthlab",
            repo="eardthpy",
            dest_dir="assignment-1",
        )

    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    # Testing expected stout from clone_repo
    assert lines[1].startswith("Oops, something")


# TODO: play with writing to std error and out and make sure our functions are
# returning both when needed.

# TODO: tests to add:
# Test what happens when you clone and the dir already exists
# What happens when you clone and the directory you try to clone into
# doesn't exist
# Test that clone returned a git repo in the correct location?? <is that
# contrived if this is mocked?>


def test_clone_repo_bad_repo_unittest(
    monkeypatch, example_student_repo, capsys
):
    """Test what happens when you clone into a directory that hasn't been
    created yet. This is the same as the test above ubt using mock in a
    context manager. i think that is a bit more specific / easy to read vs
    the decorators.

    This should return a RuntimeError"""

    example_student_repo

    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)
    # This works and is also raising sterr correctly! so this is all promising

    with pytest.raises(RuntimeError):
        with mock.patch(
            github._call_git, side_effect=mock_call_git("1", "2", "2", "4")
        ):
            github.clone_repo(
                organization="earthlab",
                repo="eardthpy",
                dest_dir="assignment-1",
            )
    # TODO: delete this - but it just shows you that std error is writing out
    #  correctly from my mock function that patches _call_git
    captured = capsys.readouterr()
    print(captured)


# CLONE: test what happens when you clone and the remote doesn't exist


# These are tests in the main branch now
# i think i mistakenly thought these were from the old abc classroom they
# are more likely from karen!


def test_init_and_commit(default_config, tmp_path):
    """
    Tests that we can create a directory, initialize it as a git repo,
    and commit some changes.
    """
    repo_dir = Path(tmp_path, "init-and-commit")
    repo_dir.mkdir()
    a_file = Path(repo_dir, "testfile.txt")
    a_file.write_text("Some text")
    github.init_and_commit(repo_dir)
    assert Path(repo_dir, ".git").exists()
    git_return = github._call_git("log", directory=repo_dir)
    assert git_return.stdout.startswith("commit")


def test_master_branch_to_main_repeatedly(tmp_path):
    """
    Tests that we can sucessfully change the default master branch to
    main, and nothing bad happends if we try and do it again
    """
    repo_dir = Path(tmp_path, "change-master")
    repo_dir.mkdir()
    github.git_init(repo_dir)

    # change the default branch name
    github._master_branch_to_main(repo_dir)
    # in order to test that main exists, we need to add some commits
    a_file = Path(repo_dir, "testfile.txt")
    a_file.write_text("Some text")
    commit_msg = "commit some things"
    github.commit_all_changes(repo_dir, msg=commit_msg)

    # now test the existance of main
    github._call_git(
        "show-ref",
        "--quiet",
        "--verify",
        "refs/heads/main",
        directory=repo_dir,
    )

    # trying again should also work without error
    github._master_branch_to_main(repo_dir)


def test_master_branch_to_main_no_commits(tmp_path):
    """
    Tests that changing the name of the master branch in a initialized
    repo without commits works.
    """
    repo_dir = Path(tmp_path, "change-master-no-commits")
    repo_dir.mkdir()
    github.git_init(repo_dir)
    github._master_branch_to_main(repo_dir)


# TODO: add an  actual check here for the standard out
def test_check_git_ssh_pass():
    """When ssh is setup correctly, the check should run and pass with no
    output."""
    with mock.patch("subprocess.run"):
        # Skip actually running the subprocess call and return the expected
        # output
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Hi username"
        )
        # Here this should just run and pass
        # I don't think we need an assert unless we add a message for
        # successful check to the function. then we get a return output
        github.check_git_ssh()


def test_check_git_ssh_warning(capsys):
    """Test what happens when ssh is setup but user hasn't logged in"""
    with mock.patch("subprocess.run"):
        # Skip actually running the subprocess call and return the expected
        # output
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Warning: Permanently"
        )
        # Here this should just run and pass
        # I don't think we need an assert unless we add a message for
        # successful check to the function. then we get a return output
        github.check_git_ssh()
        captured_output = capsys.readouterr().out.splitlines()
        assert captured_output[0].startswith("Warning:")


def test_check_git_ssh_error(capsys):
    """Test what happens when ssh is not setup - should raise RuntimeError"""
    with mock.patch("subprocess.run"):
        # Skip running subprocess call, return the expected error
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Encountered this error"
        )
        with pytest.raises(RuntimeError):
            github.check_git_ssh()
        captured_output = capsys.readouterr().out.splitlines()
        assert captured_output[0].startswith("Encountered this error")


#
# def mock_check_ssh_fail():
#     open("ssh.txt")
#     return None


# TODO this test is not working. i can't seem to force trigger a file not found
# it always seems to raise a runtime error. i may not understand how that part
# works. This test currently doesn't work
# def test_check_git_ssh_file_not_found(capsys):
#     """Test what happens when ssh is not setup - should raise
#     FileNotFoundError"""
#     with mock.patch('subprocess.run') as mock_requests:
#         mock_requests.run.side_effect = FileNotFoundError
#         # Skip running subprocess call, return the expected error
#         #subprocess.run.return_value = mock_check_ssh_fail()
#         with pytest.raises(FileNotFoundError):
#             github.check_git_ssh()
#         captured_output = capsys.readouterr().out.splitlines()
#         assert captured_output[0].startswith("[Errno 2] No")


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


def test_get_auth_user(mock_auth_return):
    """Test that when authentication goes as planned, the username is
    returned"""
    with mock.patch("abcclassroom.github.get_request") as mock_get_request:
        mock_get_request.return_value = mock_auth_return

        user = github._get_authenticated_user("fake_token")
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
    with mock.patch("abcclassroom.github.get_request") as mock_get_request:
        mock_get_request.return_value = mock_auth_return
        # This has a broken dictionary but the code just has it fail quietly
        github._get_authenticated_user("fake_token")


# TODO pay attention here as i may have this and be able to use this above?
# Consider how to organize some of these tests. Maybe we have a file for all
# things authentication?
@pytest.fixture
def mock_login_200():
    """A fixture that recreates the response for a login to gh."""
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


def test_get_login_code(mock_login_200, capsys):
    """Tests that a login code can be properly processed and provides the
    user with the expected prompts"""

    with mock.patch("requests.post"), mock.patch(
        "builtins.input", return_value="DUDE"
    ):
        requests.post.return_value = mock_login_200
        github._get_login_code("client-id-here")
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
        github._get_login_code("client-id-here")
    captured_output = capsys.readouterr().out.splitlines()
    assert captured_output[0].startswith("{'device_code': ")


"""
>>>>>> TESTS BELOW ARE ON FUNCTIONS THAT I THINK ARE DEPRECATED <<<<<
"""
# TODO: https://github.com/earthlab/abc-classroom/issues/361 this function
# isnt' in karen's list of functions to test
# def test_check_student_repo_exists_pass(monkeypatch):
#     """Testing that checking a student repo works"""
#     monkeypatch.setattr(gh3, "login", mock_login)
#     try:
#         github.check_student_repo_exists("earthlab", "test", "student")
#         assert True
#     except RuntimeError:
#         assert False


# TODO: similar to above - this isn't in the list of functions to test.
# This function used to be called in MAIN but is now commented out
# SO i think we should drop these tests
#
# def test_check_student_repo_fail(monkeypatch):
#     """A student repo that doesn't exist should fail"""
#     monkeypatch.setattr(gh3, "login", mock_login)
#     # TODO if we use github3 there is a speciicaly Not FoundError exception
#     #  that should be captures here
#     with pytest.raises(Exception):
#         github.check_student_repo_exists("earthlab", "not", "student")
