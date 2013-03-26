import os

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

i = 0
for path, dirs, files in os.walk(CURRENT_PATH):
    print(path)
    print(dirs)
    print(files)
    print("---")
    i += 1
    if i >= 6:
        break
