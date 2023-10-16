.. _plugin_logging:

Logging plugins
===============

.. warning::

   The logging plugins are not the first ones to be loaded. So other plugins might have logged things using the Python :mod:`logging` module when those plugins start handling logs.

Those plugins define how log is displayed. To select a logger (i.e. a plugin logger), use the configuration file:

.. code-block:: ini
   :caption: Enable the `logging.foo` plugin.

   [logging]
   logger = foo

In the above example, plugin ``logging.foo`` is used as the logging plugin (if this option is not set, ``logging.auto`` is used by default).

``logging.quiet`` — Does not log anything
-----------------------------------------

Note that things logged *before* this plugin is enabled are still logged using the default Python module.

``logging.stdlib`` — Use the Python :mod:`logging` module
---------------------------------------------------------

Default logger, that uses the :mod:`logging` Python module.
The format string can be set in the configuration file:

.. code-block:: ini
   :caption: Define format string

   [logging.stdlib]
   format = %%(asctime)s XXX %%(message)s

You can use the attribute names `defined by the logging module <https://docs.python.org/3/library/logging.html#logrecord-attributes>`__. Note that you need to escape ``%`` with double ``%``, because :mod:`configparser` formats strings found in configuration files.


``logging.auto`` — Automatic plugin selection
---------------------------------------------

If standard output is a tty, use the ``logging.rich`` plugin.
Otherwise, log without frills using the ``logging.stdlib`` plugin.

``logging.rich`` — Logging with colors and progress bar
-------------------------------------------------------

Log stuff using colors and a progress bar (uses the :mod:`rich` module).
