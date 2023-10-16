.. _quickstart:

Quickstart
==========

Why SpiX?
---------

With SpiX, the compilation process of a ``.tex`` file (Is it compiled using latex? pdflatex? xelatex? lualatex? Should I process its bibliography? with bibtex or biber? Is there an index?) is written in the ``.tex`` file itself, in a human-readable format (a shell script). That way [#why]_:

- when you want to compile two years later, you don't have to guess the compilation process;
- you can send the ``.tex`` file to someone, and that's it: no need to send detailed instructions or a Makefile along with it (everything is in the ``.tex`` file);
- the compilation process is human readable: it can be understood by anyone who is able to read a very basic shell script. In particular, one can read it even if she does not know SpiX.

The ``.tex`` file
-----------------

Write the compilation process of your ``.tex`` file as a shell script, before the preamble, as lines starting with ``%$``:

.. code-block:: latex

   % Compile this file twice with lualatex.
   %$ lualatex foo.tex
   %$ lualatex foo.tex

   \documentclass{article}
   \begin{document}
   Hello, world!
   \end{document}

You can also replace the file name with ``$texname`` (and ``$basename``, without the extension).
That way, you don't have to worry about the file name when writing your commands.

.. code-block:: latex

   % Compile this file twice with lualatex.
   %$ lualatex $texname
   %$ lualatex $texname

Compilation
-----------

To compile the ``.tex`` file, run SpiX:

.. code-block:: shell

   spix foo.tex

Spix will parse the ``.tex`` file, looking for shell snippets (lines before the preamble starting with ``%$``), and run them.

That's all!

.. rubric:: Footnotes

.. [#why] A more detailed answer to *"Why SpiX?"* can be found in :ref:`why`.
