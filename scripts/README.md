In this directory there are a few scripts to help automate the process
of setting up an Open Source Comes to Campus event.

Right now, there is only one -- used for creating repositories for
"Practicing Git" exercises.

Set-up steps: Get Virtualenv
----------------------------

These are only really expected to work on Debian/Ubuntu. Sorry about
that for now.

Make sure you start by doing "cd" to be inside the scripts directory, e.g.:

    $ cd open-source-comes-to-campus/scripts

(but the precise command does depend on where you start out.)

Now, check if you have the 'virtualenv' command. To do that, here we
use the program called "which" that will either print a path to the
virtualenv program, or a "not found" message.

    $ which virtualenv

If you got a "not found" message, run this:

    $ sudo apt-get install python-virtualenv

You'll know you have succeeded because now running which virtualenv
which definitely print a path for you. For example:

    $ which virtualenv
    /usr/bin/virtualenv

Set-up steps: Create virtualenv
-------------------------------

In order to separate this code from other Python code on your system,
run the following command:

    $ virtualenv --system-site-packages .

(The "." character at the end is essential.)

You should expect to see some lines of output starting with:

    New python executable in ./bin/python

and eventually get your prompt back. So far, so good.


Set-up steps: Install the code into your virtualenv
---------------------------------------------------

Run this command:

    $ bin/python setup.py develop

If all went well, you should have a file called bin/setup_practicing_git


Configuring
-----------

To use the app, you must create a GitHub Personal Access Token. This is a magic number,
separate from your password, that identifies you to GitHub. To make one, visit:

https://github.com/settings/applications

Look for the "Personal Access Tokens" section, and click "Create new token."

For the "Token description" type something that will remind you why
you created it, like "Practicing Git app".

Then you will see your token and a button to copy it to the clipboard. Do that,
and then in *this folder*, create a new file called settings.txt with just that
string as its contents.

You can test that your configuration was successful by running:

    $ bin/setup_practicing_git

The first thing that app does is make sure your credentials are valid. It requires
you to answer questions before doing anything possibly dangerous.


Using the app
-------------

The app prompts you and tells you how to use it. Generally, though, when you run it,
you should have the following expectations:

* You will need to create some GitHub organizations by hand.

* The app will create the GitHub repositories, fill them with issues, and fill them with contents.

To run it, execute:

    $ bin/setup_practicing_git
