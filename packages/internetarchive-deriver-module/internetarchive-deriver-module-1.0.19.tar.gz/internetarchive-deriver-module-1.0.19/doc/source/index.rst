.. Internet Archive Deriver Module documentation master file, created by
   sphinx-quickstart on Fri Jan 15 17:06:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Internet Archive Deriver Module's documentation!
===========================================================

Introduction
------------

You have landed on the documentation for the Internet Archive's
``derivermodule``. This is a module used internally to ease the creation of new
so called "deriver modules" in Python. Deriver modules are pieces of code that
operate on uploaded files, creating "derivative" formats (for example, if one
uploads a ``flac`` audio file, a derivative ``opus`` file could be created to
allow for quicker downloads of a lossy variant of the audio.


Concept: the container environment
----------------------------------

All deriver modules based on the ``derivermodule`` (this) library currently run
in a Docker container.

The contain environment has the following paths and files set up::

    /item/
          <identifier>_meta.xml
          <identifier>_files.xml
          <other item files>
    /task/
          task.json                 (task arguments, source/target files)
          petabox.json              (petabox config)
    /tmp                            (disk backed)
    /var/tmp/fast                   (ram backed tmpfs)


The ``Dockerfile`` defines the starting point of the container (``CMD``), and if
a non-zero exit code is returned, the derive task fails.

task.json
~~~~~~~~~

Overview of keys:

* ``identifier``: identifier of the item (``str``)
* ``sourceFile``: absolute path to the source file for the derive (``str``)
* ``sourceFormat``: format of source file (``str``)
* ``targetFile``: absolute path to the target file for the derive (``str``)
* ``targetFormat``: format of the target file (``str``)
* ``task``: dictionary with task information, containing at least ``args`` as a
  key to access task arguments.
* ``?``


petabox.json
~~~~~~~~~~~~

Useful keys:

* ``statsd-server``: address of the statsd server (``str``)
* ``statsd-port``: port of the statsd server (``str``?)
* ``?``


Quickstart
----------

The subsections below will get you started with a simple module.

Also check out the "Example deriver module" for a simple deriver module that
uses most of the functionality exposed by this library, see `modules using
derivermodule`_ for more examples, and for more (non python specific)
documentation, see https://git.archive.org/www/serverless


Build your module with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the root directory of your project, run these steps:

1. Create a Dockerfile, for example::

		cat > Dockerfile
		FROM alpine:3.13

		RUN apk add py3-pip

		RUN apk add libxml2-utils # for xmllint tool

		RUN mkdir -p app
		WORKDIR /app

		RUN apk add py3-lxml py3-xmltodict
		RUN pip3 install internetarchive-deriver-module

		ADD main.py /app

		CMD python3 main.py

2. Create ``main.py``, the starting point of your module

3. Build the container (pick a name other than ``example_container``)::

       sudo docker build -t example-container .

Running your module with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, create a directory to store the test-items that you would like to test
with. It is important that you do not store all the items in the directory of
your docker module, because docker reads **all** files in the directory of your
project when building a module (it won't necessarily include them in the final
artifact), so having lots of large files around slows down build times.

For each item that you would like to test your module on, you will have to
create a ``task`` and ``item`` directory. The ``task`` directory has to
contain the ``task.json`` and ``petabox.json`` files, and the ``item``
directory has to contain all the (relevant) item files (at least
``<identifier>_meta.xml``, ``<identifier>_files.xml``, and your ``sourceFile``
and ``targetFile``).

Step by step, from the root directory of your project:

1. ``mkdir -p ../test-items/my_identifier/{task,item}``

2. Place ``my_identifier_meta.xml`` and any other requires files in
   ``../items/my_identifier/item``.

3. Create ``../test-items/my_identifier/task/task.json`` with something like this::

	   cat > ../test-items/my_identifier/task/task.json
	   {
		  "identifier" : "my_identifier",
		  "sourceFile" : "/item/my_identifier_chocr.html.gz",
		  "sourceFormat" : "Character hOCR GZ",
		  "targetFile" : "/item/my_identifier_hocr.html.gz",
		  "targetFormat" : "hOCR GZ",
		  "task" : {
			 "args" : {}
		  }
	   }

4. Run the container (make sure to swap out ``example-container`` for the name
   you picked)::

	sudo docker run -v `pwd`/../test-items/my_identifier/task:/task -v `pwd`/../test-items/my_identifier/item:/item -i -t example-container

5. Wait for the module to finish.


If you need to make changes, you usually have to rebuild your module. You can
map (override) specific files from your directory with arguments like this to
``docker run``::

    -v `pwd`/main.py:/app/main.py

This will map your new ``main.py`` to the containers ``/app/main.py``.


Deployment
----------

Create a repository on `git.archive.org`, under the right namespace (reach out
to the Petabox team to figure out what it is, it might be `www/`). Then pick
names for your testing and production branches. A recommendation could be
`testing` and `production`: meaning that only commits pushed to any of those two
branches have a chance of being picked up by the production environment (and
thus, pushing to `master` does not trigger a deploy). Then communicate those
branch names to the petabox team.

The `testing` branch can then be selected for a derive by passing the
`test_serverless` argument with the value `on` to the task arguments.
`production` will then be the default branch.


General Deriver Module Guidelines
---------------------------------

When writing a deriver module, it's important to keep the following things in
mind:

* Ensure that your module returns a non-zero exit code upon fatal errors. This
  is done with ``sys.exit(<any positive non-zero number>)``, or when a
  python exception is raised and not caught. Doing so will cause the derive to
  'red row', marking the process as "needs administration attention", which in
  turn allows for you or someone else to find the problem and analyse it.
* When starting out, it's better to hard-fail rather than silently ignore
  errors, and deal with any potential red-rows later on.
* When failing, try to make one of the last lines of your program be clear and
  unique, so that the red row analyser can find and classify your red rows:

  * Don't::

    >>> print('Something went wrong! :-('); sys.exit(1)

  * Do::

    >>> print('FATAL: Invalid wibble marker for this wobble, exiting'); sys.exit(1)
* Version your module, and increase the module version when it makes sense.
  Log the version to the task log at least; also consider writing the module
  version to the file metadata of the file(s) you create (e.g. to the ``targetFile``)
  You can also write the module version information to the item metadata, but
  consult with the collections team before doing so.
* Consider if your module should support task arguments (see
  ``derivermodule.task.get_task_arg_or_environ_arg``).


Source code
-----------

The source code for the module can be found here::

    https://git.archive.org/merlijn/python-derivermodule

Modules using derivermodule
---------------------------

The following projects make use of this library:

* https://git.archive.org/www/tesseract
* https://git.archive.org/www/pdf
* https://git.archive.org/www/microfilm-issue-generator
* https://git.archive.org/www/hocr-char-to-word
* https://git.archive.org/www/hocr-fts-text
* https://git.archive.org/www/hocr-pageindex

Components
----------

.. toctree::
   :maxdepth: 2

   helloworld.rst
   const.rst
   logger.rst
   metadata.rst
   task.rst
   files.rst
   imagestack.rst
   scandata.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
