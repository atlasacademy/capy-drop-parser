import argparse
import errno
import json
import logging
import multiprocessing
import operator
import shutil
import signal
import sys
import time
from pathlib import Path

import cv2

import fgo_mat_counter


TERMINATE = False
SCRIPT_BASE_PATH = Path(sys.argv[0]).parent


def signal_handling(*_):
    global TERMINATE
    if TERMINATE:
        sys.exit(1)
    TERMINATE = True
    print(
        "Notice: app may take up to polling frequency time and however long it takes to finish the queue before exting."
    )


signal.signal(signal.SIGINT, signal_handling)


def get_node_directories():
    node_dirs = []
    for i in (SCRIPT_BASE_PATH / "input").iterdir():
        if i.is_dir():
            node_dirs.append(i)

    return node_dirs


def check_dirs_for_new_images(dir_list):
    work_items = []
    for folder in dir_list:
        for f in folder.iterdir():
            if f.is_file() and cv2.imread(str(f)) is not None:
                new_path = SCRIPT_BASE_PATH / "output" / f.parts[-2] / f.name
                new_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, new_path)
                f.unlink()
                work_items.append(new_path)

    return work_items


def normalize_drop_locations(drops):
    for drop in drops:
        drop["y"] = int(drop["y"] / 110)
        drop["x"] = int((drop["x"] - 50) / 110)

    return drops


def convert_score_to_float_for_json(drops):
    for drop in drops:
        drop["score"] = float(drop["score"])

    return drops


def create_result_json_file(result):
    image_path = Path(result["image_path"])
    json_file_path = image_path.parent / (image_path.stem + ".json")
    with open(json_file_path, "w") as f:
        json.dump(result, f, indent=4)


def handle_success(result):
    if result["matched"]:
        result["drops"] = normalize_drop_locations(result["drops"])
        result["drops"] = convert_score_to_float_for_json(result["drops"])
        result["drops"].sort(key=operator.itemgetter("y", "x"))
    else:
        logging.error(f"analysis failed: {result}")
        result["exception"] = repr(result["exception"])
    create_result_json_file(result)


def handle_failure(result):
    raise Exception(f"Failure handler was called, this should not happen: {result}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-j",
        "--num_processes",
        required=False,
        default=1,
        help="Number of processes to allocate in the process pool",
    )
    arg_parser.add_argument(
        "-p",
        "--polling_frequency",
        required=False,
        default=60,
        help="how often to check for new images in seconds",
    )
    args = arg_parser.parse_args()

    logging.basicConfig(
        format="%(relativeCreated)6d %(threadName)s %(message)s",
        level=logging.ERROR,
        filename="logfile.log",
        filemode="w",
    )
    logging.getLogger("").addHandler(logging.StreamHandler())

    process_pool = multiprocessing.Pool(processes=int(args.num_processes))

    while not TERMINATE:
        for wi in check_dirs_for_new_images(get_node_directories()):
            with open(
                SCRIPT_BASE_PATH / "input" / wi.parts[-2] / "settings.json"
            ) as fp:
                settings = json.load(fp)
            process_pool.apply_async(
                fgo_mat_counter.analyze_image_for_discord,
                [wi, settings, SCRIPT_BASE_PATH / "input" / wi.parts[-2] / "files"],
                {},
                handle_success,
                handle_failure,
            )

        time.sleep(int(args.polling_frequency))

    print("shutting down....")
    process_pool.close()
    process_pool.join()
    print("done")
