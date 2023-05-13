import sys
from clean_folder.functions import do_arrange, remove_empty_dirs


def ask_path():
    print("Можна передати шлях до каталогу у якості праметра командного рядка наступним чином:")
    print(f"\n\tpython {sys.argv[0]} <шлях_до_каталогу>\n")
    print("або ввести з клавіатури нижче.\n")

    try:
        return input("Введіть шлях до каталогу: ").strip()
    except KeyboardInterrupt:
        print("\nInterrupted by user!")


def print_results(file_list):
    if file_list:
        for key, val in file_list.items():
            print(f"{key}:")
            print(*[f'{i["path"]} -> {i["new_path"]}' for i in val], sep="\n")


def arrange_dir():
    scan_dir = ask_path() if len(sys.argv) == 1 else sys.argv[1]

    try:
        file_list = do_arrange(scan_dir)
    except Exception as ex:
        print(ex)
    else:
        print_results(file_list)

    print("\nRemoving empty directories:")
    remove_empty_dirs(scan_dir)


if __name__ == "__main__":
    arrange_dir()
