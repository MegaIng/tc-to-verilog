from dataclasses import dataclass, field
from pathlib import Path

import subprocess

from bin2coe import convert as bin2coe
from io import BytesIO


@dataclass
class MemoryFile:
    out_file: str
    word_size: int
    word_count: int
    schematic_folder: Path = field(init=False, default=None)

    def get_raw_content(self, level_id: int = 86, schematic_folder: Path = None) -> bytes:
        return b""

    def get_hex_content(self, level_id: int = 86, schematic_folder: Path = None) -> str:
        stream = BytesIO()
        bin2coe.convert(stream, self.get_raw_content(level_id, schematic_folder),
                        self.word_size, self.word_count, 0, 16, mem=True)
        stream.seek(0)
        return stream.read().decode()

    def get_padded_content(self, level_id: int = 86, schematic_folder: Path = None) -> bytes:
        data = self.get_raw_content(level_id, schematic_folder)
        return data.ljust(self.word_size * self.word_count, b'\x00')


@dataclass
class FileRomMemoryFile(MemoryFile):
    path: Path

    def get_raw_content(self, level_id: int = 86, schematic_folder: Path = None) -> bytes:
        return self.path.read_bytes()


@dataclass
class ComponentMemoryFile(MemoryFile):
    file_name: str

    def get_raw_content(self, level_id: int = 86, schematic_folder: Path = None) -> bytes:
        if not schematic_folder:
            return b""
        path = (schematic_folder or self.schematic_folder) / self.file_name
        return path.read_bytes()


@dataclass
class ProgramMemoryFile(MemoryFile):
    program_mapping: dict[int, str]

    def get_raw_content(self, level_id: int = 86, schematic_folder: Path = None) -> bytes:
        schematic_folder = (schematic_folder or self.schematic_folder)
        if not schematic_folder:
            return b""
        name = self.program_mapping.get(level_id, "new_program")
        file = (schematic_folder / f"{name}.bin")
        if file.is_file():
            return file.read_bytes()
        else:
            return b""


def translate_path(path):
    from tc2verilog.tc_schematics import ON_WSL
    if ON_WSL:
        return Path(subprocess.check_output(["wslpath", "-u", str(path)]).strip().decode())
    else:
        return Path(path)
