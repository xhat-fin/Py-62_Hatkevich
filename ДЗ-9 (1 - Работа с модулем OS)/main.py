import os
from collections import Counter


print(f'Операционная система: {os.name}')

print(f'Путь к рабочей папке: {os.getcwd()}')

def new_dirs(path):
    new_dir = []
    full_files = []
    for file in os.listdir(path):
        if os.path.isfile(file):
            full_files.append(file.split('.'))
            new_dir.append(file.split('.')[-1])
    return list(dict.fromkeys(new_dir)), full_files


def make_new_dirs(list_dirs):
    for dir1 in list_dirs:
        path_dir = os.path.join(os.getcwd(), dir1)
        if os.path.exists(path_dir) is False:
            os.mkdir(path_dir)


def count_files(ls, path):
    ext_file = []
    for l in ls:
        if len(l) > 1:
            ext_file.append(l[-1])
    ext_file_dict = dict(Counter(ext_file))

    file_size = {}
    for l in ls:
        if l[-1] not in file_size:
            file_size[l[-1]] = os.path.getsize(os.path.join(path, '.'.join(l)))
        else:
            file_size[l[-1]] += os.path.getsize(os.path.join(path, '.'.join(l)))
    return ext_file_dict, file_size


new_dir, full_files = new_dirs(os.getcwd())
count_file, file_size = count_files(full_files, os.getcwd())


make_new_dirs(new_dir)
for file in full_files:
    index_dir = os.listdir(os.getcwd()).index(file[-1])
    os.rename(os.path.join(os.getcwd(), '.'.join(file)),
              os.path.join(os.getcwd(), os.listdir(os.getcwd())[index_dir], '.'.join(file)))

for i in count_file:
    print(f"В папку {i} было перемещено {count_file[i]} файлов в размере {file_size[i]} байт")

# print(new_dir)


for dirr in new_dir:
    print(f'файл {os.listdir(os.path.join(os.getcwd(), dirr))[0]}'
          f' переименован в same_{os.listdir(os.path.join(os.getcwd(), dirr))[0]}')
    
    os.rename(os.path.join(os.getcwd(), dirr, f'{os.listdir(os.path.join(os.getcwd(), dirr))[0]}'),
              os.path.join(os.getcwd(), dirr, f'same_{os.listdir(os.path.join(os.getcwd(), dirr))[0]}'))
