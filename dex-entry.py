#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display the dex entry for a given pokemon.

Todo:
    Implement clean dex display for PHAT and WHAT displays.
    Implement command line arguments to use as an individual script.
    Port remaining code necessary from display-test.

"""

from typing import List, Tuple


def get_entry(id: int, gen: int, ver: int) -> str:
    """Fetch a pokemon's dex entry.

    Args:
        id:  The national dex id for the pokemon
        gen: The generation for the entry
        ver: The version within generation for the entry

    Returns:
        The dex entry or "flavor" text description for the given pokemon

    Raises:
        DexError: Pokemon doesn't exist or data not in database

    Notes:
        The ver argument is probably not the ideal way to handle the multiple
        entries for each generation but for the time being it may be the best.

    Todo:
        Actually implement this once a database is in place.

    """
    entry = ("For no reason, it jumps and splashes about, making it "
             "easy for predators like Pidgeotto to catch it mid-jump.")
    return entry


def get_data(id: int) -> Tuple[str, str, float, float]:
    """Fetch a pokemon's dex data.

    Args:
        id: The national dex id for the pokemon

    Returns:
        A tuple consisting of:
            Species
            Classification
            Height (Meters)
            Weight (Kilograms)

    Raises:
        DexError: Pokemon doesn't exist or data not in database

    Notes:
        Not sure if there's much reason to keep this separate
        from get_entry, may combine the two later.
        Height and Weight are metric purely because it makes
        it easier to fit the numbers on the small PHAT display.

    Todo:
        As per get_entry, implement once database exists.

    """
    species = "Magikarp"
    classification = "Fish"
    height = 0.9
    weight = 10.0
    return (species, classification, height, weight)


def entry_wrap(entry: str, line_length: int = 17, line_count: int = 7) -> List[str]:
    """Split an entry into separate lines to account for text wrap.

    Args:
        entry:       The entry to be wrapped
        line_length: The maximum length of each line for display
                     Defaults to 17, the maximum on a PHAT using the gscfont
        line_count:  The maximum number of lines for display
                     Defaults to 7, the maximum on a PHAT using the gscfont

    Returns:
        A list of strings, one for each line to be displayed

    Raises:
        DexError: Entry too long to be displayed on one screen given restrictions

    Notes:
        It may be better to find a way to shrink the text to fit longer entries.
        Until that decision is made an error will be raised if the entry won't fit.

    Todo:
        This can probably be written cleaner, look in to it

    """
    words = entry.split(' ')
    line_index = 0
    line_strings = [''] * line_count

    for i in range(len(words)):
        if ((len(line_strings[line_index]) == line_length - 2 and len(words[i]) > 2) or
           (len(line_strings[line_index]) == line_length - 1 and len(words[i]) > 1) or
           (len(line_strings[line_index]) == line_length)):
            line_index += 1
        if len(line_strings[line_index]) + len(words[i]) <= line_length:
            line_strings[line_index] += words[i]
            if len(line_strings[line_index]) < line_length:
                line_strings[line_index] += ' '
        else:
            wrap_index = line_length - len(line_strings[line_index])
            line_strings[line_index] += words[i][:wrap_index] + '-'
            line_index += 1
            line_strings[line_index] += words[i][wrap_index:] + ' '
    return line_strings
