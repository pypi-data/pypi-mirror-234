.. _install:

Download and Install
====================

* If applicable, the easiest way to get `SpiX` working is by using your distribution package manager. With Debian (and Ubuntu, and surely other distributions that inherit from Debian), it is in package `texlive-extra-utils <https://packages.debian.org/search?keywords=texlive-extra-utils>`__ (since version 2020.20210202-3)::

    sudo apt install texlive-extra-utils

* If `spix` is not packaged (yet) for your operating system, the next preferred installation method uses `pip <https://pip.pypa.io>`_ (preferably in a `virtualenv <https://docs.python-guide.org/dev/virtualenvs/>`_)::

    python3 -m pip install spix

* Or you can install it from sources:

  * download the `stable <https://pypi.python.org/pypi/spix>`_ or `development <https://framagit.org/spalax/spix/-/archive/main/spix-main.zip>`_ version;
  * unpack it;
  * install it (in a `virtualenv <https://docs.python-guide.org/dev/virtualenvs/>`_, if you do not want to mess with your distribution installation system)::

        python3 -m pip install .

* To install it from `CTAN <https://ctan.org/>`__:

  * `download <https://ctan.org/pkg/spix>`__ the package from CTAN;
  * extract the ``spix.py`` file, and copy it somewhere in your ``PATH``.
    On GNU/Linux (and MacOS?), you can rename it to ``spix``.

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/spix-<VERSION>_all.deb
