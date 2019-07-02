FAQ
====

Installation
------------

My install fails because  `error: package directory 'src/find_namespace:' does not exist`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see an issue with the install failing like so:

.. code-block:: bash

    $python3.7 -m pip install git+https://github.com/funkybob/gilbert.git
    Collecting git+https://github.com/funkybob/gilbert.git
    Cloning https://github.com/funkybob/gilbert.git to /tmp/pip-g3bsf2gf-build
        Complete output from command python setup.py egg_info:
        running egg_info
        creating pip-egg-info/gilbert.egg-info
        writing pip-egg-info/gilbert.egg-info/PKG-INFO
        writing dependency_links to pip-egg-info/gilbert.egg-info/dependency_links.txt
        writing entry points to pip-egg-info/gilbert.egg-info/entry_points.txt
        writing requirements to pip-egg-info/gilbert.egg-info/requires.txt
        writing top-level names to pip-egg-info/gilbert.egg-info/top_level.txt
        writing manifest file 'pip-egg-info/gilbert.egg-info/SOURCES.txt'
        error: package directory 'src/find_namespace:' does not exist
        
        ----------------------------------------
    Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-g3bsf2gf-build/

This will be because you have a version of setuptools that is too old, Gilbert requires a version of setuptools `>=41.0.1`

You can fix this by updating versions:

.. code-block:: bash

    pip install -U setuptools
	
How do I have Gilbert automatically rebuild the site when files change?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Have gilbert watch your files, and re-render on changes:

.. code-block:: bash

	$ gilbert --root mysite watch

If you are using Windows you will notice this error:

.. code-block:: powershell

	OSError: [WinError 126] The specified module could not be found

This is because the implementation for "watch" was written only for inotify compatible OSs as a matter of expediency.

However there is a solution for Windows users to use `watchexec <https://github.com/watchexec/watchexec#windows>`_, which is available using `scoop <https://scoop.sh/>`_, or by unzipping the binary from the GitHub Releases.

Using scoop:

.. code-block:: powershell

	scoop install watchexec

Now the command to have gilbert watch your files, and re-render on changes:

.. code-block:: :powershell

	watchexec -i docs gilbert render