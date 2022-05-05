from dataclasses import dataclass
from pathlib import Path

import subprocess

from bin2coe import convert as bin2coe
from io import BytesIO


@dataclass
class MemoryFile:
    out_file: str
    word_size: int
    word_count: int

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        return b""

    def get_hex_content(self, schematic_folder: Path) -> str:
        stream = BytesIO()
        bin2coe.convert(stream, self.get_raw_content(schematic_folder),
                        self.word_size, self.word_count, 0, 16, mem=True)
        stream.seek(0)
        return stream.read().decode()

    def get_padded_content(self, schematic_folder: Path) -> bytes:
        data = self.get_raw_content(schematic_folder)
        return data.rjust(self.word_size * self.word_count, b'\x00')


@dataclass
class FileRomMemoryFile(MemoryFile):
    path: Path

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        return self.path.read_bytes()


@dataclass
class ComponentMemoryFile(MemoryFile):
    file_name: str

    def get_raw_content(self, schematic_folder: Path) -> bytes:
        path = schematic_folder / self.file_name
        return path.read_bytes()


def translate_path(path):
    from tc2verilog.tc_schematics import ON_WSL
    if ON_WSL:
        return Path(subprocess.check_output(["wslpath", "-u", str(path)]).strip().decode())
    else:
        return Path(path)
