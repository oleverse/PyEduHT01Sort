from functions import get_file_list


scan_dir = "/tmp/test_dir"

file_list = get_file_list(scan_dir)

for key, val in file_list.items():
   print(f"{key} ->")
   for each in val:
     print(each)