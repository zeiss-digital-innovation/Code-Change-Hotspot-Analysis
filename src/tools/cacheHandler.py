import argparse, sys, os

sys.dont_write_bytecode = True


def check_if_file_exists(file_name: str):

    return os.path.exists(create_path_to_file(file_name))


def create_path_to_file(file_name: str):
    path_to_current_dir: str = os.getcwd()
    return os.path.join(path_to_current_dir, file_name)


def delete_file(file_name: str):
    try:
        os.remove(create_path_to_file(file_name))
        deleted_files.append(file_name)
    except FileNotFoundError as e:
        print(f"{file_name} File was not found")

    except OSError as e:
        print(f"{file_name} could not be removed. You cannot remove directories.")


parser = argparse.ArgumentParser(
    description=f"A script that either deletes or keeps cache files created by createHotspots.py",
    usage="cacheHandler.py [-h] [-d file_name | -k file_name ]",
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-d",
    "--delete",
    action="append",
    nargs="*",
    help="Mode to delete files: -d new.txt old.txt\nEntering no filenames deletes all cache files",
)
group.add_argument(
    "-k",
    "--keep",
    action="append",
    nargs="*",
    help="Mode to keep specified files: -k new.text\nNOTE: Not specified files will be deleted",
)
args = parser.parse_args()
# If no Inputs are given
if len(sys.argv) == 1:
    parser.print_help()

cache: list[str] = [
    "old.txt",
    "new.txt",
    "older_counted.txt",
    "newer_counted.txt",
    "treemap_data.txt",
]

if args.delete:
    d = args.delete
    false_inputs: list[str] = []
    deleted_files: list[str] = []
    no_inputs: bool = False

    # check if user made any imputs
    counter_empty_lists: int = 0
    for i in range(0, len(d)):
        if len(d[i]) == 0:
            counter_empty_lists += 1
            continue
        else:
            continue
    if counter_empty_lists == len(d):
        no_inputs = True

    if no_inputs:
        # TODO Add logic to delete all existing cache files in cwd
        for name in cache:
            if check_if_file_exists(name):
                delete_file(name)
            else:
                continue
    else:
        for i in range(0, len(d)):
            if len(d[i]) != 0:
                for name in d[i]:
                    if (
                        check_if_file_exists(name) and name in cache
                    ):  # Condition so that only cache files are deleted
                        delete_file(file_name=name)
                    else:
                        false_inputs.append(name)
            else:
                continue

    # How many files are actually deleted
    # Lists which are deleted
    if len(deleted_files) > 0:
        print(f"\n{len(deleted_files)} file(s) will be deleted:")
        for name in deleted_files:
            print(f"{name}")
    else:
        print(
            "\nNo files have been deleted.\n"
            "Possible Reasosns:\nTypo in inputs\nFile not registered as cache from createHotspots.py (-h for more info)\n"
            "No cache existing"
        )
    # Prints which files could not be found e.g: because of typo
    if len(false_inputs) > 0:
        print(f"\n{len(false_inputs)} file(s) could not be found:")
        for name in false_inputs:
            print(name)

    print("\nDONE.")
