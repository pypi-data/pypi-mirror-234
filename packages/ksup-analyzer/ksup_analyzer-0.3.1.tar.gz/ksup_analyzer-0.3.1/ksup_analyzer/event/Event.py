import pandas as pd
from datetime import datetime
from ksup_analyzer.event.Result import RaceResult, QualiResult, RaceResultsDataFrame

TRACK_NAMES_BY_REPLAY_NAMES = {
    "sunny-side-track": {"name": "Sunny Side Park", "layouts": {"Path-A": "GP"}},
    "sugar-hill-track": {
        "name": "Sugar Hill",
        "layouts": {"Default-Path": "Full", "Reverse-Path": "Full – Reverse"},
    },
    "maple-ridge-track": {
        "name": "Maple Ridge",
        "layouts": {"Path-A": "Full", "Reverse": "Full – Reverse"},
    },
    "rennvoort-track": {
        "name": "Rennvoort",
        "layouts": {"Path-A": "Full", "Reverse": "Full – Reverse"},
    },
    "rivazza-track": {"name": "Faenza", "layouts": {"Path-A": "GP"}},
    "magdalena-track": {
        "name": "Magdalena",
        "layouts": {"Path-A": "Full", "Path-B": "Club"},
    },
    "copperwood-track": {
        "name": "Cooperwood",
        "layouts": {
            "Path-A": "Full",
            "Path-B": "Club",
            "Full-Reverse": "Full – Reverse",
            "Club-Reverse": "Club – Reverse",
        },
    },
    "siena-track": {
        "name": "Siena",
        "layouts": {"Path-A": "Full", "Reverse": "Reverse"},
    },
    "whistlevalley-track": {
        "name": "Whistle Valley",
        "layouts": {"Path-A": "Full", "Reverse": "Full – Reverse"},
    },
    "hidden-lake-track": {
        "name": "Hidden Lake",
        "layouts": {
            "Path-A": "Standard",
            "Path-B": "Reverse",
        },
    },
    "centrifuge-track": {
        "name": "Centrifuge",
        "layouts": {
            "Path-A": "Standard",
            "Path-B": "Reverse",
            "Path-C": "Club",
            "Path-D": "Club - Reverse",
        },
    },
    "tilksport-track": {
        "name": "Tilksport",
        "layouts": {
            "Path-A": "Full",
            "Path-B": "Club",
            "Path-C": "Rallycross",
            "Full-Reverse": "Full – Reverse",
            "Club-Reverse": "Club – Reverse",
        },
    },
    "thunder-valley-track": {
        "name": "Thunder Point",
        "layouts": {
            "Path-A": "Full",
            "Path-B": "Club",
            "Path-A-Reverse": "Full – Reverse",
            "Path-B-Reverse": "Club – Reverse",
        },
    },
    "oval1-track": {"name": "Bullseye Speedwey", "layouts": {"Path-A": "Oval"}},
    "speedopolis-track": {"name": "Speedopolis", "layouts": {"Path-A": "Oval"}},
    "dirt-oval-track": {"name": "Poke Bowl", "layouts": {"Path-A": "Oval"}},
    "grand-canyon-track": {
        "name": "Interstate",
        "layouts": {"Path-A": "Rallycross", "Reverse": "Rallycross – Reverse"},
    },
    "buffalo-track": {
        "name": "Buffalo Hill",
        "layouts": {"Path-A": "Rallycross", "Path-B": "Club", "Buffalo Hill": "Mini"},
    },
    "lost-lagoons-track": {"name": "Lost Lagoons", "layouts": {"Path-A": "Rallycross"}},
}


class Event:
    def __init__(self, lineup, race, quali=None) -> None:
        self.lineup = lineup
        self.race = race
        self.quali = quali

    def create_result_dataframe(self) -> None:
        # The main result dataframe will be a subclass of pd.DataFrame.
        # This allows us to create custom methods on it.
        race_result_df = RaceResultsDataFrame(
            [result.as_series() for result in self.race.results]
        )

        if self.quali:
            quali_df = pd.concat(
                [result.as_series() for result in self.quali.results], axis=1
            ).transpose()

            race_result_df = race_result_df.join(
                quali_df, lsuffix="_race", rsuffix="_quali"
            )
        else:
            # even if we do not have quali data, we want the race columns to be suffixed in the same way
            race_result_df.columns = [col + "_race" for col in race_result_df.columns]

        lineup_df = pd.concat(
            [driver.as_series() for driver in self.lineup.drivers], axis=1
        ).transpose()

        self.__result_df = race_result_df.join(lineup_df)

    @property
    def result_df(self) -> RaceResultsDataFrame:
        return self.__result_df

    def run_result_calculations(self) -> None:
        self.__result_df._run_result_calculations()


class Session:
    def __init__(self, race_file_content: dict) -> None:
        self.assign_properties(race_file_content)

    def assign_properties(self, r: dict) -> None:
        self.datetime_utc = datetime.strptime(r["timeStampUtc"], "%Y%m%dT%H:%M:%SZ")

        # location = track without layout
        self.location = TRACK_NAMES_BY_REPLAY_NAMES[r["track"]]["name"]
        self.layout = TRACK_NAMES_BY_REPLAY_NAMES[r["track"]]["layouts"][r["path"]]
        # track = location + layout
        self.track = f"{self.location} ({self.layout})"

        rc = r["raceConfiguration"]

        if rc["proximityGhostingMode"] == 1:
            self.collisions = "Prevent All Collisions"
        elif rc["proximityGhostingMode"] == 2:
            self.collisions = "Prevent Lapping Collisions"
        else:
            self.collisions = "All Collisions"

        self.has_wear = rc["wearMode"]
        # self.tire_wear = int(rc["wearCoefficients"]["tireWear"] * 100)
        # self.fuel_use = int(rc["wearCoefficients"]["fuelUse"] * 100)
        # self.vehicle_damage = int(rc["wearCoefficients"]["vehicleDamage"] * 100)
        # self.env_damage = int(rc["wearCoefficients"]["environmentDamage"] * 100)
        self.slipstream = int(rc["geometricSlipStreamCoefficient"] * 100)
        self.rubberbanding = int(rc["standingsSlipStreamCoefficient"] * 100)

        rec = rc["raceEndConditionConfig"]

        if rec["type"] == 1:
            self.length_type = "lap"
            self.length = rec["parameter"]
        elif rec["type"] == 2:
            self.length_type = "minute"
            self.length = rec["parameter"] / 60
        else:
            self.length_type = "km"
            self.length = rec["parameter"] / 1000

        self.length_desc = f"{self.length} {self.length_type}s"

    @property
    def datetime_race(self):
        return self.datetime_utc


class Race(Session):
    def __init__(self, race_file_content: dict) -> None:
        super().__init__(race_file_content)

        self.results = [
            RaceResult(result_dict)
            for result_dict in race_file_content["raceResult"]["racerResults"]
        ]


class Quali(Session):
    def __init__(self, race_file_content: dict) -> None:
        super().__init__(race_file_content)

        self.results = [
            QualiResult(result_dict)
            for result_dict in race_file_content["raceResult"]["racerResults"]
        ]
