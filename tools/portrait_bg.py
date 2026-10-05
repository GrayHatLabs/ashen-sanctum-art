"""Backgrounds for the class-select portraits (the characters are composited on top unchanged).

    python tools/portrait_bg.py   -> generated/portrait_bg/{sorceress,inventor}.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402

BGS = {
    "sorceress": "the burning interior of a ruined gothic sanctum at night, broken arches and pillars, fire and glowing "
                 "embers drifting, ash falling, a blood red sky through a shattered rose window, rich red and orange palette",
    "inventor": "a foggy Victorian steampunk city at dusk, brass airships in the sky, clock tower, copper pipes and "
                "rising steam, gas lamps, warm brass and teal palette",
}


def main():
    for name, desc in BGS.items():
        body = {
            "description": f"{desc}, background scenery only, empty street, no people, portrait orientation, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "people, person, character, figure, woman, text, watermark",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"portrait bg {name}", r.get("usage"))
        gen.save_b64(r["image"], gen.d_of("portrait_bg") / f"{name}.png")
        print("saved", name, flush=True)


if __name__ == "__main__":
    main()
