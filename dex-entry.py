#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Display the dex entry for a given pokemon on an inky display.

Todo:
    Implement clean dex display for PHAT and WHAT displays.
    Implement command line arguments to use as an individual script.
    Port remaining code necessary from display-test.
    The textual output to the display probably needs to be refactored to account for more variables
        - in progress
    Formatter class or module for building pasteable strings, floats?

"""

from typing import List, Tuple
from PIL import Image, ImageDraw  # type: ignore
from PIL.ImagePalette import ImagePalette  # type: ignore
from dex.font import Font
from dex.poke import Pokemon
import logging


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
    entry = (
        "For no reason, it jumps and splashes about, making it "
        "easy for predators like Pidgeotto to catch it mid-jump."
    )
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
    partial = entry.replace("'d", "ⓓ").replace("'l", "ⓛ").replace("'m", "ⓜ").replace("'r", "ⓡ")
    finished = partial.replace("'s", "ⓢ").replace("'t", "ⓣ").replace("'v", "ⓥ")
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
    words = entry.split(" ")
    line_index = 0
    line_strings = [""] * line_count

    for i in range(len(words)):
        if (
            (len(line_strings[line_index]) == line_length - 2 and len(words[i]) > 2)
            or (len(line_strings[line_index]) == line_length - 1 and len(words[i]) > 1)
            or (len(line_strings[line_index]) == line_length)
        ):
            line_index += 1
        if len(line_strings[line_index]) + len(words[i]) <= line_length:
            line_strings[line_index] += words[i]
            if len(line_strings[line_index]) < line_length:
                line_strings[line_index] += " "
        else:
            wrap_index = line_length - len(line_strings[line_index])
            line_strings[line_index] += words[i][:wrap_index] + "-"
            line_index += 1
            line_strings[line_index] += words[i][wrap_index:] + " "
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
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image


def display_char(img: Image, font: Font, location: Tuple[int, int], character: str) -> None:
    """Paste a single character from a fontsheet to the display image.

    Args:
        img:         The display image to be pasted into
        font:        The font class in use
        location:    (x, y) location tuple to paste character
        character:   Character to be pasted

    Notes:
        X and Y coordinates are anchored to the top left pixel of the character,
        and 0,0 is the top left of the display

    """
    # sheet = font.sheetstring
    # (
    #     "ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyz      "
    #     "ÄÖÜäöü          ⓓⓛⓜⓡⓢⓣⓥ       ⓃⓄ'①②-  ?!.&é ▷▶▼♂$×./,♀0123456789"
    # )
    # sheet_x = (sheet.index(character) % font.sheetwidth) * font.charwidth
    # sheet_y = (int(sheet.index(character) / font.sheetwidth)) * font.charheight

    # char_sprite = font.crop((sheet_x, sheet_y, sheet_x + char_width, sheet_y + char_height))
    char_sprite = font.get_character(character)
    img.paste(char_sprite, location, create_mask(char_sprite))


def display_line(img: Image, font: Font, location: Tuple[int, int], line: str) -> None:
    """Paste an entire line into a display image using characters from a fontsheet.

    Args:
        img:         The display image to be pasted into
        font:        The font class
        location:    (x, y) location tuple to paste character
        line:        Line to be pasted

    Notes:
        X and Y coordinates are anchored to the top left pixel of the
        first character of the line, 0,0 is the top left of the display

    """
    for character, index in zip(line, range(len(line))):
        display_char(img, font, (location[0] + font.charwidth * index, location[1]), character)


def display_lines(img: Image, font: Font, location: Tuple[int, int], lines: List[str], line_gap: int = 4) -> None:
    """Paste multiple lines into a display image using characters from a fontsheet.

    Args:
        img:         The display image to be pasted into
        font:        The font class
        location:    (x, y) location tuple to paste character
        lines:       List of lines to be pasted
        line_gap:    Distance in pixels to separate each line

    Notes:
        X and Y coordinates are anchored to the top left pixel of the first
        character of the first line, 0,0 is the top left of the display.

        The lines are left aligned to the X coordinate

    """
    for line, index in zip(lines, range(len(lines))):
        display_line(img, font, (location[0], location[1] + index * (font.charheight + line_gap)), line)


def display_sprite(img: Image, location: Tuple[int, int], id: int, gen: int, ver: int, form: int = 0) -> None:
    """Paste sprite and bounding box into display image.

    Args:
        img:      The display image to be pasted into
        location: (x, y) location tuple to paste character
        id:       Id of the pokemon sprite to paste
        gen:      Generation to pull sprite from
        ver:      Version within generation to pull sprite from
        form:     Choose form if pokemon has more than one

    Notes:
        X and Y coordinates are anchored to the top left of the bounding box
        for the sprite, 0,0 is the top left of the display.

    Todo:
        Sprites are currently stored using sprites from gen 2, but without
        an indicator by filename to indicate generation. I think the best
        solution may be to make each sprite file a full sheet, with gen 1 left
        aligned. This will require shifting all of the sprites over 56 pixels
        as they are gen 2, but it would help expansion in the future if done now.

    """
    box = Image.open("assets/ui/spritebox.png")
    sprite_sheet = Image.open("assets/sprites/{:03d}.png".format(id))

    # TODO: Put this next line in a try/except or get index errors for high gens
    sprite = sprite_sheet.crop((0, 56 * ver, 56, 56 + 56 * ver))

    img.paste(box, location, create_mask(box))
    img.paste(sprite, tuple(n + 6 for n in location), create_mask(sprite))


def display_footprint(img: Image, location: Tuple[int, int], id: int) -> None:
    """Paste footprint sprite into display image.

    Args:
        img:      The display image to be pasted into
        location: (x, y) location tuple to paste character
        id:       Id of the pokemon footprint to paste

    Notes:
        X and Y coordinates are anchored to the top left of the footprint
        sprite area, 0,0 is the top left of the display.

    """
    sprite_sheet = Image.open("assets/sprites/{:03d}.png".format(id))
    footprint = sprite_sheet.crop((0, 112, 16, 128))
    img.paste(footprint, location, create_mask(footprint))


def display_numeric(img: Image, font: Font, location: Tuple[int, int], width: int, mon: Pokemon) -> None:
    """Paste numeric data into display image.

    Args:
        img:      Display image to be pasted into
        font:     Fontsheet image
        location: (x, y) location tuple to paste character
        width:    How wide the section should be
        data:     Numeric data to be pasted
                  Tuple with data in the following order:
                    ID
                    Height
                    Weight

    Notes:
        X and Y coordinates are the top left of the ID line for numeric data
        0,0 is the top left of the display
        Too many digits in height or weight for given width may cause issues

    Todo:
        Still contains some magic numbers, should work on this
        Refactor to support more input variables

    """
    draw = ImageDraw.Draw(img)
    underline = 2  # Third color on a three color inky display
    x = location[0]
    y = location[1]
    ly = y
    right_bound = x + width

    # ID section
    display_line(img, font, (x, ly), "ⓃⓄ")
    display_line(img, font, (right_bound - (3 * 8), ly), "{0:03d}".format(mon.id))
    draw.line((x, ly + 8, right_bound - 2, ly + 8), underline)

    # Height section
    ly += 8 + 4
    display_line(img, font, (x, ly), "HT")
    display_char(img, font, (right_bound - 8, ly), "m")
    display_char(img, font, (int(right_bound - 2.75 * 8), ly), ".")
    display_line(img, font, (int(right_bound - 4.5 * 8), ly), "{: >2s}".format(str(mon.height).split(".")[0]))
    display_line(img, font, (int(right_bound - 2.125 * 8), ly), str(mon.height).split(".")[1])
    draw.line((x, ly + 8, right_bound - 2, ly + 8), underline)

    # Weight section
    ly += 8 + 4
    display_line(img, font, (x, ly), "WT")
    display_char(img, font, (right_bound - 2 * 8 + 1, ly), "k")
    display_char(img, font, (right_bound - 8, ly), "g")
    display_char(img, font, (int(right_bound - 3.5 * 8), ly), ".")
    display_line(img, font, (int(right_bound - 6.25 * 8), ly), "{: >3s}".format(str(mon.weight).split(".")[0]))
    display_line(img, font, (int(right_bound - 2.875 * 8), ly), str(mon.weight).split(".")[1])
    draw.line((x, ly + 8, right_bound - 2, ly + 8), underline)


if __name__ == "__main__":
    try:
        from inky import InkyPHAT  # type: ignore
    except (ModuleNotFoundError, RuntimeError):
        print("Inky library absent, will not display to e-ink")
        print("Setting image size to PHAT")
        img = Image.new("P", (212, 104))
        en_inky = False
    else:
        en_inky = True
        inky_display = InkyPHAT("yellow")
        inky_display.set_border(inky_display.BLACK)
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

    id = 129

    mon = Pokemon(129)

    # entry = get_entry(id, 2, 0)
    # data = get_data(id)
    font = Font("assets/ui/gscfont.png")

    display_sprite(img, (1, 1), id, 2, 0)
    display_numeric(img, font, (2, 69), 67, mon)

    img = img.rotate(180)
    if en_inky:
        inky_display.set_image(img)
        inky_display.show()
    palette = ImagePalette(palette=[255, 255, 255, 0, 0, 0, 255, 0, 0], size=9)
    img.putpalette(palette.tostring())
    img = img.rotate(180)
    img.save("last_display.png")
