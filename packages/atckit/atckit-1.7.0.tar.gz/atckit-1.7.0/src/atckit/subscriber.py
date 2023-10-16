# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of AccidentallyTheCables Utility Kit,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
from typing import Callable
import typing_extensions

class FunctionSubscriber:
    """ Function subscriber


    Provides a += / -= interface for adding callback functions

    Example:

    \li Define some functions

        \code{.py}
        def a():
            print("a")
        def b():
            print("b")
        \endcode

    \li Create a subscriber and Subscribe the above functions
        \code{.py}
        f = FunctionSubscriber()
        f += a
        f += b
        print(f.functions)
        \endcode

    \li Remove a subscription
        \code{.py}
        f -= a
        print(f.functions)
        \endcode

    \li Execute subscribed functions
        \code{.py}
        for method_def in f.functions:
            method_def()
        \endcode
    """

    _functions:list[Callable]

    @property
    def functions(self) -> list[Callable]:
        """\b \e PROPERTY; Currently Subscribed Functions"""
        return self._functions

    def __init__(self) -> None:
        """Initializer
        """
        self._functions = []

    def __iadd__(self,fn:Callable) -> typing_extensions.Self:
        """Inline Add. Subscribe Function
        @param method \c fn Method to Subscribe
        """
        if fn not in self._functions:
            self._functions.append(fn)
        return self

    def __isub__(self,fn:Callable) -> typing_extensions.Self:
        """Inline Subtract. Unsubscribe Function
        @param method \c fn Method to Unsubscribe
        """
        if fn not in self._functions:
            return self
        i:int = self._functions.index(fn)
        self._functions.pop(i)
        return self
