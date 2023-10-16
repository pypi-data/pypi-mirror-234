#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
https://www.compart.com/en/unicode/block

Author  huang22
Date    ：2023/9/28 16:27
"""
from enum import Enum, EnumMeta

UNICODE_BLOCKS = {
    "Basic Latin": ("0000", "007F"),
    "Latin-1 Supplement": ("0080", "00FF"),
    "Latin Extended-A": ("0100", "017F"),
    "Latin Extended-B": ("0180", "024F"),
    "IPA Extensions": ("0250", "02AF"),
    "Spacing Modifier Letters": ("02B0", "02FF"),
    "Combining Diacritical Marks": ("0300", "036F"),
    "Greek and Coptic": ("0370", "03FF"),
    "Cyrillic": ("0400", "04FF"),
    "Cyrillic Supplement": ("0500", "052F"),
    "Armenian": ("0530", "058F"),
    "Hebrew": ("0590", "05FF"),
    "Arabic": ("0600", "06FF"),
    "Syriac": ("0700", "074F"),
    "Arabic Supplement": ("0750", "077F"),
    "Thaana": ("0780", "07BF"),
    "NKo": ("07C0", "07FF"),
    "Samaritan": ("0800", "083F"),
    "Mandaic": ("0840", "085F"),
    "Syriac Supplement": ("0860", "086F"),
    "Arabic Extended-A": ("08A0", "08FF"),
    "Devanagari": ("0900", "097F"),
    "Bengali": ("0980", "09FF"),
    "Gurmukhi": ("0A00", "0A7F"),
    "Gujarati": ("0A80", "0AFF"),
    "Oriya": ("0B00", "0B7F"),
    "Tamil": ("0B80", "0BFF"),
    "Telugu": ("0C00", "0C7F"),
    "Kannada": ("0C80", "0CFF"),
    "Malayalam": ("0D00", "0D7F"),
    "Sinhala": ("0D80", "0DFF"),
    "Thai": ("0E00", "0E7F"),
    "Lao": ("0E80", "0EFF"),
    "Tibetan": ("0F00", "0FFF"),
    "Myanmar": ("1000", "109F"),
    "Georgian": ("10A0", "10FF"),
    "Hangul Jamo": ("1100", "11FF"),
    "Ethiopic": ("1200", "137F"),
    "Ethiopic Supplement": ("1380", "139F"),
    "Cherokee": ("13A0", "13FF"),
    "Unified Canadian Aboriginal Syllabics": ("1400", "167F"),
    "Ogham": ("1680", "169F"),
    "Runic": ("16A0", "16FF"),
    "Tagalog": ("1700", "171F"),
    "Hanunoo": ("1720", "173F"),
    "Buhid": ("1740", "175F"),
    "Tagbanwa": ("1760", "177F"),
    "Khmer": ("1780", "17FF"),
    "Mongolian": ("1800", "18AF"),
    "Unified Canadian Aboriginal Syllabics Extended": ("18B0", "18FF"),
    "Limbu": ("1900", "194F"),
    "Tai Le": ("1950", "197F"),
    "New Tai Lue": ("1980", "19DF"),
    "Khmer Symbols": ("19E0", "19FF"),
    "Buginese": ("1A00", "1A1F"),
    "Tai Tham": ("1A20", "1AAF"),
    "Combining Diacritical Marks Extended": ("1AB0", "1AFF"),
    "Balinese": ("1B00", "1B7F"),
    "Sundanese": ("1B80", "1BBF"),
    "Batak": ("1BC0", "1BFF"),
    "Lepcha": ("1C00", "1C4F"),
    "Ol Chiki": ("1C50", "1C7F"),
    "Cyrillic Extended-C": ("1C80", "1C8F"),
    "Georgian Extended": ("1C90", "1CBF"),
    "Sundanese Supplement": ("1CC0", "1CCF"),
    "Vedic Extensions": ("1CD0", "1CFF"),
    "Phonetic Extensions": ("1D00", "1D7F"),
    "Phonetic Extensions Supplement": ("1D80", "1DBF"),
    "Combining Diacritical Marks Supplement": ("1DC0", "1DFF"),
    "Latin Extended Additional": ("1E00", "1EFF"),
    "Greek Extended": ("1F00", "1FFF"),
    "General Punctuation": ("2000", "206F"),
    "Superscripts and Subscripts": ("2070", "209F"),
    "Currency Symbols": ("20A0", "20CF"),
    "Combining Diacritical Marks for Symbols": ("20D0", "20FF"),
    "Letterlike Symbols": ("2100", "214F"),
    "Number Forms": ("2150", "218F"),
    "Arrows": ("2190", "21FF"),
    "Mathematical Operators": ("2200", "22FF"),
    "Miscellaneous Technical": ("2300", "23FF"),
    "Control Pictures": ("2400", "243F"),
    "Optical Character Recognition": ("2440", "245F"),
    "Enclosed Alphanumerics": ("2460", "24FF"),
    "Box Drawing": ("2500", "257F"),
    "Block Elements": ("2580", "259F"),
    "Geometric Shapes": ("25A0", "25FF"),
    "Miscellaneous Symbols": ("2600", "26FF"),
    "Dingbats": ("2700", "27BF"),
    "Miscellaneous Mathematical Symbols-A": ("27C0", "27EF"),
    "Supplemental Arrows-A": ("27F0", "27FF"),
    "Braille Patterns": ("2800", "28FF"),
    "Supplemental Arrows-B": ("2900", "297F"),
    "Miscellaneous Mathematical Symbols-B": ("2980", "29FF"),
    "Supplemental Mathematical Operators": ("2A00", "2AFF"),
    "Miscellaneous Symbols and Arrows": ("2B00", "2BFF"),
    "Glagolitic": ("2C00", "2C5F"),
    "Latin Extended-C": ("2C60", "2C7F"),
    "Coptic": ("2C80", "2CFF"),
    "Georgian Supplement": ("2D00", "2D2F"),
    "Tifinagh": ("2D30", "2D7F"),
    "Ethiopic Extended": ("2D80", "2DDF"),
    "Cyrillic Extended-A": ("2DE0", "2DFF"),
    "Supplemental Punctuation": ("2E00", "2E7F"),
    "CJK Radicals Supplement": ("2E80", "2EFF"),
    "Kangxi Radicals": ("2F00", "2FDF"),
    "Ideographic Description Characters": ("2FF0", "2FFF"),
    "CJK Symbols and Punctuation": ("3000", "303F"),
    "Hiragana": ("3040", "309F"),
    "Katakana": ("30A0", "30FF"),
    "Bopomofo": ("3100", "312F"),
    "Hangul Compatibility Jamo": ("3130", "318F"),
    "Kanbun": ("3190", "319F"),
    "Bopomofo Extended": ("31A0", "31BF"),
    "CJK Strokes": ("31C0", "31EF"),
    "Katakana Phonetic Extensions": ("31F0", "31FF"),
    "Enclosed CJK Letters and Months": ("3200", "32FF"),
    "CJK Compatibility": ("3300", "33FF"),
    "CJK Unified Ideographs Extension A": ("3400", "4DBF"),
    "Yijing Hexagram Symbols": ("4DC0", "4DFF"),
    "CJK Unified Ideographs": ("4E00", "9FFF"),
    "Yi Syllables": ("A000", "A48F"),
    "Yi Radicals": ("A490", "A4CF"),
    "Lisu": ("A4D0", "A4FF"),
    "Vai": ("A500", "A63F"),
    "Cyrillic Extended-B": ("A640", "A69F"),
    "Bamum": ("A6A0", "A6FF"),
    "Modifier Tone Letters": ("A700", "A71F"),
    "Latin Extended-D": ("A720", "A7FF"),
    "Syloti Nagri": ("A800", "A82F"),
    "Common Indic Number Forms": ("A830", "A83F"),
    "Phags-pa": ("A840", "A87F"),
    "Saurashtra": ("A880", "A8DF"),
    "Devanagari Extended": ("A8E0", "A8FF"),
    "Kayah Li": ("A900", "A92F"),
    "Rejang": ("A930", "A95F"),
    "Hangul Jamo Extended-A": ("A960", "A97F"),
    "Javanese": ("A980", "A9DF"),
    "Myanmar Extended-B": ("A9E0", "A9FF"),
    "Cham": ("AA00", "AA5F"),
    "Myanmar Extended-A": ("AA60", "AA7F"),
    "Tai Viet": ("AA80", "AADF"),
    "Meetei Mayek Extensions": ("AAE0", "AAFF"),
    "Ethiopic Extended-A": ("AB00", "AB2F"),
    "Latin Extended-E": ("AB30", "AB6F"),
    "Cherokee Supplement": ("AB70", "ABBF"),
    "Meetei Mayek": ("ABC0", "ABFF"),
    "Hangul Syllables": ("AC00", "D7AF"),
    "Hangul Jamo Extended-B": ("D7B0", "D7FF"),
    "High Surrogates": ("D800", "DB7F"),
    "High Private Use Surrogates": ("DB80", "DBFF"),
    "Low Surrogates": ("DC00", "DFFF"),
    "Private Use Area": ("E000", "F8FF"),
    "CJK Compatibility Ideographs": ("F900", "FAFF"),
    "Alphabetic Presentation Forms": ("FB00", "FB4F"),
    "Arabic Presentation Forms-A": ("FB50", "FDFF"),
    "Variation Selectors": ("FE00", "FE0F"),
    "Vertical Forms": ("FE10", "FE1F"),
    "Combining Half Marks": ("FE20", "FE2F"),
    "CJK Compatibility Forms": ("FE30", "FE4F"),
    "Small Form Variants": ("FE50", "FE6F"),
    "Arabic Presentation Forms-B": ("FE70", "FEFF"),
    "Halfwidth and Fullwidth Forms": ("FF00", "FFEF"),
    "Specials": ("FFF0", "FFFF"),
    "Linear B Syllabary": ("10000", "1007F"),
    "Linear B Ideograms": ("10080", "100FF"),
    "Aegean Numbers": ("10100", "1013F"),
    "Ancient Greek Numbers": ("10140", "1018F"),
    "Ancient Symbols": ("10190", "101CF"),
    "Phaistos Disc": ("101D0", "101FF"),
    "Lycian": ("10280", "1029F"),
    "Carian": ("102A0", "102DF"),
    "Coptic Epact Numbers": ("102E0", "102FF"),
    "Old Italic": ("10300", "1032F"),
    "Gothic": ("10330", "1034F"),
    "Old Permic": ("10350", "1037F"),
    "Ugaritic": ("10380", "1039F"),
    "Old Persian": ("103A0", "103DF"),
    "Deseret": ("10400", "1044F"),
    "Shavian": ("10450", "1047F"),
    "Osmanya": ("10480", "104AF"),
    "Osage": ("104B0", "104FF"),
    "Elbasan": ("10500", "1052F"),
    "Caucasian Albanian": ("10530", "1056F"),
    "Linear A": ("10600", "1077F"),
    "Cypriot Syllabary": ("10800", "1083F"),
    "Imperial Aramaic": ("10840", "1085F"),
    "Palmyrene": ("10860", "1087F"),
    "Nabataean": ("10880", "108AF"),
    "Hatran": ("108E0", "108FF"),
    "Phoenician": ("10900", "1091F"),
    "Lydian": ("10920", "1093F"),
    "Meroitic Hieroglyphs": ("10980", "1099F"),
    "Meroitic Cursive": ("109A0", "109FF"),
    "Kharoshthi": ("10A00", "10A5F"),
    "Old South Arabian": ("10A60", "10A7F"),
    "Old North Arabian": ("10A80", "10A9F"),
    "Manichaean": ("10AC0", "10AFF"),
    "Avestan": ("10B00", "10B3F"),
    "Inscriptional Parthian": ("10B40", "10B5F"),
    "Inscriptional Pahlavi": ("10B60", "10B7F"),
    "Psalter Pahlavi": ("10B80", "10BAF"),
    "Old Turkic": ("10C00", "10C4F"),
    "Old Hungarian": ("10C80", "10CFF"),
    "Hanifi Rohingya": ("10D00", "10D3F"),
    "Rumi Numeral Symbols": ("10E60", "10E7F"),
    "Yezidi": ("10E80", "10EBF"),
    "Old Sogdian": ("10F00", "10F2F"),
    "Sogdian": ("10F30", "10F6F"),
    "Chorasmian": ("10FB0", "10FDF"),
    "Elymaic": ("10FE0", "10FFF"),
    "Brahmi": ("11000", "1107F"),
    "Kaithi": ("11080", "110CF"),
    "Sora Sompeng": ("110D0", "110FF"),
    "Chakma": ("11100", "1114F"),
    "Mahajani": ("11150", "1117F"),
    "Sharada": ("11180", "111DF"),
    "Sinhala Archaic Numbers": ("111E0", "111FF"),
    "Khojki": ("11200", "1124F"),
    "Multani": ("11280", "112AF"),
    "Khudawadi": ("112B0", "112FF"),
    "Grantha": ("11300", "1137F"),
    "Newa": ("11400", "1147F"),
    "Tirhuta": ("11480", "114DF"),
    "Siddham": ("11580", "115FF"),
    "Modi": ("11600", "1165F"),
    "Mongolian Supplement": ("11660", "1167F"),
    "Takri": ("11680", "116CF"),
    "Ahom": ("11700", "1173F"),
    "Dogra": ("11800", "1184F"),
    "Warang Citi": ("118A0", "118FF"),
    "Dives Akuru": ("11900", "1195F"),
    "Nandinagari": ("119A0", "119FF"),
    "Zanabazar Square": ("11A00", "11A4F"),
    "Soyombo": ("11A50", "11AAF"),
    "Pau Cin Hau": ("11AC0", "11AFF"),
    "Bhaiksuki": ("11C00", "11C6F"),
    "Marchen": ("11C70", "11CBF"),
    "Masaram Gondi": ("11D00", "11D5F"),
    "Gunjala Gondi": ("11D60", "11DAF"),
    "Makasar": ("11EE0", "11EFF"),
    "Lisu Supplement": ("11FB0", "11FBF"),
    "Tamil Supplement": ("11FC0", "11FFF"),
    "Cuneiform": ("12000", "123FF"),
    "Cuneiform Numbers and Punctuation": ("12400", "1247F"),
    "Early Dynastic Cuneiform": ("12480", "1254F"),
    "Egyptian Hieroglyphs": ("13000", "1342F"),
    "Egyptian Hieroglyph Format Controls": ("13430", "1343F"),
    "Anatolian Hieroglyphs": ("14400", "1467F"),
    "Bamum Supplement": ("16800", "16A3F"),
    "Mro": ("16A40", "16A6F"),
    "Bassa Vah": ("16AD0", "16AFF"),
    "Pahawh Hmong": ("16B00", "16B8F"),
    "Medefaidrin": ("16E40", "16E9F"),
    "Miao": ("16F00", "16F9F"),
    "Ideographic Symbols and Punctuation": ("16FE0", "16FFF"),
    "Tangut": ("17000", "187FF"),
    "Tangut Components": ("18800", "18AFF"),
    "Khitan Small Script": ("18B00", "18CFF"),
    "Tangut Supplement": ("18D00", "18D8F"),
    "Kana Supplement": ("1B000", "1B0FF"),
    "Kana Extended-A": ("1B100", "1B12F"),
    "Small Kana Extension": ("1B130", "1B16F"),
    "Nushu": ("1B170", "1B2FF"),
    "Duployan": ("1BC00", "1BC9F"),
    "Shorthand Format Controls": ("1BCA0", "1BCAF"),
    "Byzantine Musical Symbols": ("1D000", "1D0FF"),
    "Musical Symbols": ("1D100", "1D1FF"),
    "Ancient Greek Musical Notation": ("1D200", "1D24F"),
    "Mayan Numerals": ("1D2E0", "1D2FF"),
    "Tai Xuan Jing Symbols": ("1D300", "1D35F"),
    "Counting Rod Numerals": ("1D360", "1D37F"),
    "Mathematical Alphanumeric Symbols": ("1D400", "1D7FF"),
    "Sutton SignWriting": ("1D800", "1DAAF"),
    "Glagolitic Supplement": ("1E000", "1E02F"),
    "Nyiakeng Puachue Hmong": ("1E100", "1E14F"),
    "Wancho": ("1E2C0", "1E2FF"),
    "Mende Kikakui": ("1E800", "1E8DF"),
    "Adlam": ("1E900", "1E95F"),
    "Indic Siyaq Numbers": ("1EC70", "1ECBF"),
    "Ottoman Siyaq Numbers": ("1ED00", "1ED4F"),
    "Arabic Mathematical Alphabetic Symbols": ("1EE00", "1EEFF"),
    "Mahjong Tiles": ("1F000", "1F02F"),
    "Domino Tiles": ("1F030", "1F09F"),
    "Playing Cards": ("1F0A0", "1F0FF"),
    "Enclosed Alphanumeric Supplement": ("1F100", "1F1FF"),
    "Enclosed Ideographic Supplement": ("1F200", "1F2FF"),
    "Miscellaneous Symbols and Pictographs": ("1F300", "1F5FF"),
    "Emoticons": ("1F600", "1F64F"),
    "Ornamental Dingbats": ("1F650", "1F67F"),
    "Transport and Map Symbols": ("1F680", "1F6FF"),
    "Alchemical Symbols": ("1F700", "1F77F"),
    "Geometric Shapes Extended": ("1F780", "1F7FF"),
    "Supplemental Arrows-C": ("1F800", "1F8FF"),
    "Supplemental Symbols and Pictographs": ("1F900", "1F9FF"),
    "Chess Symbols": ("1FA00", "1FA6F"),
    "Symbols and Pictographs Extended-A": ("1FA70", "1FAFF"),
    "Symbols for Legacy Computing": ("1FB00", "1FBFF"),
    "CJK Unified Ideographs Extension B": ("20000", "2A6DF"),
    "CJK Unified Ideographs Extension C": ("2A700", "2B73F"),
    "CJK Unified Ideographs Extension D": ("2B740", "2B81F"),
    "CJK Unified Ideographs Extension E": ("2B820", "2CEAF"),
    "CJK Unified Ideographs Extension F": ("2CEB0", "2EBEF"),
    "CJK Compatibility Ideographs Supplement": ("2F800", "2FA1F"),
    "CJK Unified Ideographs Extension G": ("30000", "3134F"),
    "Tags": ("E0000", "E007F"),
    "Variation Selectors Supplement": ("E0100", "E01EF"),
    "Supplementary Private Use Area-A": ("F0000", "FFFFF"),
    "Supplementary Private Use Area-B": ("100000", "10FFFF"),
}


class EnumChrMeta(EnumMeta):
    def __getattribute__(cls, item):
        value = super().__getattribute__(item)

        if isinstance(value, cls):
            value = value.chrs

        return value


class UnicodeBlocks(Enum, metaclass=EnumChrMeta):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.chrs = [chr(i) for i in range(int(begin, base=16), int(end, base=16) + 1)]

    BasicLatin = UNICODE_BLOCKS["Basic Latin"]
    Latin1Supplement = UNICODE_BLOCKS["Latin-1 Supplement"]
    LatinExtendedA = UNICODE_BLOCKS["Latin Extended-A"]
    LatinExtendedB = UNICODE_BLOCKS["Latin Extended-B"]
    IPAExtensions = UNICODE_BLOCKS["IPA Extensions"]
    SpacingModifierLetters = UNICODE_BLOCKS["Spacing Modifier Letters"]
    CombiningDiacriticalMarks = UNICODE_BLOCKS["Combining Diacritical Marks"]
    GreekandCoptic = UNICODE_BLOCKS["Greek and Coptic"]
    Cyrillic = UNICODE_BLOCKS["Cyrillic"]
    CyrillicSupplement = UNICODE_BLOCKS["Cyrillic Supplement"]
    Armenian = UNICODE_BLOCKS["Armenian"]
    Hebrew = UNICODE_BLOCKS["Hebrew"]
    Arabic = UNICODE_BLOCKS["Arabic"]
    Syriac = UNICODE_BLOCKS["Syriac"]
    ArabicSupplement = UNICODE_BLOCKS["Arabic Supplement"]
    Thaana = UNICODE_BLOCKS["Thaana"]
    NKo = UNICODE_BLOCKS["NKo"]
    Samaritan = UNICODE_BLOCKS["Samaritan"]
    Mandaic = UNICODE_BLOCKS["Mandaic"]
    SyriacSupplement = UNICODE_BLOCKS["Syriac Supplement"]
    ArabicExtendedA = UNICODE_BLOCKS["Arabic Extended-A"]
    Devanagari = UNICODE_BLOCKS["Devanagari"]
    Bengali = UNICODE_BLOCKS["Bengali"]
    Gurmukhi = UNICODE_BLOCKS["Gurmukhi"]
    Gujarati = UNICODE_BLOCKS["Gujarati"]
    Oriya = UNICODE_BLOCKS["Oriya"]
    Tamil = UNICODE_BLOCKS["Tamil"]
    Telugu = UNICODE_BLOCKS["Telugu"]
    Kannada = UNICODE_BLOCKS["Kannada"]
    Malayalam = UNICODE_BLOCKS["Malayalam"]
    Sinhala = UNICODE_BLOCKS["Sinhala"]
    Thai = UNICODE_BLOCKS["Thai"]
    Lao = UNICODE_BLOCKS["Lao"]
    Tibetan = UNICODE_BLOCKS["Tibetan"]
    Myanmar = UNICODE_BLOCKS["Myanmar"]
    Georgian = UNICODE_BLOCKS["Georgian"]
    HangulJamo = UNICODE_BLOCKS["Hangul Jamo"]
    Ethiopic = UNICODE_BLOCKS["Ethiopic"]
    EthiopicSupplement = UNICODE_BLOCKS["Ethiopic Supplement"]
    Cherokee = UNICODE_BLOCKS["Cherokee"]
    UnifiedCanadianAboriginalSyllabics = UNICODE_BLOCKS[
        "Unified Canadian Aboriginal Syllabics"
    ]
    Ogham = UNICODE_BLOCKS["Ogham"]
    Runic = UNICODE_BLOCKS["Runic"]
    Tagalog = UNICODE_BLOCKS["Tagalog"]
    Hanunoo = UNICODE_BLOCKS["Hanunoo"]
    Buhid = UNICODE_BLOCKS["Buhid"]
    Tagbanwa = UNICODE_BLOCKS["Tagbanwa"]
    Khmer = UNICODE_BLOCKS["Khmer"]
    Mongolian = UNICODE_BLOCKS["Mongolian"]
    UnifiedCanadianAboriginalSyllabicsExtended = UNICODE_BLOCKS[
        "Unified Canadian Aboriginal Syllabics Extended"
    ]
    Limbu = UNICODE_BLOCKS["Limbu"]
    TaiLe = UNICODE_BLOCKS["Tai Le"]
    NewTaiLue = UNICODE_BLOCKS["New Tai Lue"]
    KhmerSymbols = UNICODE_BLOCKS["Khmer Symbols"]
    Buginese = UNICODE_BLOCKS["Buginese"]
    TaiTham = UNICODE_BLOCKS["Tai Tham"]
    CombiningDiacriticalMarksExtended = UNICODE_BLOCKS[
        "Combining Diacritical Marks Extended"
    ]
    Balinese = UNICODE_BLOCKS["Balinese"]
    Sundanese = UNICODE_BLOCKS["Sundanese"]
    Batak = UNICODE_BLOCKS["Batak"]
    Lepcha = UNICODE_BLOCKS["Lepcha"]
    OlChiki = UNICODE_BLOCKS["Ol Chiki"]
    CyrillicExtendedC = UNICODE_BLOCKS["Cyrillic Extended-C"]
    GeorgianExtended = UNICODE_BLOCKS["Georgian Extended"]
    SundaneseSupplement = UNICODE_BLOCKS["Sundanese Supplement"]
    VedicExtensions = UNICODE_BLOCKS["Vedic Extensions"]
    PhoneticExtensions = UNICODE_BLOCKS["Phonetic Extensions"]
    PhoneticExtensionsSupplement = UNICODE_BLOCKS["Phonetic Extensions Supplement"]
    CombiningDiacriticalMarksSupplement = UNICODE_BLOCKS[
        "Combining Diacritical Marks Supplement"
    ]
    LatinExtendedAdditional = UNICODE_BLOCKS["Latin Extended Additional"]
    GreekExtended = UNICODE_BLOCKS["Greek Extended"]
    GeneralPunctuation = UNICODE_BLOCKS["General Punctuation"]
    SuperscriptsandSubscripts = UNICODE_BLOCKS["Superscripts and Subscripts"]
    CurrencySymbols = UNICODE_BLOCKS["Currency Symbols"]
    CombiningDiacriticalMarksforSymbols = UNICODE_BLOCKS[
        "Combining Diacritical Marks for Symbols"
    ]
    LetterlikeSymbols = UNICODE_BLOCKS["Letterlike Symbols"]
    NumberForms = UNICODE_BLOCKS["Number Forms"]
    Arrows = UNICODE_BLOCKS["Arrows"]
    MathematicalOperators = UNICODE_BLOCKS["Mathematical Operators"]
    MiscellaneousTechnical = UNICODE_BLOCKS["Miscellaneous Technical"]
    ControlPictures = UNICODE_BLOCKS["Control Pictures"]
    OpticalCharacterRecognition = UNICODE_BLOCKS["Optical Character Recognition"]
    EnclosedAlphanumerics = UNICODE_BLOCKS["Enclosed Alphanumerics"]
    BoxDrawing = UNICODE_BLOCKS["Box Drawing"]
    BlockElements = UNICODE_BLOCKS["Block Elements"]
    GeometricShapes = UNICODE_BLOCKS["Geometric Shapes"]
    MiscellaneousSymbols = UNICODE_BLOCKS["Miscellaneous Symbols"]
    Dingbats = UNICODE_BLOCKS["Dingbats"]
    MiscellaneousMathematicalSymbolsA = UNICODE_BLOCKS[
        "Miscellaneous Mathematical Symbols-A"
    ]
    SupplementalArrowsA = UNICODE_BLOCKS["Supplemental Arrows-A"]
    BraillePatterns = UNICODE_BLOCKS["Braille Patterns"]
    SupplementalArrowsB = UNICODE_BLOCKS["Supplemental Arrows-B"]
    MiscellaneousMathematicalSymbolsB = UNICODE_BLOCKS[
        "Miscellaneous Mathematical Symbols-B"
    ]
    SupplementalMathematicalOperators = UNICODE_BLOCKS[
        "Supplemental Mathematical Operators"
    ]
    MiscellaneousSymbolsandArrows = UNICODE_BLOCKS["Miscellaneous Symbols and Arrows"]
    Glagolitic = UNICODE_BLOCKS["Glagolitic"]
    LatinExtendedC = UNICODE_BLOCKS["Latin Extended-C"]
    Coptic = UNICODE_BLOCKS["Coptic"]
    GeorgianSupplement = UNICODE_BLOCKS["Georgian Supplement"]
    Tifinagh = UNICODE_BLOCKS["Tifinagh"]
    EthiopicExtended = UNICODE_BLOCKS["Ethiopic Extended"]
    CyrillicExtendedA = UNICODE_BLOCKS["Cyrillic Extended-A"]
    SupplementalPunctuation = UNICODE_BLOCKS["Supplemental Punctuation"]
    CJKRadicalsSupplement = UNICODE_BLOCKS["CJK Radicals Supplement"]
    KangxiRadicals = UNICODE_BLOCKS["Kangxi Radicals"]
    IdeographicDescriptionCharacters = UNICODE_BLOCKS[
        "Ideographic Description Characters"
    ]
    CJKSymbolsandPunctuation = UNICODE_BLOCKS["CJK Symbols and Punctuation"]
    Hiragana = UNICODE_BLOCKS["Hiragana"]
    Katakana = UNICODE_BLOCKS["Katakana"]
    Bopomofo = UNICODE_BLOCKS["Bopomofo"]
    HangulCompatibilityJamo = UNICODE_BLOCKS["Hangul Compatibility Jamo"]
    Kanbun = UNICODE_BLOCKS["Kanbun"]
    BopomofoExtended = UNICODE_BLOCKS["Bopomofo Extended"]
    CJKStrokes = UNICODE_BLOCKS["CJK Strokes"]
    KatakanaPhoneticExtensions = UNICODE_BLOCKS["Katakana Phonetic Extensions"]
    EnclosedCJKLettersandMonths = UNICODE_BLOCKS["Enclosed CJK Letters and Months"]
    CJKCompatibility = UNICODE_BLOCKS["CJK Compatibility"]
    CJKUnifiedIdeographsExtensionA = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension A"
    ]
    YijingHexagramSymbols = UNICODE_BLOCKS["Yijing Hexagram Symbols"]
    CJKUnifiedIdeographs = UNICODE_BLOCKS["CJK Unified Ideographs"]
    YiSyllables = UNICODE_BLOCKS["Yi Syllables"]
    YiRadicals = UNICODE_BLOCKS["Yi Radicals"]
    Lisu = UNICODE_BLOCKS["Lisu"]
    Vai = UNICODE_BLOCKS["Vai"]
    CyrillicExtendedB = UNICODE_BLOCKS["Cyrillic Extended-B"]
    Bamum = UNICODE_BLOCKS["Bamum"]
    ModifierToneLetters = UNICODE_BLOCKS["Modifier Tone Letters"]
    LatinExtendedD = UNICODE_BLOCKS["Latin Extended-D"]
    SylotiNagri = UNICODE_BLOCKS["Syloti Nagri"]
    CommonIndicNumberForms = UNICODE_BLOCKS["Common Indic Number Forms"]
    Phagspa = UNICODE_BLOCKS["Phags-pa"]
    Saurashtra = UNICODE_BLOCKS["Saurashtra"]
    DevanagariExtended = UNICODE_BLOCKS["Devanagari Extended"]
    KayahLi = UNICODE_BLOCKS["Kayah Li"]
    Rejang = UNICODE_BLOCKS["Rejang"]
    HangulJamoExtendedA = UNICODE_BLOCKS["Hangul Jamo Extended-A"]
    Javanese = UNICODE_BLOCKS["Javanese"]
    MyanmarExtendedB = UNICODE_BLOCKS["Myanmar Extended-B"]
    Cham = UNICODE_BLOCKS["Cham"]
    MyanmarExtendedA = UNICODE_BLOCKS["Myanmar Extended-A"]
    TaiViet = UNICODE_BLOCKS["Tai Viet"]
    MeeteiMayekExtensions = UNICODE_BLOCKS["Meetei Mayek Extensions"]
    EthiopicExtendedA = UNICODE_BLOCKS["Ethiopic Extended-A"]
    LatinExtendedE = UNICODE_BLOCKS["Latin Extended-E"]
    CherokeeSupplement = UNICODE_BLOCKS["Cherokee Supplement"]
    MeeteiMayek = UNICODE_BLOCKS["Meetei Mayek"]
    HangulSyllables = UNICODE_BLOCKS["Hangul Syllables"]
    HangulJamoExtendedB = UNICODE_BLOCKS["Hangul Jamo Extended-B"]
    HighSurrogates = UNICODE_BLOCKS["High Surrogates"]
    HighPrivateUseSurrogates = UNICODE_BLOCKS["High Private Use Surrogates"]
    LowSurrogates = UNICODE_BLOCKS["Low Surrogates"]
    PrivateUseArea = UNICODE_BLOCKS["Private Use Area"]
    CJKCompatibilityIdeographs = UNICODE_BLOCKS["CJK Compatibility Ideographs"]
    AlphabeticPresentationForms = UNICODE_BLOCKS["Alphabetic Presentation Forms"]
    ArabicPresentationFormsA = UNICODE_BLOCKS["Arabic Presentation Forms-A"]
    VariationSelectors = UNICODE_BLOCKS["Variation Selectors"]
    VerticalForms = UNICODE_BLOCKS["Vertical Forms"]
    CombiningHalfMarks = UNICODE_BLOCKS["Combining Half Marks"]
    CJKCompatibilityForms = UNICODE_BLOCKS["CJK Compatibility Forms"]
    SmallFormVariants = UNICODE_BLOCKS["Small Form Variants"]
    ArabicPresentationFormsB = UNICODE_BLOCKS["Arabic Presentation Forms-B"]
    HalfwidthandFullwidthForms = UNICODE_BLOCKS["Halfwidth and Fullwidth Forms"]
    Specials = UNICODE_BLOCKS["Specials"]
    LinearBSyllabary = UNICODE_BLOCKS["Linear B Syllabary"]
    LinearBIdeograms = UNICODE_BLOCKS["Linear B Ideograms"]
    AegeanNumbers = UNICODE_BLOCKS["Aegean Numbers"]
    AncientGreekNumbers = UNICODE_BLOCKS["Ancient Greek Numbers"]
    AncientSymbols = UNICODE_BLOCKS["Ancient Symbols"]
    PhaistosDisc = UNICODE_BLOCKS["Phaistos Disc"]
    Lycian = UNICODE_BLOCKS["Lycian"]
    Carian = UNICODE_BLOCKS["Carian"]
    CopticEpactNumbers = UNICODE_BLOCKS["Coptic Epact Numbers"]
    OldItalic = UNICODE_BLOCKS["Old Italic"]
    Gothic = UNICODE_BLOCKS["Gothic"]
    OldPermic = UNICODE_BLOCKS["Old Permic"]
    Ugaritic = UNICODE_BLOCKS["Ugaritic"]
    OldPersian = UNICODE_BLOCKS["Old Persian"]
    Deseret = UNICODE_BLOCKS["Deseret"]
    Shavian = UNICODE_BLOCKS["Shavian"]
    Osmanya = UNICODE_BLOCKS["Osmanya"]
    Osage = UNICODE_BLOCKS["Osage"]
    Elbasan = UNICODE_BLOCKS["Elbasan"]
    CaucasianAlbanian = UNICODE_BLOCKS["Caucasian Albanian"]
    LinearA = UNICODE_BLOCKS["Linear A"]
    CypriotSyllabary = UNICODE_BLOCKS["Cypriot Syllabary"]
    ImperialAramaic = UNICODE_BLOCKS["Imperial Aramaic"]
    Palmyrene = UNICODE_BLOCKS["Palmyrene"]
    Nabataean = UNICODE_BLOCKS["Nabataean"]
    Hatran = UNICODE_BLOCKS["Hatran"]
    Phoenician = UNICODE_BLOCKS["Phoenician"]
    Lydian = UNICODE_BLOCKS["Lydian"]
    MeroiticHieroglyphs = UNICODE_BLOCKS["Meroitic Hieroglyphs"]
    MeroiticCursive = UNICODE_BLOCKS["Meroitic Cursive"]
    Kharoshthi = UNICODE_BLOCKS["Kharoshthi"]
    OldSouthArabian = UNICODE_BLOCKS["Old South Arabian"]
    OldNorthArabian = UNICODE_BLOCKS["Old North Arabian"]
    Manichaean = UNICODE_BLOCKS["Manichaean"]
    Avestan = UNICODE_BLOCKS["Avestan"]
    InscriptionalParthian = UNICODE_BLOCKS["Inscriptional Parthian"]
    InscriptionalPahlavi = UNICODE_BLOCKS["Inscriptional Pahlavi"]
    PsalterPahlavi = UNICODE_BLOCKS["Psalter Pahlavi"]
    OldTurkic = UNICODE_BLOCKS["Old Turkic"]
    OldHungarian = UNICODE_BLOCKS["Old Hungarian"]
    HanifiRohingya = UNICODE_BLOCKS["Hanifi Rohingya"]
    RumiNumeralSymbols = UNICODE_BLOCKS["Rumi Numeral Symbols"]
    Yezidi = UNICODE_BLOCKS["Yezidi"]
    OldSogdian = UNICODE_BLOCKS["Old Sogdian"]
    Sogdian = UNICODE_BLOCKS["Sogdian"]
    Chorasmian = UNICODE_BLOCKS["Chorasmian"]
    Elymaic = UNICODE_BLOCKS["Elymaic"]
    Brahmi = UNICODE_BLOCKS["Brahmi"]
    Kaithi = UNICODE_BLOCKS["Kaithi"]
    SoraSompeng = UNICODE_BLOCKS["Sora Sompeng"]
    Chakma = UNICODE_BLOCKS["Chakma"]
    Mahajani = UNICODE_BLOCKS["Mahajani"]
    Sharada = UNICODE_BLOCKS["Sharada"]
    SinhalaArchaicNumbers = UNICODE_BLOCKS["Sinhala Archaic Numbers"]
    Khojki = UNICODE_BLOCKS["Khojki"]
    Multani = UNICODE_BLOCKS["Multani"]
    Khudawadi = UNICODE_BLOCKS["Khudawadi"]
    Grantha = UNICODE_BLOCKS["Grantha"]
    Newa = UNICODE_BLOCKS["Newa"]
    Tirhuta = UNICODE_BLOCKS["Tirhuta"]
    Siddham = UNICODE_BLOCKS["Siddham"]
    Modi = UNICODE_BLOCKS["Modi"]
    MongolianSupplement = UNICODE_BLOCKS["Mongolian Supplement"]
    Takri = UNICODE_BLOCKS["Takri"]
    Ahom = UNICODE_BLOCKS["Ahom"]
    Dogra = UNICODE_BLOCKS["Dogra"]
    WarangCiti = UNICODE_BLOCKS["Warang Citi"]
    DivesAkuru = UNICODE_BLOCKS["Dives Akuru"]
    Nandinagari = UNICODE_BLOCKS["Nandinagari"]
    ZanabazarSquare = UNICODE_BLOCKS["Zanabazar Square"]
    Soyombo = UNICODE_BLOCKS["Soyombo"]
    PauCinHau = UNICODE_BLOCKS["Pau Cin Hau"]
    Bhaiksuki = UNICODE_BLOCKS["Bhaiksuki"]
    Marchen = UNICODE_BLOCKS["Marchen"]
    MasaramGondi = UNICODE_BLOCKS["Masaram Gondi"]
    GunjalaGondi = UNICODE_BLOCKS["Gunjala Gondi"]
    Makasar = UNICODE_BLOCKS["Makasar"]
    LisuSupplement = UNICODE_BLOCKS["Lisu Supplement"]
    TamilSupplement = UNICODE_BLOCKS["Tamil Supplement"]
    Cuneiform = UNICODE_BLOCKS["Cuneiform"]
    CuneiformNumbersandPunctuation = UNICODE_BLOCKS["Cuneiform Numbers and Punctuation"]
    EarlyDynasticCuneiform = UNICODE_BLOCKS["Early Dynastic Cuneiform"]
    EgyptianHieroglyphs = UNICODE_BLOCKS["Egyptian Hieroglyphs"]
    EgyptianHieroglyphFormatControls = UNICODE_BLOCKS[
        "Egyptian Hieroglyph Format Controls"
    ]
    AnatolianHieroglyphs = UNICODE_BLOCKS["Anatolian Hieroglyphs"]
    BamumSupplement = UNICODE_BLOCKS["Bamum Supplement"]
    Mro = UNICODE_BLOCKS["Mro"]
    BassaVah = UNICODE_BLOCKS["Bassa Vah"]
    PahawhHmong = UNICODE_BLOCKS["Pahawh Hmong"]
    Medefaidrin = UNICODE_BLOCKS["Medefaidrin"]
    Miao = UNICODE_BLOCKS["Miao"]
    IdeographicSymbolsandPunctuation = UNICODE_BLOCKS[
        "Ideographic Symbols and Punctuation"
    ]
    Tangut = UNICODE_BLOCKS["Tangut"]
    TangutComponents = UNICODE_BLOCKS["Tangut Components"]
    KhitanSmallScript = UNICODE_BLOCKS["Khitan Small Script"]
    TangutSupplement = UNICODE_BLOCKS["Tangut Supplement"]
    KanaSupplement = UNICODE_BLOCKS["Kana Supplement"]
    KanaExtendedA = UNICODE_BLOCKS["Kana Extended-A"]
    SmallKanaExtension = UNICODE_BLOCKS["Small Kana Extension"]
    Nushu = UNICODE_BLOCKS["Nushu"]
    Duployan = UNICODE_BLOCKS["Duployan"]
    ShorthandFormatControls = UNICODE_BLOCKS["Shorthand Format Controls"]
    ByzantineMusicalSymbols = UNICODE_BLOCKS["Byzantine Musical Symbols"]
    MusicalSymbols = UNICODE_BLOCKS["Musical Symbols"]
    AncientGreekMusicalNotation = UNICODE_BLOCKS["Ancient Greek Musical Notation"]
    MayanNumerals = UNICODE_BLOCKS["Mayan Numerals"]
    TaiXuanJingSymbols = UNICODE_BLOCKS["Tai Xuan Jing Symbols"]
    CountingRodNumerals = UNICODE_BLOCKS["Counting Rod Numerals"]
    MathematicalAlphanumericSymbols = UNICODE_BLOCKS[
        "Mathematical Alphanumeric Symbols"
    ]
    SuttonSignWriting = UNICODE_BLOCKS["Sutton SignWriting"]
    GlagoliticSupplement = UNICODE_BLOCKS["Glagolitic Supplement"]
    NyiakengPuachueHmong = UNICODE_BLOCKS["Nyiakeng Puachue Hmong"]
    Wancho = UNICODE_BLOCKS["Wancho"]
    MendeKikakui = UNICODE_BLOCKS["Mende Kikakui"]
    Adlam = UNICODE_BLOCKS["Adlam"]
    IndicSiyaqNumbers = UNICODE_BLOCKS["Indic Siyaq Numbers"]
    OttomanSiyaqNumbers = UNICODE_BLOCKS["Ottoman Siyaq Numbers"]
    ArabicMathematicalAlphabeticSymbols = UNICODE_BLOCKS[
        "Arabic Mathematical Alphabetic Symbols"
    ]
    MahjongTiles = UNICODE_BLOCKS["Mahjong Tiles"]
    DominoTiles = UNICODE_BLOCKS["Domino Tiles"]
    PlayingCards = UNICODE_BLOCKS["Playing Cards"]
    EnclosedAlphanumericSupplement = UNICODE_BLOCKS["Enclosed Alphanumeric Supplement"]
    EnclosedIdeographicSupplement = UNICODE_BLOCKS["Enclosed Ideographic Supplement"]
    MiscellaneousSymbolsandPictographs = UNICODE_BLOCKS[
        "Miscellaneous Symbols and Pictographs"
    ]
    Emoticons = UNICODE_BLOCKS["Emoticons"]
    OrnamentalDingbats = UNICODE_BLOCKS["Ornamental Dingbats"]
    TransportandMapSymbols = UNICODE_BLOCKS["Transport and Map Symbols"]
    AlchemicalSymbols = UNICODE_BLOCKS["Alchemical Symbols"]
    GeometricShapesExtended = UNICODE_BLOCKS["Geometric Shapes Extended"]
    SupplementalArrowsC = UNICODE_BLOCKS["Supplemental Arrows-C"]
    SupplementalSymbolsandPictographs = UNICODE_BLOCKS[
        "Supplemental Symbols and Pictographs"
    ]
    ChessSymbols = UNICODE_BLOCKS["Chess Symbols"]
    SymbolsandPictographsExtendedA = UNICODE_BLOCKS[
        "Symbols and Pictographs Extended-A"
    ]
    SymbolsforLegacyComputing = UNICODE_BLOCKS["Symbols for Legacy Computing"]
    CJKUnifiedIdeographsExtensionB = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension B"
    ]
    CJKUnifiedIdeographsExtensionC = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension C"
    ]
    CJKUnifiedIdeographsExtensionD = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension D"
    ]
    CJKUnifiedIdeographsExtensionE = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension E"
    ]
    CJKUnifiedIdeographsExtensionF = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension F"
    ]
    CJKCompatibilityIdeographsSupplement = UNICODE_BLOCKS[
        "CJK Compatibility Ideographs Supplement"
    ]
    CJKUnifiedIdeographsExtensionG = UNICODE_BLOCKS[
        "CJK Unified Ideographs Extension G"
    ]
    Tags = UNICODE_BLOCKS["Tags"]
    VariationSelectorsSupplement = UNICODE_BLOCKS["Variation Selectors Supplement"]
    SupplementaryPrivateUseAreaA = UNICODE_BLOCKS["Supplementary Private Use Area-A"]
    SupplementaryPrivateUseAreaB = UNICODE_BLOCKS["Supplementary Private Use Area-B"]
