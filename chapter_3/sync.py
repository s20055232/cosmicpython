import hashlib
from pathlib import Path
import os
import shutil

BLOCKSIZE = 65536


def sync(source, dest):
    source_hashes = {}
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = {}
    dest_hashes = read_paths_and_hashes(dest)

    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    for action, *paths in actions:
        if action == "copy":
            shutil.copyfile(*paths)
        if action == "move":
            shutil.move(*paths)
        if action == "delete":
            os.remove(paths[0])


def read_paths_and_hashes(root):
    # Walk the root folder and build a dict of filenames and their hashes
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            # for every file that appears in source but not target, copy the file to
            # the target
            yield "copy", sourcepath, destpath
        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            # if there's a file in target that has a different path in source,
            # move it to the correct path
            yield "move", olddestpath, newdestpath

        for sha, filename in dst_hashes.items():
            if sha not in src_hashes:
                # if there's a file in target that's not in source, delete it
                yield "delete", dst_folder / filename


def hash_file(path: Path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()
