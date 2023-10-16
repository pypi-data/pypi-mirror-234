.. _usage:

Usage
=====

.. contents::
   :local:
   :depth: 1

Configuration
-------------

To configure how your ``.tex`` file is compiled, simply write the necessary commands *before* your preamble, preceded with ``%$``. That's all:

.. code-block:: latex

   % Compile this file using latex+dvipdf:
   %
   %$ latex foo.tex
   %$ dvipdf foo.dvi

   \documentclass{article}
   \begin{document}
   Hello, world!
   \end{document}

Now, when calling SpiX on this file, commands ``latex foo.tex`` and ``dvipdf foo.dvi`` are called:

.. code-block:: shell

   spix foo.tex

.. note::

   * The lines that are interpreted as snippets by SpiX must begin exactly with the two characters ``%$`` followed by a space. Any other prefix is not considered a command:

   .. code-block:: latex

      %$ A command
      % $ Ignored
      %$Ignored
       %$ Ignored
      $% Ignored

   * Any snippet defined *after* the beginning of the preamble is ignored. SpiX does not parse LaTeX code, so it considers any line that is not empty, or does not begin with ``%`` (maybe preceded by spaces) as a preamble.

   .. code-block:: latex

      %$ A snippet
      \documentclass{article}
      %$ Ignored
      \begin{document}
      %$ Ignored
      \end{document}
      %$ Ignored

.. note::

   There is no configuration file.
   SpiX is meant to run the same way on any machine:
   you set up configuration in a ``.tex`` file, you send this file to your friend,
   she runs SpiX on it, and it runs exactly the same way
   (not relying on a configuration file located somewhere in your home directory,
   that you forgot to send along the ``.tex`` file).

Allowed commands
----------------

The code snippets defined in SpiX are interpreted by the ``sh`` shell [#sh]_ (but try to stick to valid ``sh`` code, to make your snippet portable). This means that variables and control structures are allowed.

.. code-block:: latex

   %$ dviname=$basename.dvi
   %$ latex $texname
   %$ bibtex $basename
   %$ for i in $(seq 3)
   %$ do
   %$     latex $basename
   %$ endfor
   %$ dvipdf $dviname

Consecutive lines starting with ``%$`` are interpreted by one single shell call.

.. code-block:: latex

   %$ myvariable=foo
   %$ # This would display "foo"
   %$ echo $myvariable
   % This line does not start with "%$", starting another shell.
   %$ # This would display nothing, since "$myvariable" has been defined in another shell.
   %$ echo $myvariable

Environment variables
---------------------

In order to be readable by a person who has never heard about SpiX,
the snippets are run as-is (interpreted by the ``sh`` shell).

A few environment variables are introduced
(this allows snippets to be independent on file name).
For instance, suppose Donald is writing his next book, in `~/taocp/vol7.tex`:

- ``$texname`` is the file name (without directory): ``vol7.tex``;
- ``$basename`` is the file name, without extension: ``vol7``.

For instance, if file ``foo.tex`` contains the following snippet:

.. code-block:: latex

   %$ latex $texname
   %$ dvipdf $basename

When calling SpiX, commands ``latex foo.tex`` and ``dvipdf foo`` are run.

About errors
------------

SpiX will stop compilation when a code snippets fails (returns an error code different from 0).

To change this behavior, see :ref:`stoponerror` or :ref:`ignoreerrors`.

Command line arguments
----------------------

Since there is no option to configure how compilation is performed (everything is *in* the ``.tex`` file),
the binary has very few options.

.. argparse::
   :module: spix
   :func: commandline_parser
   :prog: spix

Warning
-------

SpiX is dumb: it does not control what is run, it does not check that it is safe to run.
It runs what it is told to run. For instance:

- it does not prevent malicious commands:

  .. code-block:: latex

     %$ rm -fr /

- it does not prevent infinite loops:

  .. code-block:: latex

     %$ spix $texname

- it does not prevent fork bombs:

  .. code-block:: latex

     %$ spix $texname & spix $texname &

Basically, calling SpiX is like running a shell script:
do not call SpiX on an untrusted ``.tex`` file.

.. rubric:: Footnotes

.. [#sh] Which default to ``dash`` on Debian, for instance.
