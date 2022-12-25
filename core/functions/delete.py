import os
import pathlib
import stat


def delete_folder(pth: pathlib.Path) -> None:
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            try:
                sub.unlink()
            except OSError:
                os.chmod(sub, stat.S_IWUSR)
                sub.unlink()
    pth.rmdir()
