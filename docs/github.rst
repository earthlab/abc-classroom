
Setting Up A Template Repo
--------------------------

To create a new assignment, you need to

1. Create the assignment within your classroom on GitHub and
2. Create a template repository. This repo contains all of the files that the students will need to complete their homework.

Step two can be implemented with abc-classroom by performing the following steps.


1. Authenticate with GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, you need to authenticate with GitHub. This authentication step will
allow you to automagically create the template repo within your chosen organization.

To authenticate, run:

    $ abc-init

This step will ask you for your GitHub username and password. It will
then create a token on GitHub which will allow you to create a repo.
This token can even be used to create pull requests

?? this could be used to return student feedback to them but let's see what we already have in this area??

You can view the token by going to https://github.com/settings/tokens
The token will be called `Grading workflow helper`

::::

