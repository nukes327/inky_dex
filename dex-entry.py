#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display the dex entry for a given pokemon on an inky display.

Todo:
    Implement clean dex display for PHAT and WHAT displays.
    Implement command line arguments to use as an individual script.
    Port remaining code necessary from display-test.

"""

from typing import List, Tuple
from PIL import Image  # type: ignore


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


def gsc_format(entry: str) -> str:
    """Replace character patterns with unique characters to work with gscfont.

    Args:
        entry: The entry to be formatted

    Returns:
        A string with character replacements performed

    Notes:
        The gscfont file contains special characters that exist as one of the following:
            Combination character with apostrophe and character sharing same char slot
            Symbol
            Combined letters for special use

        If using gscfont this replacement process should be done before wrapping the entry

    Todo:
        There may be a better way to handle this than using special characters, look in to it
        Notate somewhere which special characters are used for what character on the sheet
        Clean up replacements

    """
    partial = entry.replace("'d", 'ⓓ').replace("'l", 'ⓛ').replace("'m", 'ⓜ').replace("'r", 'ⓡ')
    finished = partial.replace("'s", 'ⓢ').replace("'t", 'ⓣ').replace("'v", 'ⓥ')
    return finished


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


def create_mask(source: Image, mask: Tuple[int, int, int] = (0, 1, 2)) -> Image:
    """Create an image mask for pasting purposes.

    Args:
        source: Image to create the mask from
        mask:   Tuple containing colormap indices to be masked

                Default values are equivalent to white, black, and red
                for an inky display

    Returns:
        An image mask for the source image

    Attribution:
        This method was written by the folks at pimoroni, and can be found within
        their examples for their inky displays.

    """
    mask_image = Image.new('1', source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image


def display_char(img: Image, font: Image, x: int, y: int,
                 character: str, char_width: int = 8, char_height: int = 8) -> None:
    """Paste a single character from a fontsheet to the display image.

    Args:
        img:         The display image to be pasted into
        font:        The fontsheet image
        x:           X coordinate to paste character
        y:           Y coordinate to paste character
        character:   Character to be pasted
        char_width:  Width of each character on the fontsheet
                     Default of 8 is the gscfont char width
        char_height: Height of each character on the fontsheet
                     Default of 8 is the gscfont char height

    Notes:
        X and Y coordinates are anchored to the top left pixel of the character,
        and 0,0 is the top left of the display

    Todo:
        The sheet variable is used to determine fontsheet location for each
        character, the issue being that it's hardcoded for the gscfont fontsheet.
        This should be fixed to be usable for any dimension of fontsheet, either
        by adding another method argument, or planning some more clever way.

        The magic number 16 when determining the sheet x and y is also hardcoded
        based on the character width of the gscfont file. This should also be
        fixed to be more versatile.

    """
    sheet = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyz      "
             "ÄÖÜäöü          ⓓⓛⓜⓡⓢⓣⓥ       ⓃⓄ'①②-  ?!.&é ▷▶▼♂$×./,♀0123456789")
    sheet_x = (sheet.index(character) % 16) * char_width
    sheet_y = (int(sheet.index(character) / 16)) * char_height

    char_sprite = font.crop((sheet_x, sheet_y, sheet_x + char_width, sheet_y + char_height))
    img.paste(char_sprite, (x, y), create_mask(char_sprite))


def display_line(img: Image, font: Image, x: int, y: int,
                 line: str, char_width: int = 8, char_height: int = 8) -> None:
    """Paste an entire line into a display image using characters from a fontsheet.

    Args:
        img:         The display image to be pasted into
        font:        The fontsheet image
        x:           X coordinate to paste line
        y:           Y coordinate to paste line
        line:        Line to be pasted
        char_width:  Width of each character on the fontsheet
                     Default of 8 is the gscfont char width
        char_height: Height of each character on the fontsheet
                     Default of 8 is the gscfont char height

    Notes:
        X and Y coordinates are anchored to the top left pixel of the
        first character of the line, 0,0 is the top left of the display

    """
    for character, index in zip(line, range(len(line))):
        display_char(img, font, x + char_width * index, y, character, char_width, char_height)


def display_lines(img: Image, font: Image, x: int, y: int, lines: List[str],
                  char_width: int = 8, char_height: int = 8, line_gap: int = 4) -> None:
    """Paste multiple lines into a display image using characters from a fontsheet.

    Args:
        img:         The display image to be pasted into
        font:        The fontsheet image
        x:           X coordinate to paste lines
        y:           Y coordinate to paste lines
        lines:       List of lines to be pasted
        char_width:  Width of each character on the fontsheet
                     Default of 8 is the gscfont char width
        char_height: Height of each character on the fontsheet
                     Default of 8 is the gscfont char height
        line_gap:    Distance in pixels to separate each line

    Notes:
        X and Y coordinates are anchored to the top left pixel of the first
        character of the first line, 0,0 is the top left of the display.

        The lines are left aligned to the X coordinate

    """
    for line, index in zip(lines, range(len(lines))):
        display_line(img, font, x, y + index * (char_height + line_gap), line, char_width, char_height)
