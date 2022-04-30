from dataclasses import dataclass
from pathlib import Path

import subprocess

from tc2verilog.tc_schematics import ON_WSL


@dataclass
class MemoryFile:
    out_file: str
    word_size: int
    word_count: int

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        return b""


@dataclass
class FileRomMemoryFile(MemoryFile):
    path: Path

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        if ON_WSL:
            path = Path(subprocess.check_output(["wslpath", "-u", str(self.path)]).strip().decode())
        else:
            path = self.path
        return path.read_bytes()


@dataclass
class ComponentMemoryFile(MemoryFile):
    file_name: str

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        path = schematic_folder / self.file_name
        return path.read_bytes()


def translate_path(path):
    if ON_WSL:
        return Path(subprocess.check_output(["wslpath", "-u", str(path)]).strip().decode())
    else:
        return path
