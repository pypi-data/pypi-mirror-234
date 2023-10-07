"""
Hardcoded PTP metadata from upload.php
"""

import enum

ptp_tags = (
    'action',
    'adventure',
    'animation',
    'arthouse',
    'asian',
    'biography',
    'camp',
    'comedy',
    'crime',
    'cult',
    'documentary',
    'drama',
    'experimental',
    'exploitation',
    'family',
    'fantasy',
    'film.noir',
    'history',
    'horror',
    'martial.arts',
    'musical',
    'mystery',
    'performance',
    'philosophy',
    'politics',
    'romance',
    'sci.fi',
    'short',
    'silent',
    'sport',
    'thriller',
    'video.art',
    'war',
    'western',
)


ptp_subtitles = {
    # Special codes
    'No Subtitles': '44',
    'en (forced)': '50',

    # TODO: No idea what intertitles are exactly and how to detect them.
    # 'English Intertitles': '51',

    # Regular languages
    'ar': '22',     # Arabic
    'bg': '29',     # Bulgarian
    'zh': '14',     # Chinese
    'hr': '23',     # Croatian
    'cs': '30',     # Czech
    'da': '10',     # Danish
    'nl': '9',      # Dutch
    'en': '3',      # English
    'et': '38',     # Estonian
    'fi': '15',     # Finnish
    'fr': '5',      # French
    'de': '6',      # German
    'el': '26',     # Greek
    'he': '40',     # Hebrew
    'hi': '41',     # Hindi
    'hu': '24',     # Hungarian
    'is': '28',     # Icelandic
    'id': '47',     # Indonesian
    'it': '16',     # Italian
    'ja': '8',      # Japanese
    'ko': '19',     # Korean
    'lv': '37',     # Latvian
    'lt': '39',     # Lithuanian
    'no': '12',     # Norwegian
    'fa': '52',     # Persian
    'pl': '17',     # Polish
    'pt': '21',     # Portuguese
    'pt-BR': '49',  # Brazilian Port.
    'ro': '13',     # Romanian
    'ru': '7',      # Russian
    'sr': '31',     # Serbian
    'sk': '42',     # Slovak
    'sl': '43',     # Slovenian
    'es': '4',      # Spanish
    'sv': '11',     # Swedish
    'th': '20',     # Thai
    'tr': '18',     # Turkish
    'uk': '34',     # Ukrainian
    'vi': '25',     # Vietnamese
}


class PtpTrumpableReason(enum.Enum):
    """
    Reason why a release is trumpable

    An instance's :attr:`value` is the value expected by the API. An instance's
    string representation should be human-readable and pretty.
    """

    NO_ENGLISH_SUBTITLES = 14
    HARDCODED_SUBTITLES = 4

    @classmethod
    def from_string(cls, string):
        """
        Convert human-readable string back to :class:`PtpTrumpableReason` instance

        >>> PtpTrumpableReason.from_string(
        ...     str(PtpTrumpableReason.HARDCODED_SUBTITLES)
        ... )
        <PtpTrumpableReason.HARDCODED_SUBTITLES: 4>
        """

        name = string.replace(' ', '_').upper()
        return getattr(cls, name)

    def __str__(self):
        return ' '.join((
            word.capitalize()
            for word in self.name.split('_')
        ))
