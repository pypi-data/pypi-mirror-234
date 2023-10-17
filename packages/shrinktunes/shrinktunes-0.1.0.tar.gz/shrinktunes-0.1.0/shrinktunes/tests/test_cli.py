from unittest.mock import patch

import pytest

from shrinktunes.cli import convert_files


@patch("shrinktunes.cli.convert_file")  # Mock the convert_file function
@pytest.mark.asyncio
async def test_convert_files(mock_convert_file, mock_subprocess_run):
    mock_subprocess_run.return_value.returncode = 0
    mock_convert_file.return_value = True
    await convert_files("*.wav", ["mp3"], False, False)
    assert mock_convert_file.call_count == 1
    assert mock_convert_file.call_args[0][0].match("*.wav")
    assert mock_convert_file.call_args[0][1] == "mp3"
