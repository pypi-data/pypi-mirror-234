import typer
import asyncio
from pathlib import Path
import subprocess
from datetime import datetime

from shrinktunes.ffmpeg import (
    check_ffmpeg_installation,
    print_ffmpeg_info,
    SUPPORTED_FORMATS_BY_EXTENSION,
    show_ffmpeg_install_message,
)

app = typer.Typer()


# Log with a timestamp, only if verbose mode is enabled
def log(message, verbose):
    if verbose:
        typer.echo(f"[{datetime.now().isoformat()}] {message}")


# Convert a single file to the desired format
async def convert_file(input_path: Path, output_path: Path, verbose: bool, force: bool):
    subprocess.run(["ffmpeg", "-i", str(input_path), str(output_path)], check=True)
    log(f"Converted {input_path} -> {output_path}", verbose)
    return True


# Convert all files matching the glob pattern to the desired formats
async def convert_files(glob_pattern: str, output_formats: list[str], verbose: bool, force: bool):
    # Use Path().glob() to expand the pattern and get all matching files
    paths = list(Path().glob(glob_pattern))
    log(f"Scanning glob {glob_pattern}", verbose)
    log(f"Found {len(paths)} files", verbose)

    converted_paths = []
    failed_paths = []
    skipped_paths = []

    for output_format in output_formats:
        for path in paths:
            ext = path.suffix.removeprefix(".")
            if ext not in SUPPORTED_FORMATS_BY_EXTENSION:
                typer.echo(typer.style(f"Unsupported file format: {ext} ({path})", bold=True, fg=typer.colors.RED))
                failed_paths.append(path)
                continue

            if not SUPPORTED_FORMATS_BY_EXTENSION[ext].is_encoder:
                typer.echo(typer.style(
                    f"ffmpeg does not support encoding {ext}", fg=typer.colors.RED
                ))
                failed_paths.append(path)
                continue

            output_path = path.with_suffix(f".{output_format}")

            if output_path.exists() and not force:
                typer.echo(typer.style(
                    f"Skipping {output_path} as it already exists. Use -f to force overwrite.",
                    fg=typer.colors.YELLOW,
                ))
                skipped_paths.append(path)
                continue

            success = await convert_file(path, output_path, verbose, force)
            if success:
                converted_paths.append(path)
            else:
                failed_paths.append(path)

    typer.echo(
        f"{len(converted_paths)} files converted, {len(skipped_paths)} skipped, {len(failed_paths)} failed"
    )


@app.command()
def convert(
        glob_pattern: str = typer.Argument(..., help="Glob pattern for .wav files to convert."),
        output: list[str] = typer.Option(..., "-o",
                                         help="Output format(s). Supported formats are dynamically determined from ffmpeg."),
        verbose: bool = typer.Option(False, "-v", help="Enable verbose mode."),
        force: bool = typer.Option(False, "-f", help="Force overwrite of existing files.")
):
    """
    Convert .wav files matching the glob pattern to the specified format(s).
    """
    try:
        check_ffmpeg_installation(raises=True)
    except FFMpegError:
        show_ffmpeg_install_message()
        raise typer.Exit(code=1)

    # Check if the output format is supported
    for fmt in output:
        if fmt not in SUPPORTED_FORMATS_BY_EXTENSION:
            typer.echo(f"Unsupported output format: {fmt}")
            raise typer.Exit(code=1)

    try:
        # Convert the files
        asyncio.run(convert_files(glob_pattern, output, verbose, force))
    except Exception as e:
        typer.echo(f"Error occurred: {e}")
        raise typer.Exit(code=1)


@app.command()
def info():
    print_ffmpeg_info(print_decoders=True, print_encoders=True)


def cli_main():
    app()


if __name__ == "__main__":
    cli_main()
