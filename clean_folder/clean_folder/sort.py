import sys
from clean_folder.functions import get_file_list


def do_cleaning():
  scan_dir = None

  if len(sys.argv) == 1:
    print("Можна передати шлях до каталогу у якості праметра командного рядка наступним чином:")
    print(f"\n\tpython {sys.argv[0]} <шлях_до_каталогу>\n")
    print("або ввести з клавіатури нижче.\n")
    try:
      scan_dir = input("Введіть шлях до каталогу: ")
    except KeyboardInterrupt:
      print("")
      exit()
  else:
    scan_dir = sys.argv[1]

  try:
    file_list = get_file_list(scan_dir)

    for key, val in file_list.items():
      print(f"{key} ->")
      for each in val:
        print(each)
  except Exception as ex:
    print(ex)