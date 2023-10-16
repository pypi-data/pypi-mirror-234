﻿#
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

"""
EngineBase class
============================================================================

"""

import locale
import logging

import six

from dragonfly.engines.base.timer import Timer
from dragonfly.engines.base.dictation import DictationContainerBase
import dragonfly.engines


#---------------------------------------------------------------------------

class EngineError(Exception):
    pass

class MimicFailure(EngineError):
    pass


#---------------------------------------------------------------------------

class EngineContext(object):

    def __init__(self, engine):
        self._engine = engine

    def __enter__(self):
        self._engine.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._engine.disconnect()


#---------------------------------------------------------------------------

class EngineBase(object):
    """ Base class for engine-specific back-ends. """

    _log = logging.getLogger("engine")
    _name = "base"
    _timer_manager = None
    DictationContainer = DictationContainerBase

    #-----------------------------------------------------------------------

    def __init__(self):
        # Register initialization of this engine.
        dragonfly.engines.register_engine_init(self)

        self._grammar_wrappers = {}
        self._recognition_observer_manager = None

        # Recognizing quoted words (literals) is not supported by default.
        self._has_quoted_words_support = False

#    def __del__(self):
#        try:
#            try:
#                self.disconnect()
#            except Exception, e:
#                self._log.exception("Engine destructor raised an exception: %s" % e)
#        except:
#            pass

    def __repr__(self):
        return "%s()" % self.__class__.__name__

    @property
    def name(self):
        """ The human-readable name of this engine. """
        return self._name

    @property
    def grammars(self):
        """ Grammars loaded into this engine. """
        # Return a list of each GrammarWrapper's Grammar object.
        return [w.grammar for w in self._grammar_wrappers.values()]

    def connect(self):
        """ Connect to back-end SR engine. """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def disconnect(self):
        """ Disconnect from back-end SR engine. """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def connection(self):
        """ Context manager for a connection to the back-end SR engine. """
        return EngineContext(self)

    #-----------------------------------------------------------------------
    # Methods for administrating timers.

    def create_timer(self, callback, interval, repeating=True):
        """ Create and return a timer using the specified callback and
            repeat interval. """
        return Timer(callback, interval, self._timer_manager, repeating)

    #-----------------------------------------------------------------------
    # Methods for working with grammars.

    def load_grammar(self, grammar):
        wrapper_key = id(grammar)
        if wrapper_key in self._grammar_wrappers:
            self._log.warning("Grammar %s loaded multiple times." % grammar)
            return

        wrapper = self._load_grammar(grammar)
        self._grammar_wrappers[wrapper_key] = wrapper

    def _load_grammar(self, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def unload_grammar(self, grammar):
        wrapper_key = id(grammar)
        if wrapper_key not in self._grammar_wrappers:
            raise EngineError("Grammar %s cannot be unloaded because"
                              " it was never loaded." % grammar)
        wrapper = self._grammar_wrappers.pop(wrapper_key)
        self._unload_grammar(grammar, wrapper)

    def _unload_grammar(self, grammar, wrapper):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def update_list(self, lst, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def activate_grammar(self, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def deactivate_grammar(self, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def activate_rule(self, rule, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def deactivate_rule(self, rule, grammar):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def set_exclusiveness(self, grammar, exclusive):
        """ Set the exclusiveness of a grammar. """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def set_exclusive(self, grammar, exclusive):
        """ Alias of :meth:`set_exclusiveness`. """
        self.set_exclusiveness(grammar, exclusive)

    def _get_grammar_wrapper(self, grammar):
        wrapper_key = id(grammar)
        if wrapper_key not in self._grammar_wrappers:
            raise EngineError("Grammar %s never loaded." % grammar)
        wrapper = self._grammar_wrappers[wrapper_key]
        return wrapper

    #-----------------------------------------------------------------------
    # Recognition observer methods.

    def register_recognition_observer(self, observer):
        self._recognition_observer_manager.register(observer)

    def unregister_recognition_observer(self, observer):
        self._recognition_observer_manager.unregister(observer)

    def enable_recognition_observers(self):
        self._recognition_observer_manager.enable()

    def disable_recognition_observers(self):
        self._recognition_observer_manager.disable()

    #-----------------------------------------------------------------------
    #  Miscellaneous methods.

    def do_recognition(self, begin_callback=None, recognition_callback=None,
                       failure_callback=None, end_callback=None,
                       *args, **kwargs):
        """
        Recognize speech in a loop until interrupted or :meth:`disconnect`
        is called.

        Recognition callback functions can optionally be registered.

        Extra positional and key word arguments are passed to
        :meth:`_do_recognition`.

        :param begin_callback: optional function to be called when speech
            starts.
        :type begin_callback: callable | None
        :param recognition_callback: optional function to be called on
            recognition success.
        :type recognition_callback: callable | None
        :param failure_callback: optional function to be called on
            recognition failure.
        :type failure_callback: callable | None
        :param end_callback: optional function to be called when speech
            ends, either successfully (after calling the recognition
            callback) or in failure (after calling the failure callback).
        :type end_callback: callable | None
        """
        # Import locally to avoid cycles.
        from dragonfly.grammar.recobs_callbacks import (
            register_beginning_callback, register_recognition_callback,
            register_failure_callback, register_ending_callback
        )

        if begin_callback:
            register_beginning_callback(begin_callback)
        if recognition_callback:
            register_recognition_callback(recognition_callback)
        if failure_callback:
            register_failure_callback(failure_callback)
        if end_callback:
            register_ending_callback(end_callback)

        # Call _do_recognition() to start recognizing.
        self._do_recognition(*args, **kwargs)

    def _do_recognition(self, *args, **kwargs):
        """
            Recognize speech in a loop until interrupted or
            :meth:`disconnect` is called.

            This method should be implemented by each engine.

        """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def process_grammars_context(self, window=None):
        """
            Enable/disable grammars & rules based on their current contexts.

            This must be done preemptively for some SR engine back-ends,
            such as WSR, that don't apply context changes upon/after the
            utterance start has been detected.  The WSR engine calls this
            automatically whenever the foreground application (or its
            title) changes.

            The *window* parameter is optional window information, which can
            be passed in as an optimization if it has already been gathered.

            The user may wish to call this method to update if custom
            contexts are used.

            .. note ::

               This method does not trigger the *on_begin()* methods of
               recognition observers.

        """

        if window is None:
            from dragonfly.windows.window import Window
            window = Window.get_foreground()

        # Disable recognition observers for the duration.
        self.disable_recognition_observers()
        for grammar in self.grammars:
            grammar.process_begin(window.executable, window.title,
                                  window.handle)
        self.enable_recognition_observers()

    def dispatch_recognition_other(self, grammar, words, results):
        """
            Dispatch recognition data for a grammar to all other grammars
            with a ``process_recognition_other`` method.

        """
        # Get a list of all grammar wrappers.
        wrappers = self._grammar_wrappers.copy().values()

        # Raise an error if the specified grammar was not loaded.
        wrapper_key = id(grammar)
        if wrapper_key not in self._grammar_wrappers:
            raise EngineError("Grammar %s never loaded." % grammar)

        # Attempt to call process_recognition_other() for each appropriate
        #  grammar.
        # Note: This is how recognition observers work.
        if wrapper_key in wrappers: wrappers.pop(wrapper_key)
        for wrapper in wrappers:
            wrapper.recognition_other_callback(words, results)

    def dispatch_recognition_failure(self, results):
        """
            Dispatch results data to all grammars with a
            ``process_recognition_failure`` method.

        """
        # Get a list of all grammar wrappers.
        wrappers = self._grammar_wrappers.copy().values()

        # Attempt to call process_recognition_failure() for each grammar.
        # Note: This is how recognition observers work.
        for wrapper in wrappers:
            wrapper.recognition_failure_callback(results)

    @classmethod
    def _get_words_rules(cls, words, rule_id):
        # Construct and return a sequence of (word, rule_id) 2-tuples.
        # Convert any binary words to Unicode.
        encoding = locale.getpreferredencoding()
        result = []
        for word in words:
            if isinstance(word, six.binary_type):
                word = word.decode(encoding)
            result.append((word, rule_id))
        return tuple(result)

    def mimic(self, words):
        """ Mimic a recognition of the given *words*. """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    def speak(self, text):
        """ Speak the given *text* using text-to-speech. """
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)

    @property
    def language(self):
        """
        Current user language of the SR engine. (Read-only)

        :rtype: str
        """
        return self._get_language()

    @classmethod
    def _get_language_tag(cls, language_id):
        # Get a language tag from the Windows language identifier.
        language_tags = cls._language_tags
        tags = language_tags.get(language_id)
        if tags: return tags[0]

        # The dictionary didn't contain the language, so try to get a match
        #  using the primary language identifier instead.  This allows us to
        #  match unlisted language variants.
        primary_id = language_id & 0x00ff
        for language_id2, (tag, _) in language_tags.items():
            if primary_id == language_id2 & 0x00ff:  return tag

        # Speaker language wasn't found.
        cls._log.error("Unknown speaker language: 0x%04x" % language_id)
        raise EngineError("Unknown speaker language: 0x%04x" % language_id)

    _language_tags = {
                      0x0c09: ("en", "AustralianEnglish"),
                      0xf00a: ("es", "CastilianSpanish"),
                      0xf809: ("en", "CAEnglish"),
                      0x0004: ("zh", "Chinese"),
                      0x0413: ("nl", "Dutch"),
                      0x0009: ("en", "English"),
                      0x040c: ("fr", "French"),
                      0x0407: ("de", "German"),
                      0xf009: ("en", "IndianEnglish"),
                      0x0410: ("it", "Italian"),
                      0x0411: ("jp", "Japanese"),
                      0xf40a: ("es", "LatinAmericanSpanish"),
                      0x0416: ("pt", "Portuguese"),
                      0xf409: ("en", "SingaporeanEnglish"),
                      0x040a: ("es", "Spanish"),
                      0x0809: ("en", "UKEnglish"),
                      0x0409: ("en", "USEnglish"),
                     }

    def _get_language(self):
        raise NotImplementedError("Virtual method not implemented for"
                                  " engine %s." % self)
    @property
    def quoted_words_support(self):
        """
        Whether this engine can compile and recognize quoted words.

        :rtype: bool
        """
        return self._has_quoted_words_support
