# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.28.0] - 2025-02-19

### Changed
- `parameters/Pitch.from_any`: parse numbers as frequency and not as pitch class, see [here](https://github.com/mutwo-org/mutwo.music/commit/81011b9fe3400a5135ffae460de608d330539f75)
- `parameters/Volume.from_any`: allow parsing strings not only for WesternVolume, see [here](https://github.com/mutwo-org/mutwo.music/commit/1dd5aebce2a8b53d4e0b4fe015c5d0ebacaf3e7f)
- `parameters/Volume.from_any`: always interpret all numbers as decibels, see [here](https://github.com/mutwo-org/mutwo.music/commit/39f7da6fd9cb80a78240e0443fc1ea7767db5340)

### Fixed
- `converters/GraceNotesConverter`: Fix conversion of concurrences, see [here](https://github.com/mutwo-org/mutwo.music/commit/7456740348d3be16a1ffc57b49851ef9b053c129)


## [0.27.0] - 2024-04-25

This updates 'mutwo.music' to 'mutwo.core >= 2.0.0'.
It also follows the same refactoring procedure as mutwo.core, if they apply here.

### Added
- `FlexPitch` and `FlexVolume`, see [here](https://github.com/mutwo-org/mutwo.music/commit/3a336f4cf9c9387453e99f52a1cc823ee4436992)

### Changed
- `Pitch.frequency` to `Pitch.hertz`. `PitchInterval.interval` to `PitchInterval.cents`, `Volume.amplitude` to `Volume.decibel`, `Lyric.phonetic_representation` to `Lyric.xsampa`, see [here](https://github.com/mutwo-org/mutwo.core/commit/9f08dcacc8e82a1bba3c69977a1f4f3b8e322f94) for rationale and [here](https://github.com/mutwo-org/mutwo.music/commit/6c8b416833196e8c4d3c9e4a6edaf69df85d516b) for actual change
- `IndicatorCollection.get_all_indicator()` to `IndicatorCollection.indicator_tuple` and `IndicatorCollection.get_indicator_dict()` to `Indicator_collection.indicator_dict`, see [here](https://github.com/mutwo-org/mutwo.music/commit/92bf4975f1a30477f30687197540246503402642)
- all `music_events.configurations.UNKNOWN_TO_OBJECT_TO_X` to `music_parameters.abc.X.from_any`, see [here](https://github.com/mutwo-org/mutwo.music/commit/500387bcac9db09f025f9e55b068970af5b9e44d)
- `IndicatorCollection` from dataclass to registry supported class, see [here](https://github.com/mutwo-org/mutwo.music/commit/cc91c391878c4b0dfb8ec8658caf1b50ed48d3ef)


## [0.26.0] - 2023-12-27

### Added
- Add syntactic sugar for indicator collections initialization in `NoteLike`, see [here](https://github.com/mutwo-org/mutwo.music/commit/0a018af78f2adf4d473896b32dbe91994abf772f)
- `music_parameters.Slur`, see [here](https://github.com/mutwo-org/mutwo.music/commit/7767d1a99bdf17c6aec970fde2e82e3ce55c46b6)
- `music_utilities.linear_space` to replace `numpy.linspace`, see [here](https://github.com/mutwo-org/mutwo.music/commit/7b46f656b7f1c077d6417fc9987b6438131d33c5)

### Fixed
- Fix empty string in pitch parser of `NoteLike`, see [here](https://github.com/mutwo-org/mutwo.music/commit/9b01ba9126444e80d54991b5e0a33f2c217d1e62)

### Changed
- `music_parameters.Pedal.pedal_type` to `music_parameters.Pedal.type` and `music_parameters.Pedal.pedal_activity` to `music_parameters.Pedal.activity`, see [here](https://github.com/mutwo-org/mutwo.music/commit/abc74d582c36d939e49cb7081ac5bc03a3e467be)
- simplify pitch interval constants, see [here](https://github.com/mutwo-org/mutwo.music/commit/5fd03c01d7b0a4eca9f865011dc776dc885274ed)

### Removed
- `music_converters.LoudnessToAmplitude`, see [here](https://github.com/mutwo-org/mutwo.music/commit/41239d1bdeb03297cb9c96f8854aeed8dbca8674)


## [0.25.0] - 2023-10-24

### Added
- `music_parameters.ScalePitch`, see [here](https://github.com/mutwo-org/mutwo.music/commit/4c0e6738c15587225d80967e9fc0c0e6596dc6b2)

## [0.24.0] - 2023-08-25

### Added
- `music_parameters.ScaleFamily.scale_degree_count` and `music_parameters.Scale.scale_degree_count`, see [here](https://github.com/mutwo-org/mutwo.music/commit/60c6b9b7da022b81728fa8c429d7bfe71b506971)

### Changed
- `music_parameters.DecibelVolume.decibel` is now settable, see [here](https://github.com/mutwo-org/mutwo.music/commit/bb4d0305ee8a7b19c19d3c4fc1d495f46a7a1ab2)

### Removed
- `music_generators.make_product_pitch`, `music_generators.make_common_product_set_scale` and `music_generators.make_wilsons_brun_euclidean_algorithm_generator`, see [here](https://github.com/mutwo-org/mutwo.music/commit/f75b83be5ca26e2586c11f957afbe3eeeda2b13e)
- `music_converters.ImproveWesternPitchListSequenceReadability`, see [here](https://github.com/mutwo-org/mutwo.music/commit/fa315272b0b7bd5ccd4a67c372940344aace570a)
- `BodyPart` and `Fingering`, see [here](https://github.com/mutwo-org/mutwo.music/commit/3d39b5a26158fea99405430927f08a8e10268858)

### Fixed
- missing quicktions dependency, see [here](https://github.com/mutwo-org/mutwo.music/commit/ba8a2908e405e05efe300818c191492a516bc6f5)   
- more unspecified dependencies, see [here](https://github.com/mutwo-org/mutwo.music/commit/2f209ccc7ec24adeebc2281021e383bfcbd644b4)


## [0.23.0] - 2023-04-23

### Added
- `index` property to `music_parameters.String`, see [here](https://github.com/mutwo-org/mutwo.music/commit/f39421db0534e019b7968d4dfaa15869f87d8c4a)
- `WesternPitch.round_to` in order to round microtonal pitches, see [here](https://github.com/mutwo-org/mutwo.music/commit/5f0496d095b3bdb315fafb9da2316f13642a1baa)

### Fixed
- allow initialization of empty `Orchestration`, see [here](https://github.com/mutwo-org/mutwo.music/commit/ce910b19523ba7d5ca8780dd966a3cf08b36d051)
- comparision with `JustIntonationPitch` and another pitch, see [here](https://github.com/mutwo-org/mutwo.music/commit/7f414d541c2373ad9c0b11f1eebd9bb8b10d8a0d)


## [0.22.0] - 2022-12-31

### Added
- `natural_harmonic` property to `music_parameters.NaturalHarmonic.Node`

### Changed
- `music_parameters.PlayingIndicatorCollection.natural_harmonic_list` to `music_parameters.PlayingIndicatorCollection.natural_harmonic_node_list`
- `music_parameters.Ottava.n_octaves` to `music_parameters.Ottava.octave_count`
- `music_parameters.Fermata.fermata_type` to `music_parameters.Fermata.type`
- `music_parameters.Cue.cue_count` to `music_parameters.Cue.index`


## [0.21.0] - 2022-12-30

### Added
- orchestration namespace tool with `mutwo.music_parameters.Orchestration`
- `instrument_list` attribute to `mutwo.music_events.NoteLike`
- `optional` playing indicator in `mutwo.music_parameters.PlayingIndicatorCollection` to denote optional events
- `OptionalConverter` in `mutwo.music_converters` to apply `optional` playing indicator
- classes to model fingerings:
    - `mutwo.music_parameters.abc.Fingering`
    - `mutwo.music_parameters.abc.BodyPart`
- allow + and - operations on two `mutwo.music_parameters.abc.PitchInterval`
- new instrument `mutwo.music_parameters.CelticHarp`
- new attribute `interval` for `music_parameters.Partial`
- classes to model stringed instruments and natural harmonics:
    - `mutwo.music_parameters.NaturalHarmonic`
    - `mutwo.music_parameters.String`
    - `mutwo.music_parameters.StringInstrument`

### Changed
- set default value of `pitch_list` for `mutwo.music_events.NoteLike` to `[]`: `NoteLike` has no pitches by default.
- moved builtin instruments from global variables in `mutwo.music_parameters.constants` to ordinary classes in `mutwo.music_parameters`
- `music_parameters.Partial.nth_partial` to `music_parameters.Partial.index`
- attributes of playing indicators:
    - `music_parameters.Ornamentation.n_times` -> `music_parameters.Ornamentation.count`
    - `music_parameters.ArtificalHarmonic.n_semitones` -> `music_parameters.ArtificalHarmonic.semitone_count`
    - `music_parameters.Tremolo.n_flags` -> `music_parameters.Tremolo.flag_count`

### Removed
- natural harmonic indicators have been replaced by new `NaturalHarmonicList`. Removed:
    - `music_parameters.PreciseNaturalHarmonic`
    - `music_parameters.PlayingIndicatorCollection.precise_natural_harmonic` and `music_parameters.PlayingIndicatorCollection.natural_harmonic`


## [0.20.0] - 2022-12-10

### Changed
- `mutwo.music_parameters.WesternPitch.inverse_direction` to `mutwo.music_parameters.WesternPitch.inverse`
- make the syntactic sugar of `mutwo.music_events.NoteLike` initialization explicit and configurable, see [here for more information](https://github.com/mutwo-org/mutwo.music/commit/bf47a452d8553ef001c5192393d697d0c9536dd2)

### Added
- new abstract method `mutwo.music_parameters.abc.PitchInterval.inverse`
    - added new concrete method: `mutwo.music_parameters.DirectPitchInterval.inverse`
- implementations of musical scale representations:
    - `mutwo.music_parameters.Scale`
    - `mutwo.music_parameters.ScaleFamily`
    - `mutwo.music_parameters.RepeatingScaleFamily`
- basic instrument representations:
    - `mutwo.music_parameters.abc.Instrument`
    - `mutwo.music_parameters.abc.PitchedInstrument`
    - `mutwo.music_parameters.UnpitchedInstrument`
    - `mutwo.music_parameters.ContinuousPitchedInstrument`
    - `mutwo.music_parameters.DiscreetPitchedInstrument`
    - few constants (very incomplete list of instruments):
        - `mutwo.music_parameters.constants.BF_CLARINET`
        - `mutwo.music_parameters.constants.OBOE`
        - ...

### Fixed
- comparison of `JustIntonationPitch` with other `PitchInterval` (==, <, <=, ... operator), see [here](https://github.com/mutwo-org/mutwo.music/commit/795e2d59fa54eda3cb886bbe5417cbc2903c3ebe)


## [0.19.0] - 2022-11-04

### Dropped
- python 3.9 support


## [0.18.0] - 2022-10-07

### Added
- nix installation

### Changed
- dependency from `phonemizer` to `epitran`
- prime calculations from `primesieve` to `sympy`

## [0.17.0] - 2022-08-10

### Added
- `mutwo.music_version` subpackage

### Changed
- package name from `mutwo.ext-music` to `mutwo.music`
- to new duration model of `mutwo.core`


## [0.16.0] - 2022-05-02

### Added
- `niente` to `music_parameters.Hairpin`
- `<>` to allowed hairpin symbols


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
