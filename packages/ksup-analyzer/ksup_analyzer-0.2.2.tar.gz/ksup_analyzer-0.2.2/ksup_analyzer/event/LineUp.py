from ksup_analyzer.event.Driver import Driver


class LineUp:
    def __init__(self, race_file_content: dict) -> None:
        self.assign_properties(race_file_content)

    def assign_properties(self, r: dict) -> None:
        self.drivers = [
            Driver(did, driver_dict) for did, driver_dict in r["configsById"].items()
        ]

    def __str__(self) -> str:
        return ",".join([str(driver) for driver in self.drivers])
