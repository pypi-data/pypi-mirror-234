import pandas as pd

CAR_NAMES_BY_REPLAY_NAME = {
    "standard-kart": "Standard Kart",
}


class Driver:
    def __init__(self, driver_id: str, driver_replay_dict: dict) -> None:
        self.assign_properties(driver_id, driver_replay_dict)
        self.series = None

    def assign_properties(self, did: str, d: dict) -> None:
        self.id = did

        self.name = d["racerName"]
        self.platform = d["platform"]
        self.is_ai = d["isAITeam"]

        self.colors = d["driverSkinLivery"][1]
        self.vehicle_colors = d["vehicleLivery"][1]

        self.car = CAR_NAMES_BY_REPLAY_NAME[d["vehicle"]]

    def as_series(self) -> pd.Series:
        if self.series is None:
            property_attributes = [
                attr
                for attr in dir(self)
                if not attr.startswith("__")
                and not callable(getattr(self, attr))
                and attr not in ["series", "id"]
            ]

            indices = property_attributes

            data = [getattr(self, attr) for attr in property_attributes]

            self.series = pd.Series(data=data, index=indices, name=self.id)

        return self.series

    def __str__(self) -> str:
        return self.name
