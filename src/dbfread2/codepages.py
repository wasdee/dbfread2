"""Codepage mapping and encoding utilities for DBF files.

This module provides mapping between DBF language driver codes and their corresponding
encodings, along with utilities to determine the appropriate text encoding.
"""


# Table from dbf.py by Ethan Furman
# Maps DBF language driver codes to (encoding, description) tuples
codepages: dict[int, tuple[str, str]] = {
    0x00: ('ascii', "plain ol' ascii"),
    0x01: ('cp437', 'U.S. MS-DOS'),
    0x02: ('cp850', 'International MS-DOS'),
    0x03: ('cp1252', 'Windows ANSI'),
    0x04: ('mac_roman', 'Standard Macintosh'),
    0x08: ('cp865', 'Danish OEM'),
    0x09: ('cp437', 'Dutch OEM'),
    0x0A: ('cp850', 'Dutch OEM (secondary)'),
    0x0B: ('cp437', 'Finnish OEM'),
    0x0D: ('cp437', 'French OEM'),
    0x0E: ('cp850', 'French OEM (secondary)'),
    0x0F: ('cp437', 'German OEM'),
    0x10: ('cp850', 'German OEM (secondary)'),
    0x11: ('cp437', 'Italian OEM'),
    0x12: ('cp850', 'Italian OEM (secondary)'),
    0x13: ('cp932', 'Japanese Shift-JIS'),
    0x14: ('cp850', 'Spanish OEM (secondary)'),
    0x15: ('cp437', 'Swedish OEM'),
    0x16: ('cp850', 'Swedish OEM (secondary)'),
    0x17: ('cp865', 'Norwegian OEM'),
    0x18: ('cp437', 'Spanish OEM'),
    0x19: ('cp437', 'English OEM (Britain)'),
    0x1A: ('cp850', 'English OEM (Britain) (secondary)'),
    0x1B: ('cp437', 'English OEM (U.S.)'),
    0x1C: ('cp863', 'French OEM (Canada)'),
    0x1D: ('cp850', 'French OEM (secondary)'),
    0x1F: ('cp852', 'Czech OEM'),
    0x22: ('cp852', 'Hungarian OEM'),
    0x23: ('cp852', 'Polish OEM'),
    0x24: ('cp860', 'Portuguese OEM'),
    0x25: ('cp850', 'Portuguese OEM (secondary)'),
    0x26: ('cp866', 'Russian OEM'),
    0x37: ('cp850', 'English OEM (U.S.) (secondary)'),
    0x40: ('cp852', 'Romanian OEM'),
    0x4D: ('cp936', 'Chinese GBK (PRC)'),
    0x4E: ('cp949', 'Korean (ANSI/OEM)'),
    0x4F: ('cp950', 'Chinese Big 5 (Taiwan)'),
    0x50: ('cp874', 'Thai (ANSI/OEM)'),
    0x57: ('cp1252', 'ANSI'),
    0x58: ('cp1252', 'Western European ANSI'),
    0x59: ('cp1252', 'Spanish ANSI'),
    0x64: ('cp852', 'Eastern European MS-DOS'),
    0x65: ('cp866', 'Russian MS-DOS'),
    0x66: ('cp865', 'Nordic MS-DOS'),
    0x67: ('cp861', 'Icelandic MS-DOS'),
    # 0x68: (None, 'Kamenicky (Czech) MS-DOS'),
    # 0x69: (None, 'Mazovia (Polish) MS-DOS'),
    0x6a: ('cp737', 'Greek MS-DOS (437G)'),
    0x6b: ('cp857', 'Turkish MS-DOS'),
    0x78: ('cp950', 'Traditional Chinese '
                    '(Hong Kong SAR, Taiwan) Windows'),
    0x79: ('cp949', 'Korean Windows'),
    0x7a: ('cp936', 'Chinese Simplified (PRC, Singapore) Windows'),
    0x7b: ('cp932', 'Japanese Windows'),
    0x7c: ('cp874', 'Thai Windows'),
    0x7d: ('cp1255', 'Hebrew Windows'),
    0x7e: ('cp1256', 'Arabic Windows'),
    0xc8: ('cp1250', 'Eastern European Windows'),
    0xc9: ('cp1251', 'Russian Windows'),
    0xca: ('cp1254', 'Turkish Windows'),
    0xcb: ('cp1253', 'Greek Windows'),
    0x96: ('mac_cyrillic', 'Russian Macintosh'),
    0x97: ('mac_latin2', 'Macintosh EE'),
    0x98: ('mac_greek', 'Greek Macintosh'),
}


def guess_encoding(language_driver: int) -> str:
    """Determine the text encoding based on the DBF language driver code.

    Args:
        language_driver: The language driver byte from the DBF header.

    Returns:
        str: The Python encoding name (e.g. 'cp437', 'utf-8').

    Raises:
        LookupError: If the language driver code is not recognized.
    """
    try:
        return codepages[language_driver][0]
    except KeyError:
        raise LookupError(
            f'Unknown language driver code: 0x{language_driver:02x}'
        ) from None
