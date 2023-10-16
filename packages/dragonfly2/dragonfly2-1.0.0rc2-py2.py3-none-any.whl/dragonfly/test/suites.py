#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#

import logging
import os
import sys

import pytest

from dragonfly                   import get_engine
from dragonfly.log               import setup_log
from dragonfly._platform_checks  import IS_X11

# Setup logging.
_log = logging.getLogger("dfly.test")
setup_log()


# ==========================================================================

common_names = [
    "test_actions",
    "test_contexts",
    "test_basic_rule",
    "test_engine_nonexistent",
    "test_log",
    "test_parser",
    "test_lark_parser",
    "test_timer",
    "test_window",
    "documentation/test_action_base_doctest.txt",
    "documentation/test_grammar_elements_basic_doctest.txt",
    "documentation/test_grammar_elements_compound_doctest.txt",
    "documentation/test_grammar_list_doctest.txt",
    "documentation/test_recobs_doctest.txt",
]

# Include clipboard tests if on a desktop system: Windows/X11/macOS.
if os.name == "nt" or IS_X11 or sys.platform == "darwin":
    common_names.insert(2, "test_clipboard")

# Include accessibility tests if dragonfly.accessibility is available.
try:
    import dragonfly.accessibility
    common_names.insert(0, "test_accessibility")
except ImportError:
    pass

# Define spoken language test files. All of them work with the natlink and
# text engines. The English tests should work with sapi5 and sphinx by
# default.
language_names = [
    "test_language_de_number",
    "test_language_en_number",
    "test_language_nl_number",
]

# Define Natlink test names.
natlink_names = common_names + language_names + [
    "test_compiler_natlink",
    "test_dictation",
    "test_engine_natlink",
]

# Import the `natlinkstatus' module.  The module is in a different place in
#  newer versions of Natlink.
try:
    import natlinkstatus
except ImportError:
    try:
        from natlinkcore import natlinkstatus
    except:
        natlinkstatus = None

# If `natlinkstatus' was found it, use it to check the DNS version.
dns_version = None
if natlinkstatus:
    try:
        dns_version = int(natlinkstatus.NatlinkStatus().getDNSVersion())
    except:
        # Couldn't get the DNS version for whatever reason.
        pass

# Add the appropriate DNS word formatting doctest to the `natlink_names'
#  list, assuming v11 if the DNS version was indeterminable.
if dns_version and dns_version <= 10:
    natlink_names += ["documentation/test_word_formatting_v10_doctest.txt"]
else:
    natlink_names += ["documentation/test_word_formatting_v11_doctest.txt"]


# Define doctests for each engine.
engine_tests_dict = {
    "sapi5": [
        "test_engine_sapi5",
        "test_language_en_number",
    ] + common_names,

    "sphinx": [
        "test_engine_sphinx",
        "test_language_en_number",
        "test_dictation",
    ] + common_names,

    "kaldi": [
        "test_engine_kaldi",
        "test_language_en_number",

        # Note: Kaldi cannot handle the special characters in this file.
        # "test_dictation",
    ] + common_names,

    "text": [
        "test_engine_text",
        "test_dictation",
    ] + common_names + language_names,

    "natlink": natlink_names,
}


# Add aliases of 'sapi5'.
engine_tests_dict['sapi5inproc'] = engine_tests_dict['sapi5']
engine_tests_dict['sapi5shared'] = engine_tests_dict['sapi5']


engine_params_dict = {
    "kaldi": dict(audio_input_device=False),
}


# ==========================================================================


def run_pytest_suite(engine_name, pytest_options):
    # Get test file paths.
    paths = []
    for name in engine_tests_dict[engine_name]:
        if name.startswith("test_"):
            # Use full module paths so pytest can import the files
            # correctly.
            name = "dragonfly/test/" + name + ".py"

        paths.append(name)

    # Initialize the engine and call connect().
    engine_params = engine_params_dict.get(engine_name, {})
    engine = get_engine(engine_name, **engine_params)
    engine.connect()

    # Prevent the engine from running timers on its own. This lets us
    # avoid race conditions.
    engine._timer_manager.disable()
    try:
        # Run doctests through pytest.main() now that the engine is set up.
        # Pass any specified pytest options, followed by doctest options for
        # compatibility with both Python 2.7 and 3.
        args = pytest_options + [
            '-o',
            'doctest_optionflags=ALLOW_UNICODE IGNORE_EXCEPTION_DETAIL'
        ] + paths
        return pytest.main(args)
    finally:
        # Disconnect after the tests.
        engine.disconnect()

        # Check that the dragonfly engine was not changed during the tests.
        assert engine is get_engine(), \
            "The registered engine changed during the test suite."
