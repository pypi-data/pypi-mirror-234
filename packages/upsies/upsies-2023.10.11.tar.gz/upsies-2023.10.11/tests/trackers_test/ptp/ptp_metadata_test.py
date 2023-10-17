import pytest

from upsies.trackers.ptp import metadata


@pytest.mark.parametrize(
    argnames='reason, exp_value',
    argvalues=(
        (metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES, 14),
        (metadata.PtpTrumpableReason.HARDCODED_SUBTITLES, 4),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTrumpableReason_value(reason, exp_value):
    assert reason.value == exp_value


@pytest.mark.parametrize(
    argnames='reason, string',
    argvalues=(
        (metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES, 'No English Subtitles'),
        (metadata.PtpTrumpableReason.HARDCODED_SUBTITLES, 'Hardcoded Subtitles'),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTrumpableReason_string(reason, string):
    assert str(reason) == string
    assert type(reason).from_string(string) is reason
