from bert_schemas import job as job_schema

from oqtant.schemas.interpolation import interpolate_1d_list


class ConversionError(Exception):
    pass


class RfSequence(job_schema.RfEvaporation):
    """A class that represents a sequence of radiofrequency powers/frequencies in time"""

    @classmethod
    def new(
        cls,
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        return cls(
            times_ms=times,
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation):
        return cls(**rf_evaporation.model_dump())

    def get_frequencies(self, times: list) -> list:
        """Calculates the frequency of the RfSequence object at the specified times.

        Args:
            times (list): Times (in ms) at which the RF frequencies are calculated.
        Returns:
            list: Calculated frequencies (in MHz) at the specified times.
        """
        return interpolate_1d_list(
            self.times_ms,
            self.frequencies_mhz,
            times,
            self.interpolation,
        )

    def get_powers(self, times: list) -> list:
        """Calculates RF evaporation powers at the specified times.
        Args:
            times (list): Times (in ms) at which the RF powers are calculated.
        Returns:
            list: RF powers (in mW) at the specified times.
        """
        return interpolate_1d_list(
            self.times_ms, self.powers_mw, times, self.interpolation
        )


class RfEvap(RfSequence):
    """A class that represents the forced RF evaporation that cools atoms to quantum degeneracy."""

    @classmethod
    def new(
        cls,
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        return cls(
            times_ms=[t - max(times) for t in times],
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation):
        """
        Creates a new instance of the class using the given `rf_evaporation` object as input.

        Parameters:
            rf_evaporation (job_schema.RfEvaporation): The `RfEvaporation` object containing the data for the instance creation.

        Returns:
            cls: A new instance of the class with the specified properties.
        """
        rf_evap_times = [t for t in rf_evaporation.times_ms if t <= 0.0]
        if rf_evap_times == []:
            raise ConversionError()

        rf_evap_freqs = [
            f
            for t, f in zip(rf_evaporation.times_ms, rf_evaporation.frequencies_mhz)
            if t <= 0.0
        ]

        rf_evap_pows = [
            p
            for t, p in zip(rf_evaporation.times_ms, rf_evaporation.powers_mw)
            if t <= 0.0
        ]
        return cls.new(
            times=rf_evap_times,
            frequencies=rf_evap_freqs,
            powers=rf_evap_pows,
            interpolation=rf_evaporation.interpolation,
        )


# A RfShield is a CONSTANT evaporation occuring during the entire experimental phase
# any non-negative time in the rf_evaporation object of a program indicates a
# rf shield is desired for the entire duration of the experiment stage
class RfShield(job_schema.RfEvaporation):
    """A class that represents an RF shield (at fixed frequency and power)
    being applied during the 'experiment' phase/stage."""

    @classmethod
    def new(
        cls,
        lifetime: float,
        frequency: float,
        power: float,
        interpolation: job_schema.InterpolationType = "LINEAR",
    ):
        return cls(
            times_ms=[lifetime],
            powers_mw=[power],
            frequencies_mhz=[frequency],
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation):
        """
        Create an instance of the class from the given rf_evaporation input.

        Parameters:
            rf_evaporation (job_schema.RfEvaporation): The input object containing the attributes for the instance creation.

        Returns:
            cls: An instance of the class created from the input.
        """
        if rf_evaporation.times_ms[-1] <= 0:
            raise ConversionError()
        else:
            return cls.new(
                lifetime=rf_evaporation.times_ms[-1],
                frequency=rf_evaporation.frequencies_mhz[-1],
                power=rf_evaporation.powers_mw[-1],
                interpolation=rf_evaporation.interpolation,
            )

    @property
    def lifetime(self):
        return self.times_ms[0]

    @property
    def frequency(self):
        return self.frequencies_mhz[0]

    def frequencies(self, times: list):
        return [self.frequencies_mhz[0]] * len(times)

    @property
    def power(self):
        return self.powers_mw[0]

    def powers(self, times: list):
        return [self.powers_mw[0]] * len(times)
