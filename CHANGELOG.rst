Release Notes
=============

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[unreleased]
------------
- Rather than opening text editor for commit message, allow user to provide custom message as command line arg; changes name of command line arg to 'commit_message' from 'custom_message' (@kcranston, #466)
- Update documentation to discuss using extra_files to modify gitignore and readme (@lwasser, #178)
- Reorganize the functions for checking, validating, and generating access tokens to make testing easier (@kcranston, #460)
- Remove old unused code from before the big redirection (@kcranston, #449, #465)
- Reoganize github module into smaller chunks (@kcranston, #447)
- Check for working ssh keys before git commands that connect to github (@kcranston, #366)
- Fix bug where git pull method was still trying to use master as the default branch rather than main (@kcranston, #376)
- Use classroom_roster.csv consistently for roster filename (@kcranston, #383)
- abc-clone and abc-feedback use same roster handling and print full path if FileNotFoundError (@kcranston, #384)
- new abc-roster script that creates nbgrader-formatted roster from GitHub Classroom roster (@kcranston, #59)

[0.1.9]
------------
- Default template_repos dir rather than assignment_repos (@lwasser, #327)
- Overhaul fixtures, support moving  different type of files & fix codecov ci (@lwasser, #273, #172)
- Modify how we generate an access token for GitHub API access due to upcoming deprecation of username + password authentication (@kcranston, #328)
- Make new repositories use 'main' instead of 'master' as the default branch (@kcranston, #326)
- Fix manged abc-quickstart success message (@kcranston, #367)
- Refactor the main-to-master branch renaming for better error handling and usability (@kcranston, #363)
- Implement copy_file helper for copying files from one dir to another (@kcranston, #382)
- Check for working ssh keys before git commands that connect to github (@kcranston, #366)
- Fix bug where git pull method was still trying to use master as the default branch rather than main (@kcranston, #376)

[0.1.8]
------------
- Moving to github actions in this release as well (@lwasser)
- Move clone into a stand alone package function (@lwasser, #319)
- Add fixtures to conftest for universal abc setup (@lwasser, #316)
- Fix CI to force mac to build on python 3.8 and fix linux matrix / tox versions (@lwasser, #303)

[0.1.7]
------------
- Update the default config to use ``classroom_roster.csv`` which is the default GH classroom filename (@lwasser, #297)
- Setup windows testing using github actions (@lwasser, #300)
- Add ``scrub`` argument to abc-feedback to clean hidden tests from html (@lwasser, #290, #238)

[0.1.6]
------------
- Add files_to_ignore to skip moving certain files (@lwasser, #172, #278)
- Clone dir copies assignments into an assignment-name dir rather than cloned
  dir root (@lwasser, #276)
- Fix manifest file to bundle example-data not example-files dir (@lwasser, #272 take two)

[0.1.5]
------------
-  Update manifest to bundle ``example-data`` directory (@lwasser, #272)
-  This patch also includes an extensive reorganization of the documentation.
   There is no GitHub issue associated with this effort. (@lwasser)

[0.1.4]
--------

-  Copy / create extra files from an ``extra_files`` directory rather than having
   them specified in config (@kcranston, #195)
-  Changed markdown documents to ``.rst`` to remove ``m2r`` as a dependency
   (@nkorinek, #210)
-  NOTE - there was a package bundling issue in 0.1.0-0.1.3 that was resolved in
   this release

[0.0.15]
--------

-  Check whether local repo has uncommitted changes before trying to
   commit (@kcranston, #182)
-  Update quickstart to use sample config and config functions
   (@kcranston, #160, #142)

[0.0.14]
--------

-  Fix bug with adding assignments to config (@kcranston, #161)
-  Fix feedback bug reported on slack (@kcranston)
-  Major update to documentation (@kcranston)

[0.0.13]
--------

-  Add console script for cloning student repos (@kcranston, new
   functionality)
-  Add feedback script to push reports to student repos (@kcranston, new
   functionality)
-  quickstart tests create directories using pytest tmp_path fixture
   (@kcranston, #151)
-  Codacy checks ignore assert statements used in tests (@kcranston,
   #158)
-  Fix abc-init to reflect new location of github auth functions
   (@kcranston, #163)
-  Replace nbgrader with generic course_materials name in config and
   code (@kcranston, #133)

[0.0.12]
--------

-  Change template functionality so that assignment name provided by
   user is not modified by abc-classroom (no longer add coursename as
   prefix) (@kcranston, #137)
-  Add each new assignment to an ``assignments`` section of the config
   (@kcranston, #138)
-  Fix config.yml to ensure ``gitignore`` file has a period at the
   beginning, update docs (@lwasser, #124)
-  Add assignment template functionality (@kcranston, #105)
-  Fix RTD build to ensure API reference and other docs build properly
   (#113, #114, @lwasser)
-  Add code of conduct, and md support (m2r) to build (#126, @lwasser)
-  Add documentation for ``abc-init`` (#74, @nkorinek)
-  Updated documentation for previous abc-classroom functionality
   (@kcranston)
-  Added command ``abc-quickstart`` to set up file directory for
   users(#90, @nkorinek)
-  Add a new console script that creates a template repository for an
   assignment (@kcranston, #79, #73)

[0.0.11]
--------

-  Change tracking started also added basic infrastructure for docs,
   autodoc, travis-ci testing and sphinx enhancements (@lwasser)
-  In this release some docstrings were updated. (@lwasser)

Note that this is the beginning of the change log so issues aren’t
identified here but will be in the future.
