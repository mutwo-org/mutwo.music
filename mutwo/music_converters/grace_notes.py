"""Apply grace notes on Events"""

import copy
import typing

from mutwo import core_converters
from mutwo import core_events
from mutwo import core_parameters
from mutwo import music_converters

__all__ = ("GraceNotesConverter",)


class GraceNotesConverter(core_converters.abc.EventConverter):
    """Apply grace notes and after grace notes on :class:`core_events.abc.Event`.

    :param minima_grace_notes_duration_factor: Minimal percentage how much
        of the initial duration of the :class:`~mutwo.core_events.Chronon`
        shall be moved to the grace notes / after grace notes. This value has to be
        smaller than 0.5 (so that the :class:`Chronon` have a
        duration > 0 if it has both: grace notes and after grace notes)
        and bigger than 0 (so that the grace notes or after grace notes
        have a duration > 0). Default to 0.12.
    :type minima_grace_notes_duration_factor: float
    :param maxima_grace_notes_duration_factor: Maxima percentage how much
        of the initial duration of the :class:`~mutwo.core_events.Chronon`
        shall be moved to the grace notes / after grace notes. This value has to be
        smaller than 0.5 (so that the :class:`Chronon` have a
        duration > 0 if it has both: grace notes and after grace notes)
        and bigger than 0 (so that the grace notes or after grace notes
        have a duration > 0). Default to 0.25.
    :type maxima_grace_notes_duration_factor: float
    :param minima_number_of_grace_notes: For how many events in the grace
        note or after grace note container shall the
        `minima_grace_notes_duration_factor` be applied. Default to 1.
    :type minima_number_of_grace_notes: int
    :param maxima_number_of_grace_notes: For how many events in the grace
        note or after grace note container shall the
        `maxima_number_of_grace_notes` be applied. Default to 4.
    :type maxima_number_of_grace_notes: int
    :param chronon_to_grace_note_consecution: Function which
        receives as an input a :class:`~mutwo.core_events.Chronon`
        and returns a :class:`~mutwo.core_events.Consecution`.
        By default the function will ask the event for a
        :attr:`~mutwo.events.music.NoteLike.grace_note_consecution`
        attribute, because by default `~mutwo.events.music.NoteLike`
        objects are expected.
    :type chronon_to_grace_note_consecution: typing.Callable[[core_events.Chronon], core_events.Consecution[core_events.Chronon]]
    :param chronon_to_after_grace_note_consecution: Function which
        receives as an input a :class:`~mutwo.core_events.Chronon`
        and returns a :class:`~mutwo.core_events.Consecution`.
        By default the function will ask the event for a
        :attr:`~mutwo.events.music.NoteLike.grace_note_consecution`
        attribute, because by default `~mutwo.events.music.NoteLike`
        objects are expected.
    :type chronon_to_after_grace_note_consecution: typing.Callable[[core_events.Chronon], core_events.Consecution[core_events.Chronon]]
    """

    def __init__(
        self,
        minima_grace_notes_duration_factor: float = 0.12,
        maxima_grace_notes_duration_factor: float = 0.25,
        minima_number_of_grace_notes: int = 1,
        maxima_number_of_grace_notes: int = 4,
        chronon_to_grace_note_consecution: typing.Callable[
            [core_events.Chronon],
            core_events.Consecution[core_events.Chronon],
        ] = music_converters.ChrononToGraceNoteConsecution(),
        chronon_to_after_grace_note_consecution: typing.Callable[
            [core_events.Chronon],
            core_events.Consecution[core_events.Chronon],
        ] = music_converters.ChrononToAfterGraceNoteConsecution(),
    ):
        self._test_input(
            minima_grace_notes_duration_factor,
            maxima_grace_notes_duration_factor,
            minima_number_of_grace_notes,
            maxima_number_of_grace_notes,
        )

        self._chronon_to_grace_note_consecution = (
            chronon_to_grace_note_consecution
        )
        self._chronon_to_after_grace_note_consecution = (
            chronon_to_after_grace_note_consecution
        )

        self._n_grace_notes_to_grace_note_duration_factor_envelope = (
            core_events.Envelope(
                (
                    (minima_number_of_grace_notes, minima_grace_notes_duration_factor),
                    (maxima_number_of_grace_notes, maxima_grace_notes_duration_factor),
                )
            )
        )

    @staticmethod
    def _test_input(
        minima_grace_notes_duration_factor: float,
        maxima_grace_notes_duration_factor: float,
        minima_number_of_grace_notes: int,
        maxima_number_of_grace_notes: int,
    ):
        try:
            assert minima_number_of_grace_notes < maxima_number_of_grace_notes
        except AssertionError:
            raise ValueError(
                "'minima_number_of_grace_notes' has to be smaller "
                "than 'maxima_number_of_grace_notes'!"
            )

        try:
            assert (
                minima_grace_notes_duration_factor < maxima_grace_notes_duration_factor
            )
        except AssertionError:
            raise ValueError(
                "'minima_grace_notes_duration_factor' has to "
                "be smaller than 'maxima_grace_notes_duration_factor'!"
            )

        try:
            assert maxima_grace_notes_duration_factor < 0.5
        except AssertionError:
            raise ValueError(
                "'maxima_grace_notes_duration_factor' has " "to be smaller than 0.5!"
            )

        try:
            assert minima_grace_notes_duration_factor > 0
        except AssertionError:
            raise ValueError(
                "'minima_grace_notes_duration_factor' has " "to be bigger than 0!"
            )

    def _get_grace_note_consecution(
        self, chronon_to_convert: core_events.Chronon
    ) -> core_events.Consecution[core_events.Chronon]:
        return self._chronon_to_grace_note_consecution(
            chronon_to_convert
        )

    def _get_after_grace_note_consecution(
        self, chronon_to_convert: core_events.Chronon
    ) -> core_events.Consecution[core_events.Chronon]:
        return self._chronon_to_after_grace_note_consecution(
            chronon_to_convert
        )

    def _convert_chronon(
        self,
        event_to_convert: core_events.Chronon,
        _: core_parameters.abc.Duration.Type,
    ) -> core_events.Consecution[core_events.Chronon]:
        """Convert instance of :class:`mutwo.core_events.Chronon`."""

        def adjust_grace_note_consecution(
            grace_note_consecution: core_events.Consecution[
                core_events.Chronon
            ],
        ) -> core_events.Consecution:
            if grace_note_consecution:
                factor_to_main_event = (
                    self._n_grace_notes_to_grace_note_duration_factor_envelope.value_at(
                        len(grace_note_consecution)
                    )
                )
                new_duration = event_to_convert.duration * factor_to_main_event
                grace_note_consecution = grace_note_consecution.copy()
                grace_note_consecution.duration = new_duration
            return grace_note_consecution

        grace_note_consecution = adjust_grace_note_consecution(
            self._get_grace_note_consecution(event_to_convert)
        )
        after_grace_note_consecution = adjust_grace_note_consecution(
            self._get_after_grace_note_consecution(event_to_convert)
        )

        copied_event_to_convert = copy.deepcopy(event_to_convert)
        # Remove applied grace notes / after grace notes
        copied_event_to_convert.grace_note_consecution = (
            core_events.Consecution([])
        )
        copied_event_to_convert.after_grace_note_consecution = (
            core_events.Consecution([])
        )
        copied_event_to_convert.duration -= (
            grace_note_consecution.duration
            + after_grace_note_consecution.duration
        )

        grace_note_consecution.append(copied_event_to_convert)
        grace_note_consecution.extend(after_grace_note_consecution)

        return grace_note_consecution

    def _convert_simultaneous_event(
        self,
        simultaneous_event: core_events.Concurrence,
        absolute_entry_delay: core_parameters.abc.Duration.Type,
    ) -> tuple[core_events.Concurrence[core_events.abc.Event]]:
        """Convert instance of :class:`mutwo.core_events.Concurrence`."""

        simultaneous_event_copied = simultaneous_event.empty_copy()
        for event in simultaneous_event:
            converted_event = self._convert_event(event, absolute_entry_delay)
            # If we find a chronon, we shouldn't extend but append it to the
            # the Concurrence. A converted chronon will be a
            # Consecution. The grace notes and after grace notes should
            # happen before and after the respective event. If we extend
            # the whole Consecution to the Concurrence the
            # grace notes and after grace notes will be played simultaneously
            # with the main note, therefore we have to append them.
            if isinstance(event, core_events.Chronon):
                simultaneous_event_copied.append(converted_event)
            else:
                simultaneous_event_copied.extend(converted_event)
        return (simultaneous_event_copied,)

    def _convert_consecution(
        self,
        consecution: core_events.Consecution,
        absolute_entry_delay: core_parameters.abc.Duration.Type,
    ) -> tuple[core_events.Consecution[core_events.abc.Event]]:
        consecution_copied = consecution.empty_copy()
        consecution_copied.extend(
            super()._convert_consecution(consecution, absolute_entry_delay)
        )
        return (consecution_copied,)

    def convert(self, event_to_convert: core_events.abc.Event) -> core_events.abc.Event:
        """Apply grace notes and after grace notes of all :class:`Chronon`.

        :param event_to_convert: The event which grace notes and after grace
            notes shall be converted to normal events in the upper
            :class:`Consecution`.
        :type event_to_convert: core_events.abc.Event
        """

        converted_event = self._convert_event(event_to_convert, 0)
        if isinstance(event_to_convert, core_events.Chronon):
            return converted_event
        else:
            return converted_event[0]
