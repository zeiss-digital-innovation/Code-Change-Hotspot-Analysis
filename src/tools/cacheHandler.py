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


cache: list[str] = [
    "old.txt",
    "new.txt",
    "older_counted.txt",
    "newer_counted.txt",
    "treemap_data.txt",
]

parser = argparse.ArgumentParser(
    description=f"A script that either deletes or keeps cache files created by createHotspots.py",
    usage="cacheHandler.py [-h] [-d file_name | -k file_name ]",
    epilog=f"Possible cache files:{cache} "
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


if args.delete:
    # d is a list of lists, depending on how many times parameter -d or --delete is given
    # example: py ... -d "foo.txt" "baz.txt" --delete "god_is_good.txt" --> [['foo.txt', 'baz.txt'], ['god_is_good.txt']]
    d = args.delete
    existing_cache: list[str] = [name for name in cache if check_if_file_exists(name)]
    false_inputs: list[str] = []
    deleted_files: list[str] = []
    no_inputs: bool = False

    # lists the existing cache:
    if len(existing_cache) > 0:
        print(f"\nCache files found: {len(existing_cache)}") 
        for name in existing_cache:
            print(f"{name}")
    else: 
        print("\nNo cache found")
        print("\n\nDONE.")
        sys.exit(0)
        

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
    
    # Deletion logic
    if no_inputs:
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
            
    # Prints which files could not be found e.g: because of typo
    if len(false_inputs) > 0:
        print(f"\n{len(false_inputs)} file(s) could not be found:")
        for name in false_inputs:
            print(name)

    # How many files are actually deleted
    # Lists which files are deleted
    if len(deleted_files) > 0:
        print(f"\n{len(deleted_files)} cache file(s) will be deleted:")
        for name in deleted_files:
            print(f"{name}")
    else:
        print(
            "\nNo files have been deleted.\n"
            "Possible Reasons:\nTypo in inputs\nFile not registered as cache from createHotspots.py (-h for more info)\n"
            "No cache existing"
        )
    
    print("\nDONE.")

if args.keep:
    # k is a list of lists, depending on how many times parameter -k or --keep is given
    # example: py ... -k "foo.txt" "baz.txt" --keep "god_is_good.txt" --> [['foo.txt', 'baz.txt'], ['god_is_good.txt']]
    k = args.keep
    existing_cache: list[str] = [name for name in cache if check_if_file_exists(name)]
    false_inputs: list[str] = []
    kept_files: list[str] = []
    deleted_files: list[str] = []
    no_inputs: bool = False

    # lists the existing cache:
    if len(existing_cache) > 0:
        print(f"\nCache files found: {len(existing_cache)}") 
        for name in existing_cache:
            print(f"{name}")
    else: 
        print("\nNo cache found")
        print("\n\nDONE.")
        sys.exit(0)

    # check if user made any imputs
    counter_empty_lists: int = 0
    for i in range(0, len(k)):
        if len(k[i]) == 0:
            counter_empty_lists += 1
            continue
        else:
            continue
    if counter_empty_lists == len(k):
        no_inputs = True

    if no_inputs:
        print("\nNo inputs given.\nNo files will be deleted!")
        sys.exit(0)
        print("\nDONE.")
    # Deletion logic 
    else:  # used to determine which files should be deleted
        for i in range(0, len(k)):
            if len(k[i]) != 0:
                for name in k[i]:
                    if check_if_file_exists(name) and name in existing_cache:
                        kept_files.append(name)
                        existing_cache.remove(name) 
                    else:
                        false_inputs.append(name)
        for name in existing_cache:
            delete_file(name)
    
    # Lists which files are kept
    if len(kept_files) > 0: 
        print(f"\n{len(kept_files)} cache file(s) saved through input:")
        for name in kept_files:
            print(name)
    
    # Prints which files could not be found e.g: because of typo
    if len(false_inputs) > 0:
        print(f"\n{len(false_inputs)} file(s) could not be found:")
        for name in false_inputs:
            print(name)
            
    # How many files are actually deleted
    # Lists which files are deleted
    if len(deleted_files) > 0:
        print(f"\n{len(deleted_files)} file(s) will be deleted:")
        for name in deleted_files:
            print(f"{name}")
    else:
        print(
            "\nNo files have been deleted.\n"
            "Possible Reasons:\n"
            "Files saved through input"
        )

    print("\nDONE.")
    