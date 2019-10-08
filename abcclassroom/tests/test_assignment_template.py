# Tests for assignment-template console script workflow

import pytest
import os
import abcclassroom.template as abctemplate


class TestAssignmentTemplate:

    config = {"template_dir": "test_template", "short_coursename": "tc"}

    # Tests for create_template_dir method
    def test_create_template_dir(self, tmp_path):
        # check that creates directory if does not exist
        self.config["course_directory"] = tmp_path
        template_path = abctemplate.create_template_dir(
            self.config, "test_assignment"
        )
        assert os.path.isdir(template_path)
        assert (
            template_path
            == "{}/test_template/tc-test_assignment-template".format(tmp_path)
        )

    def test_create_template_dir_when_exists(self, tmp_path):
        # test that fails when dir exists (by running method twice)
        self.config["course_directory"] = tmp_path
        with pytest.raises(SystemExit):
            template_path = abctemplate.create_template_dir(
                self.config, "test_assignment"
            )
            template_path = abctemplate.create_template_dir(
                self.config, "test_assignment"
            )

    def test_coursename_config_options(self, tmp_path):
        # test that it fails if neither short_coursename or course_name is set
        localconfig = {
            "template_dir": "test_template",
            "course_directory": tmp_path,
        }
        with pytest.raises(SystemExit):
            template_path = abctemplate.create_template_dir(
                localconfig, "test_assignment"
            )

    # Tests for copy_assignment_files method
    # def test_copy_assigment_files(config, template_repo_name, assignment):

    # Tests for create_extra_files method
    # def test_create_extra_files(config, template_repo_name, assignment):
    #
    # def test_do_local_git_things(template_dir, custom_message):
