import os
import sys

from nbclean import NotebookCleaner


def main():
    notebook = sys.argv[1]
    print('Processing', notebook)

    directory, nb_name = os.path.split(notebook)
    base_name, extension = os.path.splitext(nb_name)

    # create test files and notebook for the student
    nb = NotebookCleaner(notebook)
    nb.create_oktests(tag='private',
                      oktest_path=base_name,
                      base_dir='autograder')
    nb.create_oktests(tag='public',
                      oktest_path=base_name,
                      base_dir='student')
    nb.save(os.path.join('student', nb_name))

    # create test files for the autograder
    nb = NotebookCleaner(notebook)
    nb.create_oktests(tag='private',
                      oktest_path=base_name,
                      base_dir='autograder')
    nb.create_oktests(tag='public',
                      oktest_path=base_name,
                      base_dir='autograder')
