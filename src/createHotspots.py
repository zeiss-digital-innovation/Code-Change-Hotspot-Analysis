import pandas as pd
import plotly.express as px

# needs to be downloaded

import sys, os, re, shutil, datetime, subprocess, timeit, argparse
from collections import Counter


sys.dont_write_bytecode = True

# The path to the directory in which the user runs the script
# Used for caching (creating the texfiles)
path_to_starting_dir: str = os.getcwd()

parser = argparse.ArgumentParser(
    description="A script that displays a interactive treemap in the web-browser. "
    "It does a Hotspot analysis based on the "
    "data recieved from the git log history (number of changes on each file) of the local repository. "
    "The date given as the second argument acts as a border between the recently edited and legacy code. ",
    epilog="More info: https://github.com/zeiss-digital-innovation/Code-Change-Hotspot-Analysis",
)
parser.add_argument("repo", help='Example: "C:/path/to/local/repo"')
parser.add_argument("date", help='Format: YYYY-MM-DD e.g. "2024-02-01"')


def check_if_directory_exists(path_to_repo: str):
    if not os.path.exists(path_to_repo):
        print(
            "The inputted path does not exist or contains errors.\n"
            'Example: py createHotspots.py "C:/path/to/repo"\n\n'
            f"Your input:\n\n{path_to_repo}"
        )

        sys.exit(1)
    else:
        return path_to_repo


def check_date_format(date: str):
    try:
        y = datetime.datetime.strptime(date, "%Y-%m-%d")
        return y.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Wrong date input: {date}\nExpected format: YYYY-MM-DD\n")
        print(f"Error Message:\n{e}")
        sys.exit(1)


def check_if_data_exists(file_name: str):

    return os.path.exists(create_path_to_data(file_name))


def create_path_to_data(file_name: str):
    return os.path.join(path_to_starting_dir, file_name)


def get_data(path_to_repo: str, date: str):

    older_data_file_path: str = os.path.join(path_to_starting_dir, "old.txt")
    newer_data_file_path: str = os.path.join(path_to_starting_dir, "new.txt")

    os.chdir(path=path_to_repo)
    older_data = subprocess.run(
        ["git", "log", f"--before={date}", "--pretty=format:", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )

    newer_data = subprocess.run(
        ["git", "log", f"--after={date}", "--pretty=format:", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )

    with open(older_data_file_path, "w") as file:
        file.write(older_data.stdout)

    with open(newer_data_file_path, "w") as file:
        file.write(newer_data.stdout)

    return older_data_file_path, newer_data_file_path


def count_lines(older_data_file_path: str, newer_data_file_path: str):

    if os.stat(older_data_file_path).st_size == 0:
        print(
            "There is an empty Textfile!\n"
            "You might want to change the date to one closer to the present.\n\n"
            f"Empty file:\n{older_data_file_path}"
        )
        sys.exit(1)
    else:
        with open(older_data_file_path, "r") as file:
            # reads all lines and removes empty spaces and line breaks
            older_data_lines = [
                line.strip() for line in file.readlines() if line.strip()
            ]
            # Filers Special characters and keep only alphanumeric character
            older_data_filtered_lines = [
                re.sub(r"[^a-zA-Z0-9\s\\\/\.]", "", line) for line in older_data_lines
            ]
            # Counts the occurences of every filtered line
            older_data_line_counts = Counter(older_data_filtered_lines)

            older_data_output_file_path = os.path.join(
                path_to_starting_dir, "older_counted.txt"
            )

            with open(older_data_output_file_path, "w") as output_file:
                for line, count in older_data_line_counts.items():
                    if line:  # Ensure the line is not empty
                        output_file.write(f"{line}: {count}\n")

    if os.stat(newer_data_file_path).st_size == 0:
        print(
            "There is an empty Textfile!\n"
            "You might want to change the date to one further away from the present.\n\n"
            f"Empty file:\n{newer_data_file_path}"
        )
        sys.exit(1)
    else:
        with open(newer_data_file_path, "r") as file:
            # reads all lines and removes empty spaces and line breaks
            newer_data_lines = [
                line.strip() for line in file.readlines() if line.strip()
            ]
            # Filers Special characters and keep only alphanumeric character
            newer_data_filtered_lines = [
                re.sub(r"[^a-zA-Z0-9\s\\\/\.]", "", line) for line in newer_data_lines
            ]
            # Counts the occurences of every filtered line
            newer_data_line_counts = Counter(newer_data_filtered_lines)

            newer_data_output_file_path = os.path.join(
                path_to_starting_dir, "newer_counted.txt"
            )

        with open(newer_data_output_file_path, "w") as output_file:
            for line, count in newer_data_line_counts.items():
                if line:  # Ensure the line is not empty
                    output_file.write(f"{line}: {count}\n")

    return older_data_output_file_path, newer_data_output_file_path


def compare_data(older_data_counted_file_path: str, newer_data_counted_file_path: str):

    treemap_data_file_path: str = shutil.copyfile(
        src=newer_data_counted_file_path,
        dst=os.path.join(path_to_starting_dir, "treemap_data.txt"),
    )

    # Creates the lists so only the paths are compared
    with open(older_data_counted_file_path, "r") as file:
        older_data_paths_as_list: list[str] = []
        for line in file:
            path, _ = line.strip().split(": ")
            older_data_paths_as_list.append(path)

    with open(newer_data_counted_file_path, "r") as file2:
        newer_data_paths_as_list: list[str] = []
        for line in file2.readlines():
            path, _ = line.strip().split(": ")
            newer_data_paths_as_list.append(path)

    # Actual Comparison
    with open(treemap_data_file_path, "a+") as file3:
        for line in older_data_paths_as_list:
            if line not in newer_data_paths_as_list:
                file3.write(f"\n{line}: 0")

    return treemap_data_file_path


def displaying_treemap(treemap_data_file_path: str):

    data: list = []
    # Data from the git log command after the set date (i.e 2024/01/01)
    # After running count_lines and compare_data (treemap_data.txt)
    with open(treemap_data_file_path, "r") as file:
        for line in file:
            if line.strip():
                path, changes = line.strip().split(": ")
                changes = int(changes)
                changes += 1  # Counting this as the initial commit
                data.append({"File Path": path, "Changes": changes})
            else:
                continue
    df = pd.DataFrame(data)

    df["Path Components"] = df["File Path"].apply(lambda x: x.split("/"))
    max_depth_of_dir: int = df["Path Components"].apply(len).max()
    for i in range(0, max_depth_of_dir):
        df[f"Level {i + 1}"] = df["Path Components"].apply(
            lambda x: x[i] if i < len(x) else None
        )
    # i == 0 --> Level 1; i == max_depth_of_dir == 4 --> Level 5

    df["Colors"] = df["Changes"].apply(lambda x: "#CAEDFB" if x == 1 else "#FAE2D6")

    print(df)

    path = [px.Constant("all")] + [f"Level {i}" for i in range(1, max_depth_of_dir + 1)]
    fig = px.treemap(
        df,
        path=path,
        values="Changes",
        title="Treemap der Dateipfade basierend auf Änderungen",
        color="Colors",
        color_discrete_sequence=["#CAEDFB", "#FAE2D6", "#F2F2F2"],
    )
    fig.update_traces(root_color="lightgrey")

    fig.show()


def script():
    path_to_repo: str = check_if_directory_exists(path_to_repo=args.repo)
    date: str = check_date_format(date=args.date)

    # Checks first if treemap data exists
    # because it saves more time if treemap data actually exists
    if check_if_data_exists("treemap_data.txt"):
        print(
            f"Found path to treemap data:\n\n{create_path_to_data('treemap_data.txt')}\n\n"
            "Skipping 3/3 steps..."
        )
        displaying_treemap(
            treemap_data_file_path=create_path_to_data("treemap_data.txt")
        )

    elif check_if_data_exists("newer_counted.txt") and check_if_data_exists(
        "older_counted.txt"
    ):
        print(
            f"Found path to newer_counted data:\n\n{create_path_to_data('newer_counted.txt')}\n\n"
            f"And found path to older_counted data:\n\n{create_path_to_data('older_counted.txt')}\n\n"
            "Skipping 2/3 steps..."
        )
        treemap_data_file_path: str = compare_data(
            older_data_counted_file_path=create_path_to_data("older_counted.txt"),
            newer_data_counted_file_path=create_path_to_data("newer_data.txt"),
        )
        displaying_treemap(treemap_data_file_path=treemap_data_file_path)

    elif check_if_data_exists("new.txt") and check_if_data_exists("old.txt"):
        print(
            f"Found path to new data:\n\n{create_path_to_data('new.txt')}\n\n"
            f"And found path to old data:\n\n{create_path_to_data('old.txt')}\n\n"
            "Skipping 1/3 steps..."
        )
        older_data_counted_file_path, newer_data_counted_file_path = count_lines(
            older_data_file_path=create_path_to_data("old.txt"),
            newer_data_file_path=create_path_to_data("new.txt"),
        )
        treemap_data_file_path: str = compare_data(
            older_data_counted_file_path=older_data_counted_file_path,
            newer_data_counted_file_path=newer_data_counted_file_path,
        )
        displaying_treemap(treemap_data_file_path=treemap_data_file_path)

    else:
        print("Found no data.\nSkipping 0/3 steps")
        older_data_file_path, newer_data_file_path = get_data(
            path_to_repo=path_to_repo, date=date
        )
        older_data_counted_file_path, newer_data_counted_file_path = count_lines(
            older_data_file_path=older_data_file_path,
            newer_data_file_path=newer_data_file_path,
        )
        treemap_data_file_path: str = compare_data(
            older_data_counted_file_path=older_data_counted_file_path,
            newer_data_counted_file_path=newer_data_counted_file_path,
        )
        displaying_treemap(treemap_data_file_path=treemap_data_file_path)


# Running the actual script
if __name__ == "__main__":

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.repo and args.date:
        execution_time = timeit.timeit(
            script, number=1
        )  # number specifies how many times to run the function
        print(f"Execution time: {execution_time:.2f} seconds")
