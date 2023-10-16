.. _install:

Download and install
====================

Évariste can be installed using `pip <https://pip.pypa.io>`__:

.. code-block:: shell

  python3 -m pip install evariste

You can build your own Debian (and Ubuntu?) package using `stdeb <https://github.com/astraw/stdeb>`_:

.. code-block:: shell

  python3 setup.py --command-packages=stdeb.command bdist_deb
  sudo dpkg -i deb_dist/evariste-<VERSION>_all.deb
