import argparse
import concurrent.futures
import json
import operator
import shutil
from pathlib import Path

import fgo_mat_counter


def normalize_drop_locations(drops):
    for drop in drops:
        drop["y"] = int((drop["y"] - 145) / 170)
        drop["x"] = int((drop["x"] - 65) / 150)
    return drops


def convert_score_to_float_for_json(drops):
    for drop in drops:
        drop["score"] = float(drop["score"])
    return drops


def analyze_image(image, settings, output_folder, http_folder):
    result = fgo_mat_counter.analyze_image_for_discord(image, settings, http_folder)
    result["drops"] = normalize_drop_locations(result["drops"])
    result["drops"] = convert_score_to_float_for_json(result["drops"])
    result["drops"].sort(key=operator.itemgetter("y", "x"))

    with open(
        output_folder / "result" / image.name.replace("png", "json"),
        "w",
        encoding="utf-8",
    ) as fp:
        json.dump(result, fp, indent=2, ensure_ascii=False)

    shutil.copy2(image, output_folder / "image")
    image.unlink()


def main(input_f, output, http_folder):
    input_folder = Path(input_f).resolve()
    output_folder = Path(output).resolve()
    (output_folder / "image").mkdir(parents=True, exist_ok=True)
    (output_folder / "result").mkdir(parents=True, exist_ok=True)
    with open(input_folder / "settings.json", "r", encoding="utf-8") as fp:
        setting_file = json.load(fp)
    template_dir = input_folder / "files"
    settings = fgo_mat_counter.load_template_images(setting_file, template_dir)
    for image in input_folder.iterdir():
        if image.name.endswith(".png"):
            print(image.name)
            analyze_image(image, settings, output_folder, http_folder)
            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #     executor.submit(analyze_image, image, settings, output_folder, http_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder")
    parser.add_argument("-o", "--output")
    parser.add_argument("-l", "--link")
    args = parser.parse_args()
    main(args.folder, args.output, args.link)
