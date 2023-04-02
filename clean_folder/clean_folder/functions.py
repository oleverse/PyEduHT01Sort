from typing import Tuple, Any
import os
import re
import shutil
from py7zr import unpack_7zarchive
import bz2
import gzip
import lzma

from clean_folder import constants as const

# add ability to unpack 7z archives
shutil.register_unpack_format("7zip", [".7z"], unpack_7zarchive)


def transliterate(origin: str) -> str:
    """
  - transliterates cyrillic characters
  """
    result = origin

    pattern = re.compile(r"[а-яА-Я]")

    if re.match(pattern, origin):
        result = origin.translate(const.TRANSLIT_TABLE)

    return result


def normalize(not_normal_string: str) -> str:
    """
  - replaces all characters which are not latin letters with "_" (underscore)
  - does not change the case
  """
    pattern = re.compile(r"[^\w.]")
    result = re.sub(pattern, '_', not_normal_string)

    result = transliterate(result)

    return result


def stream_unpack(extension, src_path, dst_path):
    """
  - unpacks GZ, BZ2 and TX archives
  """
    if not extension:
        raise ValueError

    if not src_path or not dst_path:
        raise ValueError

    if not os.path.isfile(src_path):
        raise ValueError

    decomp_result = None

    try:
        with open(src_path, "rb") as archive_fh:
            if extension == ".GZ":
                decomp_result = gzip.decompress(archive_fh.read())
            elif extension == ".BZ2":
                decomp_result = bz2.decompress(archive_fh.read())
            elif extension == ".XZ":
                decomp_result = lzma.decompress(archive_fh.read())

        with open(dst_path, "wb") as decomp_fh:
            decomp_fh.write(decomp_result)
    except Exception as ex:
        print(f"Error unpacking: {ex}")
        raise ex


def unpack(real_archive_path: str, normalized_archive_path: str) -> Tuple[bool, Any]:
    """
  - unpacks an archive and deletes it after the job is done
  """
    # extract the name and extension parts from the normalized path
    stream_archives_list = (".GZ", ".BZ2", ".XZ")

    if (ext_index := normalized_archive_path.rfind('.')) != -1:
        extension = normalized_archive_path[ext_index:].upper()
        # check if this is tar archive
        if extension in stream_archives_list:
            if (tar_ext_index := normalized_archive_path[:ext_index].upper().rfind(".TAR")) != -1:
                extension = normalized_archive_path[tar_ext_index:].upper() + extension
                ext_index = tar_ext_index

        destination_dir_name = normalized_archive_path[:ext_index]
        if os.path.exists(destination_dir_name):
            return False, const.FS_ERROR_DIR_EXISTS

        try:
            # create the directory
            group_dir_name = os.path.dirname(destination_dir_name)
            if not os.path.exists(group_dir_name):
                os.mkdir(group_dir_name)

            # unpack the archive
            if not os.path.exists(destination_dir_name):
                os.mkdir(destination_dir_name)

            if extension in stream_archives_list:
                _, dst_tail = os.path.split(destination_dir_name)
                stream_unpack(extension, real_archive_path, os.path.join(destination_dir_name, dst_tail))
            else:
                shutil.unpack_archive(real_archive_path, destination_dir_name)

            # remove the origin
            os.remove(real_archive_path)
        except Exception as ex:
            print(ex)
            return False, const.FS_ERROR_RENAMING
    else:
        return False, const.ERROR_ARCHIVE_WITHOUT_EXTENSION

    return True, None


def get_file_group(file_name: str) -> str:
    """
  - categorizes the file by extension
  - returns group name
  """
    group_name = const.FS_DEFAULT_GROUP

    if file_name:
        # there are files with no extension out there
        if '.' in file_name:
            file_extension = file_name.split('.')[-1:][0].upper()
            group_name = const.GROUPS_BY_EXTENSION.get(file_extension, const.FS_DEFAULT_GROUP)

    return group_name


def merge_results(primary: dict, secondary: dict) -> dict:
    """
  - unites two dictionaries
  """
    if primary:
        result = primary
    else:
        # don't use precious CPU time if there's only one dict
        return secondary

    if secondary:
        for key, val in secondary.items():
            try:
                # init the dict key
                if key not in result.keys():
                    result[key] = []

                # values of both dictionaries should be lists
                result[key].extend(val)
            except Exception as ex:
                print(ex)
                continue

    return result


def add_fs_object_to_group(groups_dict: dict, group_name: str, list_item: dict) -> dict:
    """
  - adds a filesystem object to a group (groups will become directories eventually)
  """
    result = groups_dict

    # initialize the group list
    if group_name not in result.keys():
        result[group_name] = []

    result[group_name].append(list_item)

    return result


def move_file_to_group_dir(group_name: str, current_path: str, new_path: str) -> tuple:
    """
  - moves a file to a directory which has a group name
  - instead of moving an archive function unpacks it and the unpacked content
  will be placed to a directory with the name of the archive without an
  extension and this directory in order will be placed in a group directory
  """
    if not group_name or not current_path or not new_path:
        return False, const.ERROR_EMPTY_VALUE

    if os.path.exists(new_path):
        return False, const.FS_ERROR_FILE_EXISTS

    if group_name == const.FS_GROUPS["ARCH"]:
        return unpack(current_path, new_path)
    else:
        try:
            # create the directory
            dir_name = os.path.dirname(new_path)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            # move the file
            os.rename(current_path, new_path)
        except Exception as ex:
            print(ex)
            return False, const.FS_ERROR_RENAMING

    return True, None


def remove_empty_directories(directory: str, recursion_depth=0) -> int:
    """
  - removes empty directories recursively
  """
    if not directory:
        return False

    objects_count = 0

    if os.path.isdir(directory):
        with os.scandir(directory) as dir_iterator:
            for fs_object in dir_iterator:
                objects_count += 1

                if fs_object.is_dir(follow_symlinks=False):
                    deeper_result = remove_empty_directories(fs_object.path, recursion_depth + 1)

                    if not deeper_result:
                        # we are not up to removing the origin directory if it's empty
                        if recursion_depth > 0:
                            # current directory is empty, so we should remove it right here
                            # after removing the parent directory may become empty as well and thus will also be removed
                            try:
                                os.rmdir(fs_object.path)
                                objects_count -= 1
                            except Exception as ex:
                                print(ex)

    return objects_count


def get_file_list(directory: str, root_directory="", recursion_depth=0) -> dict:
    """
  - recursive function which scans the given directory and forms the list of
  grouped files
  - returns a dictionary with such structure:
    {
      "<GROUP_NAME>": [
        {
        "path": "<CURRENT_PATH_TO_THE_FILE>",
        "new_path": "<NEW_PATH_WITH_NORMALIZED_NAME>"
        },
        ...
      ]
    }
  - instead of resulting path "new_path" key can contain an error description
  (for example if we're trying to replace an existing file or directory)
  """
    result = {}

    if directory:
        # keep the base directory for furture renamings
        if not root_directory:
            root_directory = directory

        if os.path.islink(directory):
            print("Symbolic links not supported.")
            print("To treat the symlink as a directory try to add a path "
                  "separator at the end of the path.")
            return {}

        if os.path.isdir(directory):
            with os.scandir(directory) as dir_iterator:
                for fs_object in dir_iterator:
                    if fs_object.is_file(follow_symlinks=False):
                        normalized_name = normalize(fs_object.name)
                        file_group_name = get_file_group(fs_object.name)

                        list_item = {"path": fs_object.path}
                        # leave unknown files intact
                        if file_group_name != const.FS_DEFAULT_GROUP:
                            new_path = os.path.join(os.path.abspath(root_directory), file_group_name, normalized_name)
                            # move the file to a group directory
                            move_result, move_error = move_file_to_group_dir(file_group_name, fs_object.path, new_path)
                            list_item["new_path"] = new_path if move_result else move_error
                        result = add_fs_object_to_group(result, file_group_name, list_item)
                    elif fs_object.is_dir(follow_symlinks=False):
                        # ignore group directories (FS_GROUPS contains their names) if it's not a recursion call
                        if recursion_depth == 0 and fs_object.name in const.FS_GROUPS.values():
                            continue

                        deeper_result = get_file_list(fs_object.path, root_directory, recursion_depth + 1)

                        if deeper_result:
                            result = merge_results(result, deeper_result)
                            dir_normalized_name = normalize(fs_object.name)

                            if dir_normalized_name != fs_object.name:
                                list_item = {"path": fs_object.path}
                                new_path = os.path.join(os.path.split(fs_object.path)[0], dir_normalized_name)
                                list_item["new_path"] = new_path

                                if os.path.exists(new_path):
                                    list_item["new_path"] = const.FS_ERROR_DIR_EXISTS
                                else:
                                    # try to rename the directory
                                    try:
                                        os.rename(fs_object.path, new_path)
                                    except Exception as ex:
                                        print(f"Failed to rename file {fs_object.name}")
                                        print(ex)
                                        list_item["new_path"] = const.FS_ERROR_RENAMING

                                result = add_fs_object_to_group(result, const.FS_DIRECTORY_GROUP, list_item)
                    elif fs_object.is_symlink():
                        # keep symlinks listed because they are the cause why the directory may not be empty
                        result = add_fs_object_to_group(result, const.FS_SYMLINK_GROUP, {"path": fs_object.path})

        if recursion_depth == 0:
            remove_empty_directories(root_directory)

    return result
