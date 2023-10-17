# test_shrinktunes.py

import pytest
from unittest.mock import patch
from shrinktunes.ffmpeg import get_ffmpeg_supported_formats, check_ffmpeg_installation, print_ffmpeg_info


@pytest.fixture(autouse=True)
def mock_subprocess_run():
    """Mock subprocess.run to prevent calls to ffmpeg"""
    with patch("subprocess.run") as mock_run:
        yield mock_run


def test_get_ffmpeg_supported_formats(mock_subprocess_run):
    """Test get_ffmpeg_supported_formats function"""

    mock_subprocess_run.return_value.stdout = (
        " D. = Decoding supported\n"
        " .E = Encoding supported\n"
        " --\n"
        " DE webm           WebM with VP8/VP9\n"
        " D  wav            Waveform Audio\n"
    )
    formats = get_ffmpeg_supported_formats()
    assert len(formats) == 2
    assert formats[0].extension == "webm"
    assert formats[0].is_decoder
    assert formats[0].is_encoder
    assert formats[1].extension == "wav"
    assert formats[1].is_decoder
    assert not formats[1].is_encoder


def test_check_ffmpeg_installation(mock_subprocess_run):  # Test check_ffmpeg_installation function
    mock_subprocess_run.return_value.returncode = 0
    assert check_ffmpeg_installation() is True
    mock_subprocess_run.side_effect = FileNotFoundError()
    assert check_ffmpeg_installation() is False


