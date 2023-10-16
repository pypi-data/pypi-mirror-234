"""PDFbox Package."""
__all__ = (
    "PDFBOX_DATA",
    "PDFBOX_DATA_TESTS",
    "PDF_REDUCE_THRESHOLD",
    "SCAN_PREFIX",
    "exif_rm_tags",
    "pdf_diff",
    "pdf_from_picture",
    "pdf_linearize",
    "pdf_reduce",
    "pdf_scan",
    "pdf_to_picture",
)

import difflib
import random
import shutil
import subprocess
import tempfile
from typing import Literal

import fitz
import nodeps
from nodeps import Path

PDFBOX_DATA = Path(__file__).parent / "data"
PDFBOX_DATA_TESTS = PDFBOX_DATA / "tests"
PDF_REDUCE_THRESHOLD = 2000000
"""Reduce pdf for files bigger than 2MB"""
SCAN_PREFIX = "scanned_"


def exif_rm_tags(file: Path | str):
    """Removes tags with exiftool in pdf."""
    nodeps.which("exiftool", raises=True)

    subprocess.check_call(["exiftool", "-q", "-q", "-all=", "-overwrite_original", file])


def pdf_diff(file1: Path | str, file2: Path | str) -> list[bytes]:
    """Show diffs of two pdfs.

    Args:
        file1: file 1
        file2: file 2

    Returns:
        True if equals
    """
    return list(
        difflib.diff_bytes(
            difflib.unified_diff, Path(file1).read_bytes().splitlines(), Path(file2).read_bytes().splitlines(), n=1
        )
    )


def pdf_from_picture(file: Path | str, picture: Path | str, rm: bool = True) -> Path:
    """Creates pdf from image.

    Args:
        file: pdf file
        picture: image file
        rm: remove image file (default: True)
    """
    doc = fitz.Document()
    doc.new_page()
    page = doc[0]
    page.insert_image(page.rect, filename=picture)
    doc.save(Path(file))
    if rm:
        Path(picture).unlink()
    return file


def pdf_linearize(file: Path | str) -> None:
    """Linearize pdf (overwrites original)."""
    nodeps.which("qpdf")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "tmp.pdf"
        subprocess.run(["qpdf", "--linearize", file, tmp])
        Path(tmp).replace(file)


def pdf_reduce(
        path: Path | str,
        level: Literal["/default", "/prepress", "ebook", "/screen"] = "/prepress",
        threshold: int | None = PDF_REDUCE_THRESHOLD,
) -> None:
    """Compress pdf.

    https://www.adobe.com/acrobat/hub/how-to-compress-pdf-in-linux.html

    Examples:
        >>> import shutil
        >>> from nodeps import Path
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import pdf_reduce
        >>>
        >>> original = PDFBOX_DATA_TESTS / "5.2M.pdf"
        >>> backup = PDFBOX_DATA_TESTS / "5.2M-bk.pdf"
        >>>
        >>> shutil.copyfile(original, backup)  # doctest: +ELLIPSIS
        Path('.../kitpdf/data/tests/5.2M-bk.pdf')
        >>> original_size = original.stat().st_size
        >>> pdf_reduce(original, level="/screen")
        >>> reduced_size = original.stat().st_size
        >>> assert original_size != reduced_size  # doctest: +SKIP
        >>> shutil.move(backup, original)  # doctest: +ELLIPSIS
        Path('.../kitpdf/data/tests/5.2M.pdf')

    Args:
        path: path to file
        threshold: limit in MB to reduce file size, None to reuce any pdf
        level: /default is selected by the system, /prepress 300 dpi, ebook 150 dpi, screen 72 dpi

    Returns:
        None
    """
    if threshold is None or Path(path).stat().st_size > threshold:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir) / "tmp.pdf"
            subprocess.check_call(
                [
                    "gs",
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    f"-dPDFSETTINGS={level}",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={tmp}",
                    path,
                ]
            )
            Path(tmp).replace(path)


def pdf_scan(file: Path, directory: Path | None = None) -> Path:
    """Looks like scanned, linearize and sets tag color.

    Examples:
        >>> from pathlib import Path
        >>> from kitpdf import PDFBOX_DATA
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import SCAN_PREFIX
        >>> from kitpdf import pdf_scan
        >>>
        >>> for f in Path(PDFBOX_DATA_TESTS).iterdir():
        ...     if f.is_file() and f.suffix == ".pdf":
        ...         assert f"generated/{SCAN_PREFIX}" in str(pdf_scan(f, PDFBOX_DATA_TESTS / "generated"))

    Args:
        file: path of file to be scanned
        directory: destination directory (Default: file directory)

    Returns:
        Destination file
    """
    rotate = round(random.uniform(*random.choice([(-0.9, -0.5), (0.5, 0.9)])), 2)  # noqa: S311

    file = Path(file)
    filename = f"{SCAN_PREFIX}{file.stem}{file.suffix}"
    if directory:
        directory = Path(directory)
        if not directory.is_dir():
            directory.mkdir()
        dest = directory / filename
    else:
        dest = file.with_name(filename)

    nodeps.which("convert", raises=True)

    subprocess.check_call(
        [
            "convert",
            "-density",
            "120",
            file,
            "-attenuate",
            "0.4",
            "+noise",
            "Gaussian",
            "-rotate",
            str(rotate),
            "-attenuate",
            "0.03",
            "+noise",
            "Uniform",
            "-sharpen",
            "0x1.0",
            dest,
        ]
    )
    return dest


def pdf_to_picture(file: Path | str, dpi: int = 300, fmt: Literal["jpeg", "png"] = "jpeg") -> Path:
    """Creates a file with jpeg in the same directory from first page of pdf."""
    nodeps.which("pdftoppm")

    file = Path(file)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "tmp"
        subprocess.run(["pdftoppm", f"-{fmt}", "-r", str(dpi), "-singlefile", file, tmp])
        suffix = f".{fmt}" if fmt == "png" else ".jpg"
        if not (dest := tmp.with_suffix(suffix)).exists():
            msg = f"File not found {dest}"
            raise FileNotFoundError(msg)
        return shutil.copy(dest, file.with_suffix(suffix))
