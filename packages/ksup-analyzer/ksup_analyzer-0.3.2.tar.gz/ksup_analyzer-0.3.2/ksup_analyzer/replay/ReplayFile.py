import json


class ReplayFile:
    def __init__(self, file_handler, file_content_raw: str) -> None:
        self.file_handler = file_handler
        self.content = self.read_content(file_content_raw)

    def read_content(self, file_content_raw: str) -> dict:
        file_content_str = self.convert_to_valid_json(file_content_raw)
        file_content_json = json.loads(file_content_str)
        self.double_check_json_content(file_content_json)
        return file_content_json

    def convert_to_valid_json(self, file_content_raw: str) -> str:
        """
        The content of the json files is not 100% valid json format.
        So to read it with json.loads() we first need to get rid of some backslashes and
        some double quotes around the raceConfiguration.
        """
        return (
            file_content_raw.replace("\\", "")
            .replace('"raceConfiguration":"', '"raceConfiguration":')
            .replace('"raceConfiguration": "', '"raceConfiguration": ')
            .replace('}","track":', '},"track":')
        )


class QualiFile(ReplayFile):
    def __init__(self, file_handler, file_content_raw: str) -> None:
        super().__init__(file_handler, file_content_raw)

    def double_check_json_content(self, file_content_json: dict) -> None:
        assert file_content_json["raceConfiguration"]["eventName"]["text"] in [
            "Qualifying",
            "Qualifier",
        ], "This does not seem to be a quali file!"


class RaceFile(ReplayFile):
    def __init__(self, file_handler, file_content_raw: str) -> None:
        super().__init__(file_handler, file_content_raw)

    def double_check_json_content(self, file_content_json: dict) -> None:
        assert file_content_json["raceConfiguration"]["eventName"]["text"] in [
            "Race"
        ], "This does not seem to be a race file!"
