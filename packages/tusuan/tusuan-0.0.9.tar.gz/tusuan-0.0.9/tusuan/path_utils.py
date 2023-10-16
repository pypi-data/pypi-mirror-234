import glob
import os
import queue
import re


def glob_re(root_dir, path_re="**"):
    path_re_parts = path_re.split(os.path.sep)

    dir_queue = queue.SimpleQueue()
    dir_queue.put([root_dir, 0])
    result_set = set()

    while not dir_queue.empty():
        current_dir, parts_index = dir_queue.get()
        pending_paths = []

        if path_re_parts[parts_index] == "**":
            pending_paths = glob.glob(pathname=os.path.join(current_dir, "**"), recursive=True)
        else:
            pattern = re.compile(path_re_parts[parts_index])
            for listed_path in os.listdir(current_dir):
                if pattern.fullmatch(listed_path):
                    pending_paths.append(os.path.join(current_dir, listed_path))

        if parts_index == len(path_re_parts) - 1:
            result_set.update(pending_paths)
        else:
            for path in filter(os.path.isdir, pending_paths):
                dir_queue.put([path, parts_index + 1])

    # pprint(result_set)
    return result_set
