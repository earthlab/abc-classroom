# Release Notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
* Update quickstart to use sample config and config functions (@kcranston, #160, #142)

## [0.0.14]
* Fix bug with adding assignments to config (@kcranston, #161)
* Fix feedback bug reported on slack (@kcranston)
* Major update to documentation (@kcranston)

## [0.0.13]
* Add console script for cloning student repos (@kcranston, new functionality)
* Add feedback script to push reports to student repos (@kcranston, new functionality)
* quickstart tests create directories using pytest tmp_path fixture (@kcranston, #151)
* Codacy checks ignore assert statements used in tests (@kcranston, #158)
* Fix abc-init to reflect new location of github auth functions (@kcranston, #163)
* Replace nbgrader with generic course_materials name in config and code (@kcranston, #133)

## [0.0.12]
* Change template functionality so that assignment name provided by user is not modified by abc-classroom (no longer add coursename as prefix) (@kcranston, #137)
* Add each new assignment to an `assignments` section of the config (@kcranston, #138)
* Fix config.yml to ensure ``gitignore`` file has a period at the beginning, update docs (@lwasser, #124)
* Add assignment template functionality (@kcranston, #105)
* Fix RTD build to ensure API reference and other docs build properly (#113, #114, @lwasser)
* Add code of conduct, and md support (m2r) to build (#126, @lwasser)
* Add documentation for `abc-init` (#74, @nkorinek)
* Updated documentation for previous abc-classroom functionality (@kcranston)
* Added command `abc-quickstart` to set up file directory for users(#90, @nkorinek)
* Add a new console script that creates a template repository for an assignment (@kcranston, #79, #73)


## [0.0.11]
* Change tracking started also added basic infrastructure for docs, autodoc, travis-ci testing and sphinx enhancements (@lwasser)
* In this release some docstrings were updated. (@lwasser)

Note that this is the beginning of the change log so issues aren't identified here but will be in the future.
