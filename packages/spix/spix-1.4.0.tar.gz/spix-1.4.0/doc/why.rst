.. _why:

Why SpiX?
=========

Which problems does SpiX solve?
-------------------------------

The goal of SpiX is to have every information about a ``.tex`` compilation process *inside* the very file to process.

Example 1
"""""""""

Alice is a math teacher.
She writes every document she shows or hands out to her students using LaTeX.
She has a repository consisting of `hundreds of LaTeX files <https://framagit.org/lpaternault/cours-2-math>`_.
Most of her documents are compiled using a single pass of LuaLaTeX,
but some of them need two passes (because labels and references),
some of them contains `pstricks <https://tug.org/PSTricks/>`_ figures that must be compiled with LaTeX,
then converted to PDF
(because she copied them from `another repository that uses LaTeX <https://www.apmep.fr/-Annales-Bac-Brevet-BTS->`_)…

When she works on a file she edited one year ago, with her previous class, she has to guess how to compile it (lualatex? lualatex+lualatex? latex+dvipdf?).

Using SpiX, the compilation process is written *inside* the ``.tex`` file, so she can:

- look at it to see which tool to use to compile it;
- compile it using SpiX.

Example 2
"""""""""

Alice happens to work with Bob, who also uses LaTeX.
The ideal way to work on the same file would be to share a git repository containing a Makefile, but evoking those tools would scare Bob away. So they exchange files via email.
Using SpiX, the compilation process of the file they exchange is written inside the file itself:

.. code-block:: latex

   % Use lualatex twice to compile this file:
   %$ lualatex foo.tex
   %$ lualatex foo.tex

   \documentclass{article}
   \begin{document}
   Hello, world!
   \end{document}

- Alice: The first three lines of this file can be parsed by SpiX, so that Alice simply runs ``spix foo`` to compile it;
- Bob: The first three lines of this file are human-readable, so Bob understands how he should compile it.

Why not using any other tool?
-----------------------------

Makefile
""""""""

If your project is complex (convert images, compile ``.dot`` graphs, several latex passes, bibliography, index…), use a Makefile. You may prefer SpiX if:

- the Makefile would be only two lines long;
- you have tens or hundreds of simple ``.tex`` files, with slighly different compilation processes (which would mean tens or hundreds of Makefiles, or one huge Makefile);
- you want to have the compilation process *inside* the ``.tex`` file itself.

Arara
"""""

I got the idea to write compilation information into the ``.tex`` file itself from `Arara`_.

Arara provides a set of rules to compile files. If something is missing, you can write your own rule in an external file, so you might prefer SpiX if you want *everything* in the same ``.tex`` file.

Arara configuration is written using YAML. So, to understang Arara configuration, one has to know YAML and Arara (while SpiX configuration is plain shell commands, so it is human readable [#human]_).

You might prefer Arara if you have complex rules; SpiX is well suited for plain, simple commands.

TrY
"""

`TrY <https://ctan.org/pkg/try>`_ does exactly what SpiX does (and I copied the syntax of commands in ``.tex`` files from TrY). But it is written in Python2 (which is `obsolete <https://blog.python.org/2020/04/python-2718-last-release-of-python-2.html>`__), and it seems to be `no longer maintained <https://bitbucket.org/ajabutex/try/issues/14/is-this-project-still-maintained>`__.

SpiX can be seen as a successor of TrY [#endorsment]_.

Latexmk
"""""""

`Latexmk <http://personal.psu.edu/jcc8/latexmk/>`_ (and `similar tools <https://www.ctan.org/topic/compilation>`__) has a slightly different purpose.

- It guesses how to compile file (how many passes, etc.), while SpiX commands are explicit (there is *no magic* in SpiX).
- User has to specify which flavor (LaTeX, pdflatex, LuaTeX, XeLaTeX…) to use, while with SpiX, this is stored in the ``.tex`` file.

Why is it named SpiX?
---------------------

`Arara <https://gitlab.com/islandoftex/arara>`_ is named after the `blue-and-yellow macaw <https://en.wikipedia.org/wiki/Blue-and-yellow_macaw>`_ (*arara* meaning *macaw* in Portuguese), which is a big parrot. This project, which happens to be a simpler version of Arara, is named after the `blue winged parrotlet <https://en.wikipedia.org/wiki/Blue-winged_parrotlet>`_ (*toui de Spix* in French), which is a small parrot.

Obviously, the capital `X` is a nod to the capital `X` of LaTeX.

.. figure:: _static/Forpus-xanthopterygius-Entre-Rios-de-Minas.png
   :alt: A blue winged parrotlet.

   A blue winged parrotlet. Photo by `Evaldo Resende - Own work, CC BY-SA 4.0 <https://commons.wikimedia.org/w/index.php?curid=79073013>`_ (flipped, resized, reframed by Louis Paternault).

.. rubric:: Footnotes

.. [#human] At least, readable by anyone who can use a terminal.
.. [#endorsment] Without any endorsment by the original author of TrY.

