
import pathlib,shutil,os


def remove_cache_files():
    for i in pathlib.Path(".").rglob("__pycache__"):
        print(i)
        shutil.rmtree(i)


if __name__ == "__main__" :
    remove_cache_files()
