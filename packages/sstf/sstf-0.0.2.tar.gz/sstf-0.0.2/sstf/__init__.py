from pathlib import Path
import psutil
import argparse
from shutil import copyfile


def check_path(path: str) -> Path:
    s = Path(path)
    if s.is_file and s.exists:
        return s
    raise FileNotFoundError(path)


def copy_file(source, target):
    files_and_folders = Path(source).iterdir()
    for name in files_and_folders:
        path = source / name
        if path.is_dir():
            copy_file(path, target)
        elif name.with_suffix(".mp3"):
            dist = target / name.name
            print("Copy " + path.__str__() + " to " + dist.__str__())
            copyfile(path, dist)


def choose_mount_point():
    partitions = psutil.disk_partitions()
    index = 0
    for p in partitions:
        print(p.mountpoint, '   ->   ', index)
        index += 1
    n = int(input("选择你要输出到的挂载点序号: "))
    return Path(partitions[n].mountpoint)


def parse_arg():
    parser = argparse.ArgumentParser(prog="sstf", epilog="* Repository: https://github.com/lxhzzy/sstf")
    parser.add_argument("source", help="音频文件源目录", type=check_path)
    parser.add_argument("-m", "--mount_point", help="输出的挂载点", type=check_path)
    return parser.parse_args()


def main():
    arg = parse_arg()
    if arg.mount_point is not None:
        mount_point = arg.mount_point
    else:
        mount_point = choose_mount_point()

    copy_file(arg.source, mount_point)


if __name__ == "__main__":
    main()
