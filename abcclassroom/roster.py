"""
abc-classroom.roster
====================

"""

import csv
from pathlib import Path

from . import config as cf


def create_roster(
    input_file, output_file="nbgrader_roster.csv", column_to_split="name"
):
    """Given a roster file downloaded from GitHub Classroom, creates
    a roster file suitable for use with abc-classroom and nbgrader.

    Parameters
    ----------
    input_file : string
        Path to the GitHub Classroom roster
    output_file: string
        Name of the output file. Default is abc_roster.csv
    column_to_split : string
        The column that we want to split to create the new columns
        first_name and last_name. Default is "name".

    """
    # create path to input file
    classroom_roster_path = Path(input_file)

    # get the materials_dir from the config and set the path of the
    # output file
    config = cf.get_config()
    materials_dir = cf.get_config_option(config, "course_materials", False)

    # if the course materials dir does not exist, return
    if not Path(materials_dir).is_dir():
        print(
            "Course materials directory '{}' as specified in config "
            "file does not exist. Please create "
            "it and then re-run abc-roster".format(materials_dir)
        )
        return

    output_file_path = Path(materials_dir, output_file)

    # if the output file exists, return
    if output_file_path.exists():
        print(
            "Output file '{}' already exists. Please delete, rename, "
            "or move this file (or specify a different output file "
            "with the -o or --output flag) "
            "before re-running abc-roster.".format(output_file_path)
        )
        return

    try:
        with open(classroom_roster_path, newline="") as csv_input, open(
            output_file_path, "w", newline=""
        ) as csv_output:
            reader = csv.DictReader(csv_input)
            columns = reader.fieldnames
            columns.append("id")
            columns.append("first_name")
            columns.append("last_name")
            writer = csv.DictWriter(csv_output, fieldnames=columns)
            writer.writeheader()
            for row in reader:
                newrow = row
                ghname = row["github_username"]
                if ghname == "":
                    print("Skipping this row; no GitHub username found:")
                    print(" ", list(row.values()))
                    continue
                row["id"] = ghname
                if column_to_split in row:
                    name = row[column_to_split]
                    # split into two parts based on final space in field
                    # assume first part is first name and second part is
                    # last name
                    twonames = name.rsplit(" ", 1)
                    try:
                        newrow["first_name"] = twonames[0]
                    except IndexError:
                        newrow["first_name"] = ""
                    try:
                        newrow["last_name"] = twonames[1]
                    except IndexError:
                        newrow["last_name"] = ""
                writer.writerow(newrow)

    except FileNotFoundError as err:
        # prints the error [Errno 2] No such file or directory:
        # 'classroom_roster_path'
        print(err)
    except KeyError as ke:
        # prints error Error: Input file does not contain required column
        # 'github_username'
        print(
            "Error: Input file does not contain required column {}".format(ke)
        )
