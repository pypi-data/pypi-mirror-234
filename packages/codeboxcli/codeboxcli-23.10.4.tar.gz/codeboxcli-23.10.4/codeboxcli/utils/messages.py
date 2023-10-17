# -*- coding: utf-8 -*-
import importlib


def help_default(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.help_default


def help_add(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.help_add


def help_delete(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.help_delete


def help_edit(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.help_edit


def help_share(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.help_share


def error_invalid_subcommand(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_invalid_subcommand


def error_missing_value(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_missing_value.format(value=value)


def error_missing_argument(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_missing_argument.format(value=value)


def error_unknown_argument(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_unknown_argument.format(value=value)


def error_saving(language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_saving


def error_not_found(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.error_not_found.format(value=value)


def share_url(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.share_url.format(value=value)


def share_error(value, language="en"):
    try:
        lang = importlib.import_module("codeboxcli.locales." + language)
    except ImportError:
        lang = importlib.import_module("codeboxcli.locales.en")
    return lang.share_error.format(value=value)
