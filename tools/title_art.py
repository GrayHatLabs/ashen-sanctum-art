"""Title screen background (bitforge, 200x113 = 16:9; the game scales it up).

    python tools/title_art.py      -> generated/title/title_bg.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402


def main():
    body = {
        "description": (
            "wide landscape painting of a ruined gothic cathedral sanctum on a hill at night, burning embers and ash "
            "drifting through the air, a dark blood red sky with a pale moon, jagged mountains, dead trees in the "
            "foreground, dark gothic fantasy, Diablo 2 title screen mood, no characters"
        ),
        "image_size": {"width": 200, "height": 113},
        "no_background": False,
        "outline": "lineless",
        "shading": "detailed shading",
        "detail": "highly detailed",
        "view": "side",
        "negative_description": "text, letters, logo, watermark, people, characters",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge("title background", r.get("usage"))
    gen.save_b64(r["image"], gen.d_of("title") / "title_bg.png")
    print("saved title_bg", flush=True)


if __name__ == "__main__":
    main()
