#!/usr/bin/env python3

import gettext


def get_user_name():
    return input(_("What is your name?: "))


def say_hello(name):
    print(_("Hello {0}!").format(name))


if __name__ == "__main__":
    gettext.install("helloworld", localedir="locales")
    name = get_user_name()
    say_hello(name)
