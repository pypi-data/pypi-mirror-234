from pathlib import Path
from typing import List
from ksup_analyzer.replay.ReplayFile import QualiFile, RaceFile


class FileHandler:
    def __init__(self, file_paths: List[Path]) -> None:
        self.file_paths = [Path(file_path) for file_path in file_paths]
        self._quali_file, self._race_file = self.assign_files(self.file_paths)

    def get_quali_file_content(self):
        return self._quali_file.content

    def get_race_file_content(self):
        return self._race_file.content

    def assign_files(self, file_paths: List[Path]):
        self.check_input_files(file_paths)

        quali_file = None
        race_file = None

        for file_path in file_paths:
            with open(file_path, "r") as file:
                file_content = file.read()

                if (
                    '\\"text\\":\\"Qualifying\\"' in file_content
                    or '\\"text\\":\\"Qualifier\\"' in file_content
                ):
                    quali_file = QualiFile(self, file_content)
                elif '\\"text\\":\\"Race\\"' in file_content:
                    race_file = RaceFile(self, file_content)
                else:
                    raise Exception("Did not find keywords in the files ")

        assert (
            race_file is not None
        ), "Did not find a race file! Check your input files!"

        return quali_file, race_file

    def check_input_files(self, file_paths: List[Path]):
        assert len(file_paths) in [
            1,
            2,
        ], "You can pass up to two files. One (optional) qualifying file and one mandatory race replay .header file."

        assert all(
            file_path.suffix == ".header" for file_path in file_paths
        ), "The file(s) you provided are not .header files!"

        if len(file_paths) == 2:
            assert file_paths[0] != file_paths[1], "You provided the same file twice!"
