import numpy as np
import pandas as pd

pd.set_option("mode.chained_assignment", None)


class Result:
    def __init__(self, results_dict: dict) -> None:
        self.assign_individual_properties(results_dict)
        self.series = None

    def assign_individual_properties(self, res: dict) -> None:
        """
        When it comes to results, there are some that describe the drivers individual performance like lap times
        and some that need more context, namely times of other drivers in order to infer positions for example.

        This method uses the (mostly) individual results given in the replay files. Only exception is the "num_laps_led"
        property which includes knowledge of other drivers times of course.
        """
        self.driver_id = res["racingTeamId"]

        self.starting_position = res["startPositionIndex"] + 1
        # this is the total time from session begin until the driver finsished the last lap
        # this is None if the driver did not finish
        # it does include the time a driver needs in "lap 0" until the beginning of lap 1 (crossing the start/finish line)
        self.total_time = res["finishTime"]
        self.total_time_formatted = "{}:{}.{}".format(
            np.floor(self.total_time / 60).astype(int),
            np.floor(self.total_time % 60).astype(int),
            np.floor((self.total_time - np.floor(self.total_time)) * 1000).astype(int),
        )
        # list of lap times
        self.lap_times = res["lapTimes"]
        # number of laps driven, relevant for lappings
        self.num_laps_driven = len(self.lap_times) if self.lap_times else np.nan
        # minimum lap time
        self.fastest_lap_time = min(self.lap_times) if self.lap_times else np.nan
        # list of time penalties per lap, it does not include hitting CCDs during the race cause that
        # only slows you down (it does not give a time penalty)
        self.lap_time_penalties = res["lapTimePenalties"]
        # how many laps the driver led; interesting in a multi-lap quali
        self.num_laps_led = res["numLapsLed"]
        # metres driven, not sure if relevant
        self.metres_driven = res["metresDriven"]
        # number of track limit penalties
        self.number_track_limit_penalties = res["numTrackLimitsPenalties"]
        # overall track limit penalties in seconds
        self.sum_track_limit_penalties_seconds = res["totalTrackLimitsPenaltySeconds"]
        # number of wall assist penalties
        self.number_track_limit_penalties = res["numWallAssistPenalties"]
        # overall wall assist penalties in seconds
        self.sum_track_limit_penalties_seconds = res["totalWallAssistPenaltySeconds"]

        # as the total time includes the time from the starting position to the start/finish line
        # and the lap times do not, we can extract the time the driver needed to get there
        # This is relevant to calculate positions per lap because we need to add this time to the lap times
        # in order to calculate positions
        self.time_until_starting_line = (
            self.total_time - sum(self.lap_times) if self.total_time else None
        )

    def as_series(self) -> pd.Series:
        if self.series is None:
            property_attributes = [
                attr
                for attr in dir(self)
                if not attr.startswith("__")
                and not callable(getattr(self, attr))
                and attr not in ["series", "driver_id"]
            ]

            indices = property_attributes

            data = [getattr(self, attr) for attr in property_attributes]

            self.series = pd.Series(data=data, index=indices, name=self.driver_id)

        return self.series


class RaceResult(Result):
    def __init__(self, results_dict: dict) -> None:
        super().__init__(results_dict)


class QualiResult(Result):
    def __init__(self, results_dict: dict) -> None:
        super().__init__(results_dict)


class RaceResultsDataFrame(pd.DataFrame):
    # this makes sure that when you would normally construct a new dataframe when applying pandas functions
    # it instead will construct a RaceResultsDataFrame instance making sure that the methods defined below
    # are still available
    @property
    def _constructor(self):
        return RaceResultsDataFrame

    @property
    def has_quali_data(self):
        return any([col.endswith("_quali") for col in self.columns])

    @property
    def participants(self):
        return len(self.index)

    @property
    def lap_position_table(self):
        if "lap_positions_race" not in self.columns:
            self.__calc_lap_positions()
            print(
                "WARNING: You tried to get the lap_position_table before running '__calc_lap_positions()'. I did this for you although you should handle that. Do not run it twice."
            )

        # create lap table dataframe that has a column for every lap and a row for every driver
        df = pd.DataFrame(self["lap_positions_race"].to_list())
        df.index = self["name"]

        # transposed every column name is a driver name and every row index is the laps completed
        df = df.transpose()
        df.index.rename("laps completed", inplace=True)

        return df

    @property
    def gap_to_winner_table(self):
        if "gap_to_winner_race" not in self.columns:
            self.__calc_gap_to_winner()
            print(
                "WARNING: You tried to get the gap_to_winner_table before running '__calc_gap_to_winner()'. I did this for you although you should handle that. Do not run it twice."
            )

        # create lap table dataframe that has a column for every lap and a row for every driver
        df = pd.DataFrame(self["gap_to_winner_race"].to_list())
        df.index = self["name"]

        # transposed every column name is a driver name and every row index is the laps completed
        df = df.transpose()
        df.index.rename("laps completed", inplace=True)

        return df

    @property
    def gap_to_leader_table(self):
        if "gap_to_leader_race" not in self.columns:
            self.__calc_gap_to_leader()
            print(
                "WARNING: You tried to get the gap_to_leader_table before running '__calc_gap_to_leader()'. I did this for you although you should handle that. Do not run it twice."
            )

        # create lap table dataframe that has a column for every lap and a row for every driver
        df = pd.DataFrame(self["gap_to_leader_race"].to_list())
        df.index = self["name"]

        # transposed every column name is a driver name and every row index is the laps completed
        df = df.transpose()
        df.index.rename("laps completed", inplace=True)

        return df

    def _run_result_calculations(self) -> None:
        """
        Until this point self is a pandas dataframe with all the information from the header file(s).

        These are the columns which are available (the _quali columns only if a quali header files was provided):
        - 'starting_position_race'
        - 'fastest_lap_time_race'
        - 'lap_time_penalties_race'
        - 'lap_times_race'
        - 'metres_driven_race'
        - 'num_laps_driven_race'
        - 'num_laps_led_race'
        - 'time_until_starting_line_race'
        - 'total_time_race'
        - 'total_time_formatted_race'
        - 'number_track_limit_penalties_race'
        - 'sum_track_limit_penalties_seconds_race'
        - 'number_track_limit_penalties_race'
        - 'sum_track_limit_penalties_seconds_race'

        - 'fastest_lap_time_quali'
        - 'lap_time_penalties_quali'
        - 'lap_times_quali'
        - 'metres_driven_quali'
        - 'num_laps_driven_quali'
        - 'num_laps_led_quali'
        - 'time_until_starting_line_quali'
        - 'total_time_quali'
        - 'total_time_formatted_quali'
        - 'number_track_limit_penalties_quali'
        - 'sum_track_limit_penalties_seconds_quali'
        - 'number_track_limit_penalties_quali'
        - 'sum_track_limit_penalties_seconds_quali'

        - 'car'
        - 'colors'
        - 'is_ai'
        - 'name'
        - 'platform'
        - 'vehicle_colors'

        Now it is about calculating more valuable variables out of the data available, f.e. positions per lap.
        """
        self.__calc_race_position()
        self.__interpolate_time_until_starting_line_race()
        self.__calc_lap_positions()
        self.__calc_gap_to_winner()
        self.__calc_gap_to_leader()
        self.__calc_slowest_lap_time()
        self.__calc_median_lap_time()

    def __calc_slowest_lap_time(self):
        # provide slowest lap but exclude lap 1 (due to accelaration)
        self["slowest_lap_time_race"] = np.max(
            self["lap_times_race"].apply(lambda x: x[1:]).to_list(), axis=1
        )

    def __calc_median_lap_time(self):
        # provide median lap but exclude lap 1 (due to accelaration)
        self["median_lap_time_race"] = np.median(
            self["lap_times_race"].apply(lambda x: x[1:]).to_list(), axis=1
        )

    def __calc_race_position(self):
        self.sort_values(
            by=["num_laps_driven_race", "total_time_race", "starting_position_race"],
            ascending=[False, True, True],
            inplace=True,
        )
        self["end_position_race"] = list(range(1, len(self.index) + 1))

    def __interpolate_time_until_starting_line_race(self):
        # creating a series to create an index with equal distances for interpolation
        time_until_starting_line_race = self["time_until_starting_line_race"]
        time_until_starting_line_race.index = list(range(1, len(self.index) + 1))

        # spline is able to extrapolate as well
        # order 2 as the speed difference drivers have when crossing the start finish line decreases
        # the further back you go in the starting grid (P1 much slower than P2 but P11 and P12 similar if not identical)
        self[
            "time_until_starting_line_race"
        ] = time_until_starting_line_race.interpolate(
            method="spline", order=2, inplace=False
        ).values

    def __calc_lap_positions(self):
        """
        We want to calculate the position of each car on each lap and add a list of positions as a new column in self.
        In order reduce complexity we will create another dataframe called df that only holds the information we need.
        """

        # remove those that have no lap times and reduce the columns to what we really need
        df = self.loc[
            ~self["lap_times_race"].isna(),
            [
                "name",
                "time_until_starting_line_race",
                "lap_times_race",
                "starting_position_race",
                "end_position_race",
            ],
        ]

        df_lap_times = pd.DataFrame(df["lap_times_race"].to_list())
        df_lap_times.index = df.index

        df_lap_times = pd.concat(
            [df["time_until_starting_line_race"], df_lap_times],
            axis=1,
            ignore_index=True,
        )
        df_lap_times = df_lap_times.cumsum(axis=1)
        df = pd.concat([df, df_lap_times], axis=1)
        del df["lap_times_race"]

        # now we have a df with the team id as an index and the lap numbers (from 0 to e.g. 10) as a column
        # we do know the starting positions and the finishing positions already via the "starting_position" / "race_position" columns within df

        for col in df_lap_times.columns:
            df.sort_values(by=col, inplace=True)
            df[f"Lap {col}"] = list(range(1, len(df.index) + 1))
            df.loc[df[col].isnull(), f"Lap {col}"] = np.NaN
            col_pos_last_lap = f"Lap {col}"

        for _, row in df[["name", col_pos_last_lap, "end_position_race"]].iterrows():
            if np.isnan(row[col_pos_last_lap]):
                continue

            if row[col_pos_last_lap] != row["end_position_race"]:
                print(
                    f'Calculated position seems to be incorrect. Expected pos {row["end_position_race"]} at the end for {row["name"]} but found {row[col_pos_last_lap]}.'
                )

        df.sort_values(by="end_position_race", inplace=True)

        df[col_pos_last_lap] = df["end_position_race"]

        df_lap_table = df.loc[
            :,
            ["starting_position_race"]
            + [
                col
                for col in df.columns
                if isinstance(col, str) and col.startswith("Lap") and col != "Lap 0"
            ],
        ]

        # if someone has been lapped we want to see the final position anyways
        # example: there are 20 laps and someone did 18. We know his position until lap 18 and in the finish (lap 20)
        # therefore when backfilling we fill lap 19 position with the position at lap 20 cause that should be the same
        df_lap_table = df_lap_table.bfill(axis=1)

        # add the lap positions in a column of self as a list
        df_lap_table["lap_positions_race"] = df_lap_table.values.tolist()

        self["lap_positions_race"] = np.nan

        for i, value in df_lap_table["lap_positions_race"].items():
            # simply assigning a list does not work unfortunately:
            # error: ValueError: Must have equal len keys and value when setting with an iterable
            self.loc[self.index == i, "lap_positions_race"] = self.loc[
                self.index == i, "lap_positions_race"
            ].apply(lambda _: value)

    def __calc_gap_to_winner(self):
        """
        We want to calculate the gap to the winner of each car on each lap and add a list of gaps as a new column in self.
        In order reduce complexity we will create another dataframe called df that only holds the information we need.
        """

        # remove those that have no lap times and reduce the columns to what we really need
        df = self.loc[
            ~self["lap_times_race"].isna(),
            [
                "name",
                "time_until_starting_line_race",
                "lap_times_race",
                "starting_position_race",
                "end_position_race",
            ],
        ]

        df_lap_times = pd.DataFrame(df["lap_times_race"].to_list())
        df_lap_times.index = df.index

        df_lap_times = pd.concat(
            [df["time_until_starting_line_race"], df_lap_times],
            axis=1,
            ignore_index=True,
        )
        df_lap_times = df_lap_times.cumsum(axis=1)
        df = pd.concat([df, df_lap_times], axis=1)
        del df["lap_times_race"]

        # now we have a df with the team id as an index and the lap numbers (from 0 to e.g. 10) as a column
        # we do know the starting positions and the finishing positions already via the "starting_position" / "race_position" columns within df

        for col in df_lap_times.columns:
            df[f"Lap {col}"] = 0
            for idx in range(len(df.index)):
                df[f"Lap {col}"][idx] = df[col][idx] - df[col][0]
            df.loc[df[col].isnull(), f"Lap {col}"] = np.NaN

        df_gap_table = df.loc[
            :,
            [
                col
                for col in df.columns
                if isinstance(col, str) and col.startswith("Lap")
            ],
        ]

        df_gap_table = df_gap_table.bfill(axis=1)

        # add the gaps in a column of self as a list
        df_gap_table["gap_to_winner_race"] = df_gap_table.values.tolist()

        self["gap_to_winner_race"] = np.nan

        for i, value in df_gap_table["gap_to_winner_race"].items():
            # simply assigning a list does not work unfortunately:
            # error: ValueError: Must have equal len keys and value when setting with an iterable
            self.loc[self.index == i, "gap_to_winner_race"] = self.loc[
                self.index == i, "gap_to_winner_race"
            ].apply(lambda _: value)

        # in order to make the gap at the end more visible, let's provide a column just for that
        self["gap_to_winner_finish_race"] = self["gap_to_winner_race"].apply(
            lambda x: x[-1] if x else np.nan
        )

    def __calc_gap_to_leader(self):
        """
        We want to calculate the gap to the leader of each car on each lap and add a list of gaps as a new column in self.
        In order reduce complexity we will create another dataframe called df that only holds the information we need.
        """

        # remove those that have no lap times and reduce the columns to what we really need
        df = self.loc[
            ~self["lap_times_race"].isna(),
            [
                "name",
                "time_until_starting_line_race",
                "lap_times_race",
                "starting_position_race",
                "end_position_race",
            ],
        ]

        df_lap_times = pd.DataFrame(df["lap_times_race"].to_list())
        df_lap_times.index = df.index

        df_lap_times = pd.concat(
            [df["time_until_starting_line_race"], df_lap_times],
            axis=1,
            ignore_index=True,
        )
        df_lap_times = df_lap_times.cumsum(axis=1)
        df = pd.concat([df, df_lap_times], axis=1)
        del df["lap_times_race"]

        # now we have a df with the team id as an index and the lap numbers (from 0 to e.g. 10) as a column
        # we do know the starting positions and the finishing positions already via the "starting_position" / "race_position" columns within df

        for col in df_lap_times.columns:
            df.sort_values(by=col, inplace=True)
            df[f"Lap {col}"] = 0.0
            for idx in range(len(df.index)):
                df.at[idx, f"Lap {col}"] = df[col].iloc[idx] - df[col].iloc[0]
            df.loc[df[col].isnull(), f"Lap {col}"] = np.NaN

        df.sort_values(by="end_position_race", inplace=True)

        df_gap_table = df.loc[
            :,
            [
                col
                for col in df.columns
                if isinstance(col, str) and col.startswith("Lap")
            ],
        ]

        df_gap_table = df_gap_table.bfill(axis=1)

        # add the gap in a column of self as a list
        df_gap_table["gap_to_leader_race"] = df_gap_table.values.tolist()

        self["gap_to_leader_race"] = np.nan

        for i, value in df_gap_table["gap_to_leader_race"].items():
            # simply assigning a list does not work unfortunately:
            # error: ValueError: Must have equal len keys and value when setting with an iterable
            self.loc[self.index == i, "gap_to_leader_race"] = self.loc[
                self.index == i, "gap_to_leader_race"
            ].apply(lambda _: value)
