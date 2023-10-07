import json

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas import job as job_schema

from oqtant.schemas.interpolation import interpolate_1d, interpolate_1d_list


class Snapshot(job_schema.Landscape):
    """A class that represents a painted optical landscape / potential at a single
    point in (experiment stage) time.
    """

    @classmethod
    def new(
        cls,
        time: float = 0,
        positions: list = [-10, 10],
        potentials: list = [0, 0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        return cls(
            time_ms=time,
            positions_um=positions,
            potentials_khz=potentials,
            spatial_interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, landscape: job_schema.Landscape):
        return cls(**landscape.model_dump())

    def get_potential(self, positions: list) -> list:
        """Samples the potential energy of this snapshot at the specified positions
        Args:
            positions (list): List of positions (in microns).
        Returns:
            list: Value of potential energy (in kHz) at the specified positions.
        """
        potentials = interpolate_1d_list(
            self.positions_um,
            self.potentials_khz,
            positions,
            self.spatial_interpolation,
        )
        return list(np.clip(potentials, 0.0, 100.0))

    def show_potential(self):
        """Plots the potential energy as a function of position for this snapshot"""
        positions = np.arange(-60, 60, 1, dtype=float)
        fig, ax = plt.subplots()
        lns = []
        labs = []
        plt.plot(positions, self.get_potential(positions))
        plt.plot(self.positions_um, self.get_potential(self.positions_um), ".")
        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Snapshot potential energy profile")
        plt.xlim([-61, 61])
        plt.ylim([-1, 101])
        ax.legend(lns, labs, loc=0)
        plt.show()


# (potentially) dynamic landscape made up of snapshots
class Landscape(job_schema.OpticalLandscape):
    """Class that represents a dynamic painted-potential optical landscape constructed
    from individual (instantaneous time) Snapshots
    """

    @classmethod
    def new(
        cls,
        snapshots: list[Snapshot] = [
            Snapshot.new(time=0),
            Snapshot.new(time=2),
        ],
    ):
        optical_landscapes = []
        for snapshot in snapshots:
            optical_landscapes.append(
                job_schema.Landscape(
                    time_ms=snapshot.time_ms,
                    positions_um=snapshot.positions_um,
                    potentials_khz=snapshot.potentials_khz,
                    spatial_interpolation=snapshot.spatial_interpolation,
                )
            )
        return cls(landscapes=optical_landscapes)

    @classmethod
    def from_input(cls, landscape: job_schema.OpticalLandscape):
        """
        Create an instance of the class using the provided `landscape` object.

        Parameters:
            - landscape (job_schema.OpticalLandscape): The landscape object to create the instance from.

        Returns:
            - cls: An instance of the class created using the `landscape` object.
        """
        return cls(**json.loads(landscape.model_dump_json()))

    # extract Snapshot abstract objects from backend data structure
    @property
    def snapshots(self) -> list[Snapshot]:
        """
        Returns: A list of Snapshot objects.
        """
        return [Snapshot(**landscape.model_dump()) for landscape in self.landscapes]

    def get_potential(
        self, time: float, positions: list = list(np.linspace(-50, 50, 101))
    ) -> list:
        """Calculates potential energy at the specified time and positions.
        Args:
            time (float):
                Time (in ms) at which the potential energy is calculated.
            positions (list, optional):
                Positions at which the potential energy is calculated.
                Defaults to np.linspace(-100, 100, 201).
        Returns:
            list: Potential energies (in kHz) at specified time and positions.
        """
        potentials = [0] * len(positions)
        snaps = self.snapshots
        if len(snaps) < 2:
            return potentials
        snap_times = [snap.time_ms for snap in snaps]
        if time >= min(snap_times) and time <= max(snap_times):
            pre = next(snap for snap in snaps if snap.time_ms <= time)
            nex = next(snap for snap in snaps if snap.time_ms >= time)
            ts = [pre.time_ms, nex.time_ms]
            pots = [
                interpolate_1d(ts, [p1, p2], time, self.interpolation)
                for p1, p2 in zip(
                    pre.get_potential(positions), nex.get_potential(positions)
                )
            ]
            current = Snapshot.new(
                time=time, positions=list(positions), potentials=pots
            )
            potentials = current.get_potential(positions)
            np.clip(potentials, 0.0, 100.0)
        return potentials

    def show_potential(self, times: list):
        """Plots the potential energy as a function of position at the specified times.

        Args:
            times (list): times (in ms) at which to evaluate the potential energy landscape.
        """
        positions = np.arange(-60, 60, 1, dtype=float)
        fig, ax = plt.subplots()
        lns = []
        labs = []
        for time in times:
            potentials = self.get_potential(time, positions)
            np.clip(potentials, 0, 100)
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(positions, potentials, color=color)
            lns.append(ln)
            labs.append("t=" + str(time))
        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Landscape potential energy profile")
        plt.xlim([-61, 61])
        plt.ylim([-1, 101])
        ax.legend(lns, labs, loc=0)
        plt.show()


class Barrier(job_schema.Barrier):
    """Class that represents a painted optical barrier."""

    @classmethod
    def new(
        cls,
        position: float = 0,
        height: float = 0,
        width: float = 1,
        birth: float = 0,
        lifetime: float = 0,
        shape: job_schema.ShapeType = job_schema.ShapeType.GAUSSIAN,
        interpolation: job_schema.InterpolationType = job_schema.InterpolationType.LINEAR,
    ):
        if lifetime == 0:
            data = {
                "times_ms": [birth],
                "positions_um": [position],
                "heights_khz": [height],
                "widths_um": [width],
                "shape": shape,
                "interpolation": interpolation,
            }
        else:
            data = {
                "times_ms": [birth, birth + lifetime],
                "positions_um": [position] * 2,
                "heights_khz": [height] * 2,
                "widths_um": [width] * 2,
                "shape": shape,
                "interpolation": interpolation,
            }

        return cls(**data)

    @property
    def lifetime(self) -> float:
        """Extract the Barrier lifetime.

        Returns:
            float: Amount of time (in ms) that Barrier object will exist.
        """
        return self.death - self.birth

    @property
    def birth(self) -> float:
        """Extract the (experiment stage) time that the Barrier will be created.

        Returns:
            float: Time (in ms) at which the Barrier will start being projected.
        """
        return min(self.times_ms)

    @property
    def death(self) -> float:
        """Extract the (experiment stage) time that the Barrier will cease to exist.

        Returns:
            float: Time (in ms) at which the Barrier will stop being projected.
        """
        return max(self.times_ms)

    def evolve(self, duration: float, position=None, height=None, width=None):
        """Evolve the position, height, and/or width of a Barrier over a duration.
        Used to script a Barrier's behavior.

        Args:
            duration (float): Time (in ms) over which evolution should take place.
            position (float, optional): Position, in microns, to evolve to.
                                        Defaults to None (position remains unchanged).
            height (float, optional): Height, in kHz, to evolve to.
                                        Defaults to None (height remains unchanged).
            width (float, optional): Width, in microns, to evolve to.
                                        Defaults to None (width remains unchanged).
        """
        if position is None:
            position = self.positions_um[-1]
        if height is None:
            height = self.heights_khz[-1]
        if width is None:
            width = self.widths_um[-1]
        self.positions_um.append(position)
        self.heights_khz.append(height)
        self.widths_um.append(width)
        self.times_ms.append(self.times_ms[-1] + duration)

    def is_active(self, time: float) -> bool:
        """Queries if the barrier is active (exists) at the specified time
        Args:
            time (float): Time (in ms) at which the query is evaluated.
        Returns:
            bool: True if the barrier exists at the specified time.
        """
        return time >= self.times_ms[0] and time <= self.times_ms[-1]

    def get_positions(self, times: list, corrected: bool = False) -> list:
        """Calculate barrier position at the specified (experiment stage) times.

        Args:
            times (float): Times (in ms) at which positions are calculated.
        Returns:
            list: Barrier positions (in microns) at desired times.
        """
        if corrected:
            times = list(np.round(np.asarray(times), 1))
        return interpolate_1d_list(
            self.times_ms, self.positions_um, times, self.interpolation
        )

    def get_heights(self, times: list, corrected: bool = False) -> list:
        """Get barrier heights at the specified list of times

        Args:
            times (float): Times (ms) at which the heights are calculated.
        Returns:
            list: Barrier heights (kHz) at desired times.
        """
        if corrected:
            times = list(np.round(np.asarray(times), 1))
        return interpolate_1d_list(
            self.times_ms, self.heights_khz, times, self.interpolation
        )

    def get_widths(self, times: list, corrected: bool = False) -> list:
        """Get barrier widths at the specified list of times

        Args:
            times (float): Times (ms) at which the widths are calculated.
        Returns:
            list: Barrier widths (in microns) at desired times.
        """
        if corrected:
            times = list(np.round(np.asarray(times), 1))
        return interpolate_1d_list(
            self.times_ms, self.widths_um, times, self.interpolation
        )

    def get_potential(
        self, time: float, positions: list = range(-50, 51, 1), corrected: bool = False
    ) -> list:
        """Barrier potential energy at given positions at the specified time

        Args:
            time_ms (float): Time (in ms) at which the potential is calculated
            positions_um (list, optional):
                Positions (um) at which the potential energies are evaluated.
                Defaults to range(-50, 51, 1).

        Returns:
            list: Potential energies (in kHz) at the input positions
        """
        h = self.get_heights([time], corrected)[0]
        p = self.get_positions([time], corrected)[0]
        w = self.get_widths([time], corrected)[0]
        pots = [0] * len(positions)
        if h <= 0 or w <= 0 or not self.is_active(time):
            return pots
        if self.shape == "SQUARE":  # width = half width
            pots = [0 if (x < p - w or x > p + w) else h for x in positions]
        elif self.shape == "LORENTZIAN":  # width == HWHM (half-width half-max)
            pots = [h / (1 + ((x - p) / w) ** 2) for x in positions]
        elif self.shape == "GAUSSIAN":  # width = sigma (Gaussian width)
            pots = [h * np.exp(-((x - p) ** 2) / (2 * w**2)) for x in positions]
        return pots

    def show_dynamics(self, corrected: bool = False):
        """Plots the position, width, and height of the barrier over time."""
        tstart = min(self.times_ms)
        tstop = max(self.times_ms)
        times = np.linspace(
            tstart, tstop, num=int((tstop - tstart) / 0.1), endpoint=True
        )
        fig, ax1 = plt.subplots()
        # plot position and width vs time
        style = "steps-pre" if corrected else "default"
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("position or width (microns)")
        ax1.set_xlim([-1, self.times_ms[-1] + 1])
        ax1.set_ylim([-50, 50])
        (ln1,) = plt.plot(
            times, self.get_positions(times, corrected), color=color, drawstyle=style
        )
        plt.plot(
            self.times_ms,
            self.get_positions(self.times_ms, corrected),
            ".",
            color=color,
        )
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln2,) = plt.plot(
            times, self.get_widths(times, corrected), color=color, drawstyle=style
        )
        plt.plot(
            self.times_ms, self.get_widths(self.times_ms, corrected), ".", color=color
        )
        # plot height on the same time axis
        ax2 = ax1.twinx()
        ax2.set_ylabel("height (kHz)")
        ax2.set_ylim([0, 100])
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln3,) = plt.plot(
            times, self.get_heights(times, corrected), color=color, drawstyle=style
        )
        plt.plot(
            self.times_ms, self.get_heights(self.times_ms, corrected), ".", color=color
        )
        # shared setup
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.legend([ln1, ln2, ln3], ["position", "width", "height"], loc="upper left")
        plt.title("Barrier dynamics")
        fig.tight_layout()
        plt.show()

    def show_potential(self, times: list = [0], corrected: bool = False):
        """Plot the potential energy vs. position at the given times.
        Args:
            times (list): times (in ms) at which the potential is calculated.
        """
        x_limits = [-61, 61]
        y_limits = [-1, max(self.heights_khz) + 1]
        positions = np.arange(min(x_limits), max(x_limits) + 1, 1)

        fig, ax1 = plt.subplots()
        ax = plt.gca()
        lns = []
        labs = []
        for time in times:
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(
                positions, self.get_potential(time, positions, corrected), color=color
            )
            plt.plot(
                positions,
                self.get_potential(time, positions, corrected),
                ".",
                color=color,
            )
            lns.append(ln)
            labs.append("t=" + str(time))

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Barrier temporal snapshots")
        plt.xlim(x_limits)
        plt.ylim(y_limits)
        ax1.legend(lns, labs, loc=0)
        plt.show()
