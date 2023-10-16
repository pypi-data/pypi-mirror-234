#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a Sample Python file."""


from __future__ import annotations


def hello_world(i: int = 0) -> str:
    """Doc String."""
    print("Hello world")
    return f"string-{i}"


def good_night() -> str:
    """This is Ken's doc string for good_night."""
    print("Good night")
    return "string"


def hello_goodbye():
    """This is the new hello_goodbye docstring for demo.  From home"""
    hello_world(1)
    good_night()
