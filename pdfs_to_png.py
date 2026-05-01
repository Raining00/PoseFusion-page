from pathlib import Path
import argparse
import shutil
import subprocess


def convert_pdf_to_png(pdf_path: Path, output_dir: Path, dpi: int) -> None:
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        convert_pdf_to_png_with_ghostscript(pdf_path, output_dir, dpi)
        return

    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        output_path = output_dir / f"{pdf_path.stem}_page_{page_index + 1:03d}.png"
        pix.save(output_path)
        print(f"Saved: {output_path}")

    doc.close()


def convert_pdf_to_png_with_ghostscript(pdf_path: Path, output_dir: Path, dpi: int) -> None:
    gs_path = shutil.which("gs")
    if not gs_path:
        raise SystemExit(
            "Missing dependency: install PyMuPDF or Ghostscript.\n"
            "PyMuPDF: python3 -m pip install pymupdf\n"
            "Ghostscript on Ubuntu: sudo apt install ghostscript"
        )

    output_pattern = output_dir / f"{pdf_path.stem}_page_%03d.png"
    subprocess.run(
        [
            gs_path,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=png16m",
            f"-r{dpi}",
            "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4",
            f"-sOutputFile={output_pattern}",
            str(pdf_path),
        ],
        check=True,
    )
    print(f"Saved: {output_pattern}")


def convert_folder(input_dir: Path, output_dir: Path, dpi: int) -> None:
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in: {input_dir}")
        return

    for pdf_path in pdf_files:
        convert_pdf_to_png(pdf_path, output_dir, dpi)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert all PDF files in a folder to PNG images."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("./figs"),
        help="Folder containing PDF files. Default: ./figs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./images"),
        help="Folder to write PNG files. Default: ./images",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Output image resolution. Default: 300",
    )
    args = parser.parse_args()

    convert_folder(args.input, args.output, args.dpi)


if __name__ == "__main__":
    main()
