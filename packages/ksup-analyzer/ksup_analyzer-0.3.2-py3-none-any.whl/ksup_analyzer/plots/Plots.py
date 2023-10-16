from ksup_analyzer.event.Result import RaceResultsDataFrame

import matplotlib.pyplot as plt
import numpy as np


class LapPositionTablePlot:
    def __init__(self, df: RaceResultsDataFrame, race) -> None:
        self.legend = df["name"]
        self.lap_position = df.lap_position_table
        self.race = race

    def plot(self, fileprefix=None):
        fig = plt.figure(layout="constrained")
        fig.set_size_inches(20, 10)  # size of figure
        plt.rc("grid", linestyle=":", color="black")  # style of grid

        ax = plt.subplot(111)
        ax.plot(self.lap_position, linewidth=2)
        ax.set_xlabel("Laps", fontsize=20)
        ax.set_ylabel("Position", fontsize=20)
        ax.grid(True)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(self.legend, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16)

        x_labels = ["Start"]
        for lap in range(len(self.lap_position) - 1):
            x_labels.append(f"Lap {lap+1}")

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
        ax.set_yticks(np.arange(0, 12))
        ax.set_ylim(12, 0)

        plt.setp(ax.get_xticklabels(), rotation=90)
        # plt.show()
        dt = self.race.datetime_race
        if fileprefix == None:
            fig.savefig(
                f"export//{dt.strftime('%d_%m_%Y_%H_%M_%S')}_LapPosition.png", dpi=150
            )
        else:
            fig.savefig(f"export//{fileprefix}_LapPosition.png", dpi=150)


class GapToWinnerTablePlot:
    def __init__(self, df: RaceResultsDataFrame, race) -> None:
        self.legend = df["name"]
        self.gap_table = df.gap_to_winner_table
        self.race = race

    def plot(self, ymin=-15, ymax=15, fileprefix=None):
        fig = plt.figure(layout="constrained")
        fig.set_size_inches(20, 10)  # size of figure
        plt.rc("grid", linestyle=":", color="black")  # style of grid

        ax = plt.subplot(111)
        ax.plot(self.gap_table, linewidth=2)
        ax.set_xlabel("Laps", fontsize=20)
        ax.set_ylabel("Gap to winner (s)", fontsize=20)
        ax.grid(True)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(self.legend, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16)

        x_labels = ["Start"]
        for lap in range(len(self.gap_table) - 1):
            x_labels.append(f"Lap {lap+1}")

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
        ax.set_yticks(np.arange(ymin, ymax))
        ax.set_ylim(ymax, ymin)

        plt.setp(ax.get_xticklabels(), rotation=90)
        dt = self.race.datetime_race
        if fileprefix == None:
            fig.savefig(
                f"export//{dt.strftime('%d_%m_%Y_%H_%M_%S')}_GapToWinner.png", dpi=150
            )
        else:
            fig.savefig(f"export//{fileprefix}_GapToWinner.png", dpi=150)


class GapToLeaderTablePlot:
    def __init__(self, df: RaceResultsDataFrame, race) -> None:
        self.legend = df["name"]
        self.gap_table = df.gap_to_leader_table
        self.race = race

    def plot(self, ymin=-1, ymax=30, fileprefix=None):
        fig = plt.figure(layout="constrained")
        fig.set_size_inches(20, 10)  # size of figure
        plt.rc("grid", linestyle=":", color="black")  # style of grid

        ax = plt.subplot(111)
        ax.plot(self.gap_table, linewidth=2)
        ax.set_xlabel("Laps", fontsize=20)
        ax.set_ylabel("Gap to leader (s)", fontsize=20)
        ax.grid(True)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(self.legend, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16)

        x_labels = ["Start"]
        for lap in range(len(self.gap_table) - 1):
            x_labels.append(f"Lap {lap+1}")

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
        ax.set_yticks(np.arange(ymin, ymax))
        ax.set_ylim(ymax, ymin)

        plt.setp(ax.get_xticklabels(), rotation=90)
        dt = self.race.datetime_race
        if fileprefix == None:
            fig.savefig(
                f"export//{dt.strftime('%d_%m_%Y_%H_%M_%S')}_GapToLeader.png", dpi=150
            )
        else:
            fig.savefig(f"export//{fileprefix}_GapToLeader.png", dpi=150)
