# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.15.0] - 2022-04-18

### Added
- `music_parameters.WoodwindFingering`
- `music_parameters.Cue`


## [0.14.0] - 2022-04-18

### Added
- `music_parameters.WesternPitchInterval`
- default `subtract` method for `mutwo.music_parameters.abc.Pitch`
- `diatonic_pitch_class_name` property for `WesternPitch`
- `accidental_name` property for `WesternPitch`
- `is_microtonal` property for `WesternPitch`
- `enharmonic_pitch_tuple` property for `WesternPitch`
- `music_converters.ImproveWesternPitchListSequenceReadability`
- new dependency `gradient_free_optimizers`
- new constant `music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER`

### Changed
- `add` and `subtract` methods of `WesternPitch` (cleanup) -> support for `WesternPitchInterval` now
- `get_pitch_interval` of `WesternPitch` returns `WesternPitchInterval` if possible
- `music_converters.TwoPitchesToCommonHarmonics` to `music_converters.TwoPitchesToCommonHarmonicTuple`
- usage of standard music parser classes for playing_indicators and grace_notes converters
- `music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT` to `music_parameters.constants.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT`
- `music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT` to `music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT`

### Removed
- constant `music_parameters.constant.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT`
- constant `music_parameters.constant.ASCENDING_DIATONIC_PITCH_NAME_TUPLE`
- constant `music_parameters.constant.DIATONIC_PITCH_CLASS_COUNT`
- obscure `level` property of `JustIntonationPitch`


## [0.12.0] - 2022-04-03

### Changed
- use `SingleNumberParameter` class from `mutwo.ext-core` for all abstract parameters with one value
- `cents` attribute of `PitchInterval` to `instance` (in order to standardise attribute names; should be type and not unit)
- `find_pitch_variant_tuple` to `get_pitch_variant_tuple`

### Added
- abstract base classes to represent text/lyrics:
    - `mutwo.music_parameters.abc.Lyric`
    - `mutwo.music_parameters.abc.Syllable`
- module for lyrics:
    - `mutwo.music_parameters.DirectLyric`
    - `mutwo.music_parameters.LanguageBasedLyric`
    - `mutwo.music_parameters.LanguageBasedSyllable`
- new dependency phonemizer


## [0.11.0] - 2022-04-02

### Added
- various classes to standardise and simplify conversion of music parameters to simple music events:
    - `MutwoParameterDictToPitchList`
    - `MutwoParameterDictToVolume`
    - `MutwoParameterDictToPlayingIndicatorCollection`
    - `MutwoParameterDictToNotationIndicatorCollection`
    - `MutwoParameterDictToGraceNoteSequentialEvent`
    - `MutwoParameterDictToAfterGraceNoteSequentialEvent`
    - `MutwoParameterDictToNoteLike`


## [0.10.0] - 2022-03-30

### Added
- `get_pitch_interval` method to `Pitch` class
- `PitchAmbitus` class and `ambituses` module with `OctaveAmbitus` class


## [0.9.0] - 2022-03-23

### Changed
- split `constants` namespaces to `constants` / `configurations` (depending on use case)


## [0.8.0] - 2022-03-11

### Changed
- simplify the structure of `Pitch.PitchEnvelope` and `Pitch.PitchIntervalEnvelope`
    - renamed `make_generic_pitch_interval` to `cents_to_pitch_interval`
    - renamed `make_generic_pitch` to `frequency_to_pitch`
    - don't create on-the-fly classes, but simply use `DirectPitch` and `DirectPitchInterval`


## [0.7.0] - 2022-01-31

### Added
- various standard converters to extract from a simple event musical parameters:
    - `SimpleEventToPitchList`
    - `SimpleEventToVolume`
    - `SimpleEventToPlayingIndicatorCollection`
    - `SimpleEventToNotationIndicatorCollection`
    - `SimpleEventToGraceNoteSequentialEvent`
    - `SimpleEventToAfterGraceNoteSequentialEvent`


## [0.6.0] - 2022-01-30

### Changed
- `LoudnessToAmplitudeConverter` to `LoudnessToAmplitude`
- `RhythmicalStrataToIndispensabilityConverter` to `RhythmicalStrataToIndispensability`
- `TwoPitchesToCommonHarmonicsConverter` to `TwoPitchesToCommonHarmonics`


## [0.5.0] - 2022-01-30

### Changed
- package structure to namespace package to apply refactor of mutwo main package


## [0.4.0] - 2022-01-15

### Changed
- public API and general setup of `converters.symmetrical.playing_indicators` module


## [0.3.1] - 2022-01-14

### Added
- syntactic sugar for setting pitch envelope


## [0.3.0] - 2022-01-12

### Added
- music related generator modules (moved from mutwo.ext-common-generators)


## [0.2.0] - 2022-01-11

### Added
- music related parameter and converter modules (which have been removed from [mutwo core](https://github.com/mutwo-org/mutwo) in verion 0.49.0 with [commit ae94b531e431349d9c2b24c052498e1d96add6a4](https://github.com/mutwo-org/mutwo/commit/ae94b531e431349d9c2b24c052498e1d96add6a4))
