import json
import warnings
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas import job as job_schema
from pydantic import BaseModel, confloat, conint

from oqtant.schemas.job import OqtantJob
from oqtant.schemas.optical import Barrier, Landscape, Snapshot
from oqtant.schemas.rf import ConversionError, RfEvap, RfSequence, RfShield

DEFAULT_RF_EVAP = RfEvap.new(
    times=[0, 50, 300, 800, 1100],
    powers=[600, 800, 600, 400, 400],
    frequencies=[21.12, 12.12, 5.12, 0.62, 0.02],
    interpolation="LINEAR",
)

DEFAULT_NAME = "quantum matter"
DEFAULT_LIFETIME = 10  # ms
DEFAULT_TEMPERATURE = 200  # nK
DEFAULT_TOF = 8  # ms
DEFAULT_IMAGE = job_schema.ImageType.TIME_OF_FLIGHT


class QuantumMatter(BaseModel):
    """A class that represents user inputs to create and control quantum matter."""

    name: str | None = DEFAULT_NAME
    temperature: confloat(ge=0, le=1000) | None = DEFAULT_TEMPERATURE
    lifetime: conint(ge=0, le=80) | None = DEFAULT_LIFETIME
    image: job_schema.ImageType | None = DEFAULT_IMAGE
    time_of_flight: float | None = DEFAULT_TOF
    rf_evap: RfEvap | None = DEFAULT_RF_EVAP
    rf_shield: RfShield | None = None
    barriers: list[Barrier] | None = None
    landscape: Landscape | None = None
    lasers: list[job_schema.Laser] | None = None
    note: str | None = None

    def model_post_init(self, *args):
        if self.temperature != DEFAULT_TEMPERATURE and self.rf_evap != DEFAULT_RF_EVAP:
            warnings.warn(
                "Both 'temperature' and 'rf_evap' inputs provided, the last rf_evap frequency will be altered."
            )

        # warn if object lifetime is not suitable for any optical potentials specified
        end_time = 0.0
        if self.barriers:
            for barrier in self.barriers:
                end_time = max(end_time, barrier.death)
        if self.landscape:
            for snapshot in self.landscape.snapshots:
                end_time = max(end_time, snapshot.time_ms)
        if end_time > self.lifetime:
            warnings.warn(
                "Specified 'lifetime' not sufficient for included barriers and/or landscapes."
            )

    @classmethod
    def from_input(
        cls,
        name: str,
        input: job_schema.InputValues,
    ):
        """
        Creates an instance of the class using the provided input values.

        Args:
            name (str): The name of the instance.
            input (job_schema.InputValues): The input values for the instance.

        Returns:
            cls: An instance of the class with the provided input values.
        """
        try:
            evap = RfEvap.from_input(input.rf_evaporation)
        except ConversionError:
            evap = None
        try:
            shield = RfShield.from_input(input.rf_evaporation)
        except ConversionError:
            shield = None

        barriers = None
        if input.optical_barriers:
            barriers = []
            for barrier in input.optical_barriers:
                barriers.append(Barrier.from_input(barrier))

        landscape = None
        if input.optical_landscape:
            landscape = Landscape.from_input(input.optical_landscape)

        return cls(
            name=name,
            lifetime=input.end_time_ms,
            time_of_flight=input.time_of_flight_ms,
            rf_evap=evap,
            rf_shield=shield,
            barriers=barriers,
            landscape=landscape,
            lasers=input.lasers,
        )

    @classmethod
    def from_oqtant_job(cls, job: OqtantJob, run: int = 1):
        """
        Convenience method for creating a QuantumMatter object from an existing OqtantJob.

        Args:
            job (OqtantJob): An instance of the OqtantJob class.
            run (int): The index of the run to use. Defaults to 1.

        Returns:
            QuantumMatter: An instance of the QuantumMatter class created using the OqtantJob object.
        """
        return QuantumMatter.from_input(name=job.name, input=job.inputs[run - 1].values)

    @property
    def input(self) -> job_schema.InputValues:
        """Extracts InputValues needed to construct a job from this object."""
        return job_schema.InputValues(
            end_time_ms=self.lifetime,
            time_of_flight_ms=self.time_of_flight,
            image_type=self.image,
            rf_evaporation=self.rf_evaporation,
            optical_barriers=self.barriers,
            optical_landscape=self.landscape,
            lasers=self.lasers,
        )

    @property
    def rf_evaporation(self) -> job_schema.RfEvaporation:
        """
        Extracts RfEvaporation object from this object.

        Returns:
            job_schema.RfEvaporation: The rf_evaporation property.
        """
        rf_evap_derived = deepcopy(self.rf_evap)
        rf_evap_derived.frequencies_mhz[-1] = (0.02 / 200) * self.temperature
        rf_evaporation = job_schema.RfEvaporation(
            times_ms=rf_evap_derived.times_ms,
            frequencies_mhz=rf_evap_derived.frequencies_mhz,
            powers_mw=rf_evap_derived.powers_mw,
            interpolation=rf_evap_derived.interpolation,
        )
        if self.rf_shield is not None:
            rf_evaporation.times_ms.append(self.lifetime)
            rf_evaporation.powers_mw.append(self.rf_shield.power)
            rf_evaporation.frequencies_mhz.append(self.rf_shield.frequency)

        return rf_evaporation

    def corrected_rf_power(self, frequency_mhz, power_mw):
        """
        Calculate the corrected RF power based on the given frequency and power.

        Args:
            frequency_mhz (float): The frequency in MHz.
            power_mw (float): The power in mW.

        Returns:
            float: The corrected RF power in mW.
        """
        # based on data taken from smallbert for power measured in dbm by a nearby pickup rf loop
        # as a function of the frequency (in MHz) and RF attenuator voltage (in volts)
        # the 'composer' turns payload powers of 0-1000 mW into voltages using a linear
        # relationship that maps 0-1000 mW to 0-5 V on the RF attenuator (5V = max power)
        voltage = power_mw * 5.0 / 1000.0  # payload power to attenuator voltage
        power_dbm = (
            -26.2 - 42 * np.exp(-0.142 * frequency_mhz) - 32.76 * np.exp(-1.2 * voltage)
        )
        return (1000.0 / 2.0e-3) * 10 ** (
            power_dbm / 10.0
        )  # dbm to mW with overall scaling

    def corrected_rf_powers(self, frequencies, powers):
        """Calculates corrected rf powers for the given equal-length lists of
        frequencies and powers.

        Args:
            frequencies (list): input frequencies (in MHz)
            powers (list): input powers (in mW)

        Returns:
            list: Corrected rf powers corresponding to the input lists as ordered pairs.
        """
        return [
            self.corrected_rf_power(freq, pow) for freq, pow in zip(frequencies, powers)
        ]

    def show_rf_dynamics(self, corrected: bool = False):
        """
        "Plots the dynamics of a QuantumMatter object's RF output.

        Parameters:
            corrected (bool, optional): If True, plots the corrected RF power. Defaults to False.

        Returns:
            None
        """
        tstart = min(self.rf_evap.times_ms)
        evap_times = np.linspace(tstart, 0, num=int(abs(tstart) / 10), endpoint=True)
        fig, ax1 = plt.subplots()
        lns = []
        labs = []

        # plot of rf frequency vs time
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("frequency (MHz)")
        ax1.set_ylim([0, 25])
        (ln1,) = plt.plot(
            evap_times, self.rf_evap.get_frequencies(evap_times), color=color
        )
        lns.append(ln1)
        labs.append("frequency")
        plt.plot(
            self.rf_evap.times_ms,
            self.rf_evap.get_frequencies(self.rf_evap.times_ms),
            ".",
            color=color,
        )
        if self.rf_shield is not None:
            plt.plot(
                [0, self.lifetime],
                [self.rf_shield.frequency] * 2,
                marker=".",
                color=color,
            )

        # plot of rf power vs time, on the same time axis as ax1
        ax2 = ax1.twinx()
        ax2.set_ylim([0, 1000])
        ax2.set_ylabel("power (mW)")
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln2,) = plt.plot(evap_times, self.rf_evap.get_powers(evap_times), color=color)
        lns.append(ln2)
        labs.append("power")
        plt.plot(
            self.rf_evap.times_ms,
            self.rf_evap.get_powers(self.rf_evap.times_ms),
            ".",
            color=color,
        )
        if self.rf_shield is not None:
            plt.plot(
                [0, self.lifetime], [self.rf_shield.power] * 2, marker=".", color=color
            )
        if corrected:
            (ln3,) = plt.plot(
                evap_times,
                self.corrected_rf_powers(
                    self.rf_evap.get_frequencies(evap_times),
                    self.rf_evap.get_powers(evap_times),
                ),
                "--",
                color=color,
            )
            if self.rf_shield is not None:
                plt.plot(
                    [0, self.rf_shield.lifetime],
                    self.corrected_rf_powers(
                        [self.rf_shield.frequency] * 2,
                        [self.rf_shield.power] * 2,
                    ),
                    "--",
                    color=color,
                )
            lns.append(ln3)
            labs.append("corrected power")
        # shared setup
        ax1.legend(lns, labs, loc="upper center")
        color = next(ax1._get_lines.prop_cycler)["color"]
        plt.axvline(x=0, linestyle="dashed", color=color)
        plt.title("RF dynamic behavior")
        fig.tight_layout()  # avoid clipping right y-axis label
        plt.show()

    def get_magnetic_potential(self, positions: list) -> list:
        """
        Calculate the magnetic potentials for a given set of positions.

        # U = mf * g * ub * |B| with B = B0 + 0.5 * m * w^2 * x^2
        # for this purpose, we will set B0 = 0
        # (magnetic potential referenced to trap bottom as rf frequencies are)
        # our measured trap frequency is ~ 50 Hz

        Args:
            positions (list): A list of positions at which to calculate the potentials.

        Returns:
            list: A list of magnetic potentials in kHz corresponding to the given positions.
        """
        w = 2 * np.pi * 50  # weak axis trap frequency
        m = 87 * 1.66054e-27
        h = 6.626e-34
        potentials = 0.5 * m * w**2 * np.square(1e-6 * np.asarray(positions))  # in J
        potentials_khz = potentials / h / 1000.0  # in kHz
        return list(potentials_khz)

    def get_barrier_potential(
        self, time: float, positions: list, corrected: bool = False
    ) -> list:
        """Extracts the potential energy due to all a QuantumMatter object's barriers.

        Args:
            time (float): Experiment time at which to evaluate barrier(s) parameters.
            positions (list): List of positions where potential energies are evaluated.

        Returns:
            list: Potential energies (in kHz) at specified time and positions.
        """
        potentials = np.zeros_like(positions)
        if self.barriers is not None:
            for barr in self.barriers:
                potentials += np.asarray(barr.get_potential(time, positions, corrected))
        np.clip(potentials, 0, 100)
        return list(potentials)

    def get_landscape_potential(
        self, time: float, positions: list, corrected: bool = False
    ) -> list:
        """
        Calculate the potential landscape at a given time for a list of positions.

        Args:
            time (float): The time for which the potential landscape is calculated.
            positions (list): A list of positions.
            corrected (bool, optional): Whether to apply any corrections to the potential.
                Defaults to False.

        Returns:
            list: A list of potentials corresponding to the positions.
        """
        potentials = np.zeros_like(positions)
        if self.landscape is not None:
            potentials = self.landscape.get_potential(time, positions)
        return potentials

    def get_potential(self, time: float, positions: list) -> list:
        """
        Calculate the potential at each position for a given time.

        Args:
            time (float): The time at which to calculate the potential.
            positions (list): The list of positions at which to calculate the potential.

        Returns:
            list: The list of potentials at each position.
        """
        potentials = np.asarray(self.get_barrier_potential(time, positions))
        potentials += np.asarray(self.get_landscape_potential(time, positions))
        np.clip(potentials, 0, 100)  # total optical potential clipped at 100 kHz
        potentials += np.asarray(self.get_magnetic_potential(positions))
        return list(potentials)

    def show_potential(self, times: list = [0]):
        """
        Plots the (optical) potential energy surface at the specified times.

        Parameters:
            times (list): A list of times for which to display the potential energy. Default is [0].

        Returns:
            None
        """
        positions = np.arange(-60, 60, 1, dtype=float)
        fig, ax = plt.subplots()
        lns = []
        labs = []
        for time in times:
            potentials = self.get_potential(time, positions)
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(positions, potentials, color=color)
            plt.plot(positions, potentials, color=color)
            lns.append(ln)
            labs.append("t=" + str(time))
        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.xlim([-61, 61])
        plt.ylim([-1, 101])
        ax.legend(lns, labs, loc=0)
        plt.show()

    def show_barrier_dynamics(self, corrected: bool = False):
        """
        Plots the time dynamics of all of a QuantumMatter object's Barrier objects.

        Args:
            corrected (bool, optional): Determines whether the corrected barrier dynamics
                should be shown. Defaults to False.

        Returns:
            None
        """
        fig, (ax1, ax2, ax3) = plt.subplots(
            nrows=3, ncols=1, sharex=True, figsize=(6, 6)
        )
        fig.suptitle("Barrier dynamics")
        ax1.set_xlim([-1, self.input.end_time_ms])
        ax1.set_ylabel("position (microns)")
        ax2.set_ylabel("height (kHz)")
        ax3.set_ylabel("width (microns)")
        ax3.set_xlabel("time (ms)")
        lns = []
        labs = []

        style = "steps-pre" if corrected else "default"
        for indx, barrier in enumerate(self.barriers):
            color = next(ax1._get_lines.prop_cycler)["color"]
            tstart = min(barrier.times_ms)
            tstop = max(barrier.times_ms)
            times = np.linspace(
                tstart, tstop, num=int((tstop - tstart) / 0.1), endpoint=True
            )
            (ln,) = ax1.plot(
                times, barrier.get_positions(times), color=color, drawstyle=style
            )
            ax1.plot(
                barrier.times_ms,
                barrier.get_positions(barrier.times_ms),
                ".",
                color=color,
            )
            ax2.plot(times, barrier.get_heights(times), color=color, drawstyle=style)
            ax2.plot(
                barrier.times_ms,
                barrier.get_heights(barrier.times_ms),
                ".",
                color=color,
            )
            ax3.plot(times, barrier.get_widths(times), color=color, drawstyle=style)
            ax3.plot(
                barrier.times_ms, barrier.get_widths(barrier.times_ms), ".", color=color
            )
            lns.append(ln)
            labs.append("barrier " + str(indx + 1))
        fig.legend(lns, labs)
        plt.show()

    class Config:
        validate_assignment = True


class QuantumMatterFactory:
    """
    An abstract factory for creating instances of the QuantumMatter schema classes
    """

    @staticmethod
    def create_quantum_matter(
        name: str | None = None,
        temperature: float | None = None,
        lifetime: float | None = None,
        image: job_schema.ImageType | None = None,
        time_of_flight: float | None = None,
        rf_evap: RfEvap | None = None,
        rf_shield: RfShield | None = None,
        barriers: list[Barrier] | None = None,
        landscape: Landscape | None = None,
        lasers: list[job_schema.Laser] | None = None,
        note: str | None = None,
    ):
        """
        Create a new QuantumMatter instance

        Args:
            name (str | None): The quantum matter name.
            temperature (float | None): The quantum matter temperature.
            lifetime (float | None): The quantum matter lifetime.
            image (job_schema.ImageType | None): The quantum matter image.
            time_of_flight (float | None): The quantum matter time of flight.
            rf_evap (RfEvap | None): The quantum matter RF evaporation.
            rf_shield (RfShield | None): The quantum matter RF shield.
            barriers (list[Barrier] | None): The quantum matter barriers.
            landscape (Landscape | None): The quantum matter landscape.
            lasers (list[job_schema.Laser] | None): The quantum matter lasers.
            note (str | None): A note about the quantum matter.

        Returns:
            QuantumMatter: A new QuantumMatter instance.
        """
        args = {}
        for k, v in locals().items():
            if v is not None:
                args[k] = v

        return QuantumMatter(**args)

    @staticmethod
    def create_quantum_matter_from_input(name: str, input: job_schema.InputValues):
        """
        Create a quantum matter object from job schema InputValues.

        Args:
            name (str): The name of the quantum matter.
            input (job_schema.InputValues): The job schema InputValues.

        Returns:
            QuantumMatter: The quantum matter object.
        """
        return QuantumMatter.from_input(name, input)

    @staticmethod
    def create_snapshot(
        time: float = 0,
        positions: list = [-10, 10],
        potentials: list = [0, 0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        """
        Creates a snapshot object using the simplfied parameters.

        Args:
            time (float): The time in milliseconds.
            positions (list): A list of positions in micrometers.
            potentials (list): A list of potentials in kilohertz.
            interpolation (job_schema.InterpolationType): The type of interpolation for spatial data.

        Returns:
            Snapshot: The created snapshot object.
        """
        return Snapshot(
            time_ms=time,
            positions_um=positions,
            potentials_khz=potentials,
            spatial_interpolation=interpolation,
        )

    @staticmethod
    def create_snapshot_from_input(input: job_schema.Landscape):
        """
        Creates a snapshot from a job schema Landscape object.

        Args:
            input (job_schema.Landscape): The job schema landscape object.

        Returns:
            Snapshot: The created snapshot object.
        """
        return Snapshot(**input.model_dump())

    @staticmethod
    def create_landscape(
        snapshots: list = [Snapshot.new(time=0), Snapshot.new(time=2)]
    ):
        """
        Create a landscape from a list of snapshots.

        Args:
            snapshots (list, optional): A list of snapshots. Defaults to [Snapshot.new(time=0), Snapshot.new(time=2)].

        Returns:
            Landscape: The created landscape object.
        """
        optical_landscapes = []
        for snapshot in snapshots:
            optical_landscapes.append(  # kludge!
                job_schema.Landscape(
                    time_ms=snapshot.time_ms,
                    positions_um=snapshot.positions_um,
                    potentials_khz=snapshot.potentials_khz,
                    spatial_interpolation=snapshot.spatial_interpolation,
                )
            )
        return Landscape(landscapes=optical_landscapes)

    @staticmethod
    def create_landscape_from_input(input: job_schema.OpticalLandscape):
        """
        Create a landscape object from a job schema OpticalLandscape object.

        Args:
            input (job_schema.OpticalLandscape): a job schema OpticalLandscape.

        Returns:
            Landscape: A new landscape object created from the OpticalLandscape.
        """
        return Landscape(**input.model_dump())

    @staticmethod
    def create_barrier(
        position: float = 0,
        height: float = 0,
        width: float = 1,
        birth: float = 0,
        lifetime: float = 0,
        shape: job_schema.ShapeType = "GAUSSIAN",
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        """
        Create a barrier object using the simplified parameters.

        Args:
            position (float, optional): The barrier position. Defaults to 0.
            height (float, optional): The barrier height. Defaults to 0.
            width (float, optional): The barrier width. Defaults to 1.
            birth (float, optional): The barrier birth time. Defaults to 0.
            lifetime (float, optional): The barrier lifetime. Defaults to 0.
            shape (job_schema.ShapeType, optional): The barrier shape. Defaults to "GAUSSIAN".
            interpolation (job_schema.InterpolationType, optional): The barrier interpolation type. Defaults to "LINEAR".

        Returns:
            Barrier: The created barrier object.
        """
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

        return Barrier(**data)

    @staticmethod
    def create_barrier_from_input(input: job_schema.Barrier):
        """
        Creates an Oqtant Barrier from a job schema Barrier.

        Args:
            input (job_schema.Barrier): A job schema Barrier.

        Returns:
            Barrier: An Oqtant Barrier object.
        """
        return Barrier(**input.model_dump())

    @staticmethod
    def create_rf_sequence(
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: str = "LINEAR",
    ):
        """
        Creates an RfSequence object using simplified arguments.

        Parameters:
            times (list): A list of time values in milliseconds.
            powers (list): A list of power values in milliwatts.
            frequencies (list): A list of frequency values in megahertz.
            interpolation (str): The type of interpolation to be used.

        Returns:
            RfSequence: An RfSequence object.
        """
        return RfSequence(
            times_ms=times,
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @staticmethod
    def create_rf_sequence_from_input(input: job_schema.RfEvaporation):
        """
        Create an Oqtant RFSequence instance from a job schema RfEvaporation object.

        Args:
            input (job_schema.RfEvaporation): A job schema RfEvaporation object.

        Returns:
            RfSequence: an Oqtant RFSequence object.

        """
        return RfSequence(**input.model_dump())

    @staticmethod
    def create_rf_evap(
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: str = "LINEAR",
    ) -> RfEvap:
        """
        Create an RFEvaporation object using simplified arguments.

        Args:
            times (list, optional): List of time values for the RF evaporation. Defaults to [0].
            powers (list, optional): List of power values for the RF evaporation. Defaults to [0].
            frequencies (list, optional): List of frequency values for the RF evaporation. Defaults to [0].
            interpolation (str, optional): Interpolation method for the RF evaporation. Defaults to "LINEAR".

        Returns:
            RfEvap: An RfEvap object.
        """
        return RfEvap.new(
            times=[t - max(times) for t in times],
            powers=powers,
            frequencies=frequencies,
            interpolation=interpolation,
        )

    @staticmethod
    def create_rf_evap_from_input(input: job_schema.RfEvaporation) -> RfEvap:
        """
        Create an RfEvap object from a job schema RfEvaporation object.

        Args:
            input (job_schema.RfEvaporation): a job schema RfEvaporation object

        Returns:
            RfEvap: An RfEvap object.

        """
        return RfEvap.from_input(input)

    @staticmethod
    def create_rf_shield(power: float = 0, frequency: float = 0, lifetime: float = 1.0):
        """
        Create an RFShield object.

        Args:
            power (float): The RFshield power (default is 0).
            frequency (float): The RFshield frequency (default is 0).
            lifetime (float): The RFshield lifetime (default is 1.0).

        Returns:
            RfShield: The new RFShield object.
        """
        return RfShield.new(
            lifetime,
            frequency,
            power,
            interpolation="OFF",
        )

    @staticmethod
    def create_rf_shield_from_input(input: job_schema.RfEvaporation):
        """
        Create an RF shield from a job schema RfEvaporation object.

        Args:
            input (job_schema.RfEvaporation): a job schema RfEvaporation object.

        Returns:
            RfShield: The created RF shield.
        """
        return RfShield.from_input(input)
