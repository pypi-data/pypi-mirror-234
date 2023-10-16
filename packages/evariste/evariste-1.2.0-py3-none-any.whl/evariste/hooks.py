# Copyright Louis Paternault 2015-2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Implement hook mechanism.

See :ref:`hooks` for more information.

.. note::

   This implementation of hooks rely on other parts of Évariste
   (:mod:`~evariste.plugins` for example),
   and cannot be used separatedly.

Example
-------

.. code-block:: python
   :caption: Example of hook mechanism

   import contextlib

   from evariste import hooks

   class A:

       @hooks.setmethodhook()
       def a(self):
           print("Running A.a()…")

   class B:

       @hooks.contexthook("A.a"):
       @contextlib.contextmanager
       def b(self):
           print("Before running A.a()…").
           yield
           print("After running A.a()…").

   # Let's go!
   A.a()

In this example, the ``A.a()`` method has been marked as accepting hooks,
and the ``B.b()`` method has been registered as a hook for ``A.a()``.

When ``A.a()`` is run (last line of the example),
although ``B`` has not been called directly,
``B.b()`` is called as well, as a registered hook. The output of this example is::

    Before running A.a()…
    Running A.a()…
    After running A.a()…

Get functions registered as hooks
---------------------------------

Method hooks
------------

Methods can be marked to accept hooks using the following function.

.. autofunction:: setmethodhook

Context hooks
-------------

Context hooks cannot be directly defined: every method hook is also a context hook.

Iteration hooks
---------------

Iteration hooks can be executed using :meth:`~evariste.plugins.Loader.applyiterhook`.

Register functions as hooks
---------------------------

.. autofunction:: hook

.. autofunction:: contexthook

.. autofunction:: methodhook

.. autofunction:: iterhook

"""

import collections
import functools
import typing


def hook(hooktype: str, name: str) -> typing.Callable:
    """Decorator to register a function or method as a hook.

    :param str hooktype:
        Type of hook (``"methodhook"`` or ``"contexthook"``, or whatever string you want).
    :param str name:
        Name of the target hook, of the form ``Class.methodname``
        (or ``Class`` only for the ``__init__`` method).
    """

    def wrapper(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            return function(*args, **kwargs)

        hooked = getattr(function, "hooked", collections.defaultdict(set))
        hooked[hooktype].add(name)
        setattr(wrapped, "hooked", hooked)
        return wrapped

    return wrapper


def methodhook(name: str) -> typing.Callable:
    """Decorator to register a function or method as a method hook.

    For any string ``name``, ``methodhook(name)`` is a shortcut for ``hook("methodhook", name)``.
    """
    return hook("methodhook", name)


def contexthook(name: str) -> typing.Callable:
    """Decorator to register a function or method as a context hook.

    For any string ``name``, ``contexthook(name)`` is a shortcut for ``hook("contexthook", name)``.
    """
    return hook("contexthook", name)


def iterhook(name: str) -> typing.Callable:
    """Decorator to register a function or method as an iter hook.

    For any string ``name``, ``iterhook(name)`` is a shortcut for ``hook("iterhook", name)``.
    """
    return hook("iterhook", name)


def iter_hooks(instance):
    """Iterates over the method of `instance` registered as hooks."""
    for attrname in dir(instance):
        attr = getattr(instance, attrname)
        if callable(attr) and hasattr(attr, "hooked"):
            for hooktype, hooks in getattr(attr, "hooked").items():
                for item in hooks:
                    yield hooktype, item, attr


def setmethodhook(
    *, getter: typing.Union[None, typing.Callable] = None
) -> typing.Callable:
    """Decorator to mark that a method can accept method and context :ref:`hooks`.

    :param function getter:
        Function that, given the instance object as argument,
        returns a :class:`plugins.Loader` object.
        If ``None``, the default ``self.shared.builder.plugins`` is used
        (``self`` is supposed to have this attribute).
    """

    def decorator(function):
        """Actual decorator."""
        if function.__name__ == "__init__":
            hookname = function.__qualname__[: -len(function.__name__) - 1]
        else:
            hookname = function.__qualname__

        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            """Wrapped function."""
            self = args[0]
            if getter is None:
                plugins = self.shared.builder.plugins
            else:
                plugins = getter(*args, **kwargs)

            return plugins.applymethodhook(hookname, function, *args, **kwargs)

        return wrapped

    return decorator
