"""Create web-sized copies of supplied artwork without changing the originals."""
from pathlib import Path
import shutil
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "NEWSCREEN"
UPDATES = ROOT / "new-images"
LEGACY_UPDATES = ROOT / "new-screen"
ASSETS = ROOT / "docs" / "assets" / "showcase"
POSTERS = {
    "share": "01_give_shape_to_your_verses.jpg",
    "write": "02_every_emotion_finds_its_words.jpg",
    "styles": "03_your_poetry,_your_style.jpg",
    "video": "04_your_verses_come_to_life.jpg",
    "book": "05_your_poems_become_a_book.jpg",
    "space": "06_a_space_all_yours.jpg",
}

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, filename in POSTERS.items():
        source_path = UPDATES / filename
        if not source_path.exists():
            source_path = LEGACY_UPDATES / filename
        if not source_path.exists():
            source_path = SOURCE / filename
        if not source_path.exists():
            if all((ASSETS / f"{name}-{width}.webp").exists() for width in (480, 960)):
                print(f"Retained prepared poster: {name}")
                continue
            raise FileNotFoundError(f"Missing poster source and prepared variants: {filename}")
        with Image.open(source_path) as source:
            original = ImageOps.exif_transpose(source).convert("RGB")
            for width in (480, 960):
                size = (width, round(original.height * width / original.width))
                original.resize(size, Image.Resampling.LANCZOS).save(
                    ASSETS / f"{name}-{width}.webp", quality=86, method=6)
    feature = SOURCE / "poesie_feature_graphic_en_1024x500.png"
    if feature.exists():
        with Image.open(feature) as original:
            assert original.size == (1024, 500), "Unexpected store feature graphic size"
            original.convert("RGB").save(ASSETS / "feature-1024.webp", quality=90, method=6)
        shutil.copy2(feature, ASSETS / "feature-1024.png")
    elif not all((ASSETS / f"feature-1024.{ext}").exists() for ext in ("webp", "png")):
        raise FileNotFoundError("Missing store feature graphic and prepared copies")
    fonts = ROOT / "docs" / "assets" / "fonts"
    fonts.mkdir(exist_ok=True)
    for filename in ("IMFellEnglish-Regular.ttf", "IMFellEnglish-Italic.ttf"):
        source_path = ROOT.parent / "PDF_Poesie_App" / "Resources" / "Fonts" / filename
        target_path = fonts / filename
        if source_path.is_file():
            shutil.copy2(source_path, target_path)
        elif not target_path.is_file():
            raise FileNotFoundError(f"Missing font source and prepared copy: {filename}")
    total = sum(path.stat().st_size for path in ASSETS.glob("*.webp"))
    print(f"Prepared 6 responsive posters and feature graphic: {total / 1024:.0f} KiB of WebP assets.")

if __name__ == "__main__":
    main()
