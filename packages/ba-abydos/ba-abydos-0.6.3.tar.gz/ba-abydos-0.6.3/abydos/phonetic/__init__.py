# Copyright 2014-2020 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.phonetic.

The phonetic package includes classes for phonetic algorithms,
including:

    - Robert C. Russell's Index (:py:class:`.RussellIndex`)
    - American Soundex (:py:class:`.Soundex`)
    - Refined Soundex (:py:class:`.RefinedSoundex`)
    - Daitch-Mokotoff Soundex (:py:class:`.DaitchMokotoff`)
    - NYSIIS (:py:class:`.NYSIIS`)
    - Match Rating Algorithm (:py:class:`.phonetic.MRA`)
    - Metaphone (:py:class:`.Metaphone`)
    - Double Metaphone (:py:class:`.DoubleMetaphone`)
    - Caverphone (:py:class:`.Caverphone`)
    - Alpha Search Inquiry System (:py:class:`.AlphaSIS`)
    - Fuzzy Soundex (:py:class:`.FuzzySoundex`)
    - Phonex (:py:class:`.Phonex`)
    - Phonem (:py:class:`.Phonem`)
    - Phonix (:py:class:`.Phonix`)
    - PHONIC (:py:class:`.PHONIC`)
    - Standardized Phonetic Frequency Code (:py:class:`.SPFC`)
    - Statistics Canada (:py:class:`.StatisticsCanada`)
    - LEIN (:py:class:`.LEIN`)
    - Roger Root (:py:class:`.RogerRoot`)
    - Eudex phonetic hash (:py:class:`.phonetic.Eudex`)
    - Parmar-Kumbharana (:py:class:`.ParmarKumbharana`)
    - Davidson's Consonant Code (:py:class:`.Davidson`)
    - SoundD (:py:class:`.SoundD`)
    - PSHP Soundex/Viewex Coding (:py:class:`.PSHPSoundexFirst` and
      :py:class:`.PSHPSoundexLast`)
    - Dolby Code (:py:class:`.Dolby`)
    - NRL English-to-phoneme (:py:class:`.NRL`)
    - Ainsworth grapheme to phoneme (:py:class:`.Ainsworth`)
    - Beider-Morse Phonetic Matching (:py:class:`.BeiderMorse`)

There are also language-specific phonetic algorithms for German:

    - Kölner Phonetik (:py:class:`.Koelner`)
    - phonet (:py:class:`.Phonet`)
    - Haase Phonetik (:py:class:`.Haase`)
    - Reth-Schek Phonetik (:py:class:`.RethSchek`)

For French:

    - FONEM (:py:class:`.FONEM`)
    - an early version of Henry Code (:py:class:`.HenryEarly`)

For Spanish:

    - Phonetic Spanish (:py:class:`.PhoneticSpanish`)
    - Spanish Metaphone (:py:class:`.SpanishMetaphone`)

For Swedish:

    - SfinxBis (:py:class:`.SfinxBis`)
    - Wåhlin (:py:class:`.Waahlin`)

For Norwegian:

    - Norphone (:py:class:`.Norphone`)

For Brazilian Portuguese:

    - SoundexBR (:py:class:`.SoundexBR`)

And there are some hybrid phonetic algorithms that employ multiple underlying
phonetic algorithms:

    - Oxford Name Compression Algorithm (ONCA) (:py:class:`.ONCA`)
    - MetaSoundex (:py:class:`.MetaSoundex`)


Each class has an ``encode`` method to return the phonetically encoded string.
Classes for which ``encode`` returns a numeric value generally have an
``encode_alpha`` method that returns an alphabetic version of the phonetic
encoding, as demonstrated below:

>>> rus = RussellIndex()
>>> rus.encode('Abramson')
'128637'
>>> rus.encode_alpha('Abramson')
'ABRMCN'

----

"""

from abydos.phonetic._ainsworth import Ainsworth
from abydos.phonetic._alpha_sis import AlphaSIS
from abydos.phonetic._beider_morse import BeiderMorse
from abydos.phonetic._caverphone import Caverphone
from abydos.phonetic._daitch_mokotoff import DaitchMokotoff
from abydos.phonetic._davidson import Davidson
from abydos.phonetic._dolby import Dolby
from abydos.phonetic._double_metaphone import DoubleMetaphone
from abydos.phonetic._eudex import Eudex
from abydos.phonetic._fonem import FONEM
from abydos.phonetic._fuzzy_soundex import FuzzySoundex
from abydos.phonetic._haase import Haase
from abydos.phonetic._henry_early import HenryEarly
from abydos.phonetic._koelner import Koelner
from abydos.phonetic._lein import LEIN
from abydos.phonetic._meta_soundex import MetaSoundex
from abydos.phonetic._metaphone import Metaphone
from abydos.phonetic._mra import MRA
from abydos.phonetic._norphone import Norphone
from abydos.phonetic._nrl import NRL
from abydos.phonetic._nysiis import NYSIIS
from abydos.phonetic._onca import ONCA
from abydos.phonetic._parmar_kumbharana import ParmarKumbharana
from abydos.phonetic._phonem import Phonem
from abydos.phonetic._phonet import Phonet
from abydos.phonetic._phonetic import _Phonetic
from abydos.phonetic._phonetic_spanish import PhoneticSpanish
from abydos.phonetic._phonex import Phonex
from abydos.phonetic._phonic import PHONIC
from abydos.phonetic._phonix import Phonix
from abydos.phonetic._pshp_soundex_first import PSHPSoundexFirst
from abydos.phonetic._pshp_soundex_last import PSHPSoundexLast
from abydos.phonetic._refined_soundex import RefinedSoundex
from abydos.phonetic._reth_schek import RethSchek
from abydos.phonetic._roger_root import RogerRoot
from abydos.phonetic._russell_index import RussellIndex
from abydos.phonetic._sfinx_bis import SfinxBis
from abydos.phonetic._sound_d import SoundD
from abydos.phonetic._soundex import Soundex
from abydos.phonetic._soundex_br import SoundexBR
from abydos.phonetic._spanish_metaphone import SpanishMetaphone
from abydos.phonetic._spfc import SPFC
from abydos.phonetic._statistics_canada import StatisticsCanada
from abydos.phonetic._waahlin import Waahlin

__all__ = [
    '_Phonetic',
    'RussellIndex',
    'Soundex',
    'RefinedSoundex',
    'DaitchMokotoff',
    'FuzzySoundex',
    'LEIN',
    'Phonex',
    'PHONIC',
    'Phonix',
    'PSHPSoundexFirst',
    'PSHPSoundexLast',
    'NYSIIS',
    'MRA',
    'Caverphone',
    'AlphaSIS',
    'Davidson',
    'Dolby',
    'SPFC',
    'RogerRoot',
    'StatisticsCanada',
    'SoundD',
    'ParmarKumbharana',
    'Metaphone',
    'DoubleMetaphone',
    'Eudex',
    'BeiderMorse',
    'NRL',
    'MetaSoundex',
    'ONCA',
    'FONEM',
    'HenryEarly',
    'Koelner',
    'Haase',
    'RethSchek',
    'Phonem',
    'Phonet',
    'SoundexBR',
    'PhoneticSpanish',
    'SpanishMetaphone',
    'SfinxBis',
    'Waahlin',
    'Norphone',
    'Ainsworth',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
