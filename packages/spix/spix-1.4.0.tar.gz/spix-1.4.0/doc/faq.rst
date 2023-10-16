.. _faq:

Frequently asked questions
==========================

.. contents::
   :local:

Why won't SpiX accept any option to control compilation?
--------------------------------------------------------

The purpose of SpiX is to have every single piece of information regarding how to compile a ``.tex`` file *inside* the ``.tex`` file itself.
So, SpiX having options to control the compilation would go against this purpose.
That is why the only SpiX options are options
*about* SpiX itself (``--help``, ``--version``),
or *about* the compilation (``--dry-run``),
but nothing that changes *how* the file is to be compiled.

How to re-run SpiX as soon as a file has changed?
-------------------------------------------------

SpiX has no built-in feature to do this,
but you can use external tools, like `entr <https://eradman.com/entrproject/>`__:

.. code-block:: shell

   ls foo.tex | entr spix foo.tex

But if your compilation process includes several passes of LaTeX, and biblatex, and…, you probably don't want to re-run *everything* as soon as you fix a typo in your document. In this case, do not use SpiX at all:

.. code-block:: shell

   ls foo.tex | entr pdflatex foo.tex

Then, when every single typo has been fixed, at last, you can use SpiX to properly compile your document:

.. code-block:: shell

   spix foo.tex

How to run SpiX on several files?
---------------------------------

SpiX accepts exactly one file as an argument.

To run it on several files, you can use `find <https://www.gnu.org/software/findutils/>`__:

.. code-block:: shell

   find . -name '*tex' -exec spix {} \;

or `parallel <https://www.gnu.org/software/parallel/>`__:

.. code-block:: shell

   parallel spix -- *tex

or both:

.. code-block:: shell

   find . -name '*tex' -exec parallel spix -- {} \+

How to check if a ``.tex`` file has any SpiX commands set?
----------------------------------------------------------

Option ``--dry-run`` will print the code snippets to be run by SpiX.
Thus, to test whether any code snippets has been set in a ``.tex`` file,
you can test use:

.. code-block:: shell

   if [ -z "$(spix --dry-run foo.tex)" ]
   then
     echo "No command defined."
   else
     echo "Some commands defined."
   fi

.. _stoponerror:

How to stop compilation on first error?
---------------------------------------

A code snippet defined in your ``.tex`` file is executed,
even if commands inside it fails.
For instance, suppose your file contains the following code snippet.

.. code-block:: latex

   %$ latex $texname
   %$ bibtex $basename
   %$ latex $texname
   %$ latex $texname
   %$ dvipdf $basename

If the first LaTeX compilation fails, the following commands are still executed.
Preventing any further command to be executed is dealt with using the shell options, not SpiX.
You can chain your commands using ``&&``:

.. code-block:: latex

   %$ latex $texname &&\
   %$ bibtex $basename &&\
   %$ latex $texname &&\
   %$ latex $texname &&\
   %$ dvipdf $basename

or use ``set -e``:

.. code-block:: latex

   %$ set -e
   %$ latex $texname
   %$ bibtex $basename
   %$ latex $texname
   %$ latex $texname
   %$ dvipdf $basename

or split you snippet into several snippets
(that way, SpiX will stop after the first code snippet that ends with an error):

.. code-block:: latex

   %$ latex $texname
   %
   %$ bibtex $basename
   %
   %$ latex $texname
   %
   %$ latex $texname
   %
   %$ dvipdf $basename

.. _ignoreerrors:

How to go on compiling, even when errors occur?
-----------------------------------------------

If any code snippets ends with an error (an error code other than 0),
SpiX will stop the compilation. You may want to continue, no matter what.
Once again, this is achieved using the shell, not using SpiX.
You can:

- force the error code at the end of your code snippet:

  .. code-block:: latex

     %$ latex $texname
     %$ exit 0

- Catch errors using ``|| true``:

  .. code-block:: latex

     %$ latex $texname || true
