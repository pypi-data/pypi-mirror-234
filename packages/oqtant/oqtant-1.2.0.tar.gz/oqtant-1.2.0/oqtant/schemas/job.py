# Copyright 2023 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from enum import Enum
from math import floor, log10, pi
from typing import Any, Optional, Union
from uuid import UUID

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from bert_schemas import job as job_schema
from dateutil import parser as date_parser
from dateutil import tz
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from pydantic import Field

from oqtant.util.exceptions import (
    JobPlotFitError,
    JobPlotFitMismatchError,
    JobReadError,
)

SIG_ABS = 0.297


class OutputImageType(str, Enum):
    TIME_OF_FLIGHT = "TIME_OF_FLIGHT"
    IN_TRAP = "IN_TRAP"
    MOT = "MOT"
    TIME_OF_FLIGHT_FIT = "TIME_OF_FLIGHT_FIT"


class AxisType(str, Enum):
    x = "x"
    y = "y"


def round_sig(x: float, sig: int = 2):
    """
    Round a number to a specified number of significant digits.

    Parameters:
        x (float): The number to be rounded.
        sig (int): The number of significant digits (default is 2).

    Returns:
        float: The rounded number.
    """
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def TF_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    TFpOD: float,
    xc: float,
    yc: float,
    rx: float,
    ry: float,
    os: float,
) -> np.ndarray:
    """
    Defines 2D Thomas-Fermi distribution characteristic of zero-temperature Bose-gas
    Requires function(s): get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing mesh grid of image coordinates
    :param TFpOD:
    :type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
    :param rx:
    :type rx: float - Thomas-Fermi radius along the x direction
    :param ry:
    :type ry: float - Thomas-Fermi radius along the y direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y direction
    :param os:
    :type os: float - Constant offset
    """

    # unpack 1D list into 2D x and y coords
    (x, y) = xy_mesh

    # Simplify Thomas-Fermi expression
    A = 1 - ((y - yc) / rx) ** 2 - ((x - xc) / ry) ** 2

    # make 2D Thomas-Fermi distribution
    OD = np.real(TFpOD * np.maximum(np.sign(A) * (np.abs(A)) ** (3 / 2), 0)) + os

    # flatten the 2D Gaussian down to 1D
    return OD.ravel()


def Gaussian_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    GpOD: float,
    xc: float,
    yc: float,
    sigx: float,
    sigy: float,
    os: float,
):
    """
    Defines 2D gaussian distribution characteristic of a thermal ensemble of atoms
    Requires function(s): get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
    :param GpOD:
    :type GpOD: float - Gaussian peak Optical Density (OD)
    :param sigx:
    :type sigx: float - Gaussian spread along the x direction
    :param sigy:
    :type sigy: float - Gaussian spread along the y direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y direction
    :param os:
    :type os: float - Constant offset
    """

    (x, y) = xy_mesh

    OD = (
        GpOD * np.exp(-0.5 * ((y - yc) / sigy) ** 2 - 0.5 * ((x - xc) / sigx) ** 2) + os
    )
    return OD.ravel()


def bimodal_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    GpOD: float,
    sigx: float,
    sigy: float,
    TFpOD: float,
    rx: float,
    ry: float,
    xc: float,
    yc: float,
    os: float,
):
    """
    Defines 2D bimodal distribution characteristic of finite-temperature Bose-gas
    Requires functions: Gaussian_dist_2D, TF_dist_2D, get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
    :param GpOD:
    :type GpOD: float - Gaussian peak Optical Density (OD)
    :param sigx:
    :type sigx: float - Gaussian spread along the x direction
    :param sigy:
    :type sigy: float - Gaussian spread along the y direction (along gravity)
    :param TFpOD:
    :type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
    :param rx:
    :type rx: float - Thomas-Fermi radius along the x direction
    :param ry:
    :type ry: float - Thomas-Fermi radius along the y direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y direction
    :param os:
    :type os: float - Constant offset
    """

    return Gaussian_dist_2D(xy_mesh, GpOD, xc, yc, sigx, sigy, os) + TF_dist_2D(
        xy_mesh, TFpOD, xc, yc, rx, ry, os
    )


class OqtantJob(job_schema.JobCreate):
    active_run: int = 1
    external_id: UUID | None = None
    time_submit: str | datetime | None = None

    @property
    def truncated_name(self):
        if len(self.name) > 40:
            return f"{self.name[:37]}..."
        return self.name

    @property
    def id(self):
        return self.external_id

    @property
    def formatted_time_submit(self):
        return self.format_datetime_string(self.date_time)

    @staticmethod
    def format_datetime_string(datetime_string: str) -> str:
        try:
            parsed_datetime = date_parser.parse(datetime_string)
            parsed_datetime = parsed_datetime.replace(tzinfo=tz.tzutc())
            parsed_datetime = parsed_datetime.astimezone(tz.tzlocal())
            formatted_datetime_string = parsed_datetime.strftime("%m/%d/%Y, %H:%M")
        except Exception:
            formatted_datetime_string = datetime_string
        return formatted_datetime_string

    def __print_keys(self, subject: Any, indent: int = 0, drill_lists=False):
        if isinstance(subject, dict):
            for key, value in subject.items():
                print(f"{' ' * indent}- {key}")
                if isinstance(value, dict):
                    self.__print_keys(value, indent=indent + 2, drill_lists=drill_lists)
                if isinstance(value, list) and drill_lists:
                    for list_value in value:
                        if isinstance(list_value, dict):
                            self.__print_keys(
                                list_value, indent=indent + 2, drill_lists=drill_lists
                            )

    @property
    def input_fields(self):
        self.__print_keys(self.input.dict(), drill_lists=True)

    @property
    def output_fields(self):
        if self.status == job_schema.JobStatus.COMPLETE:
            self.__print_keys(self.output.dict())
        else:
            raise JobReadError("Job results not available.")

    @property
    def output(self):
        if self.status != job_schema.JobStatus.COMPLETE:
            raise JobReadError("Job results not available.")
        return self.inputs[self.active_run - 1].output.values

    @property
    def input(self):
        return self.inputs[self.active_run - 1].values

    @property
    def lifetime(self):
        return self.input.end_time_ms

    @property
    def atom_statistics(self):
        if self.input.image_type == job_schema.ImageType.TIME_OF_FLIGHT:
            print(f"Temperature (nK): {self.temperature}")
            print(f"Total atoms : {self.output.tof_atom_number}")
            print(f"Condensed atoms : {self.output.condensed_atom_number}")
            print(f"Thermal atoms : {self.output.thermal_atom_number}")
        else:
            raise JobReadError(
                "Atom statistics only available for TIME_OF_FLIGHT imaging in a BEC job."
            )

    @property
    def TOF(self):
        """
        Returns shaped TOF image if it exists
        :returns: reshaped pixels numpy array (100,100)

        """
        if self.status != job_schema.JobStatus.COMPLETE:
            raise JobReadError("Job results not available.")
        try:
            reshaped_pixels = np.array(self.output.tof_image.pixels).reshape(
                self.output.tof_image.rows, self.output.tof_image.columns
            )
        except Exception as exc:
            raise JobReadError("no TOF results") from exc
        return reshaped_pixels

    @property
    def IT(self):
        """
        Returns shaped IT image if it exists
        :returns: reshaped pixels numpy array (100,100)

        """
        if self.status != job_schema.JobStatus.COMPLETE:
            raise JobReadError("Job results not available.")

        try:
            reshaped_pixels = np.array(
                self.inputs[0].output.values.it_plot.pixels
            ).reshape(self.output.it_plot.rows, self.output.it_plot.columns)
        except Exception as exc:
            raise JobReadError("no IT results") from exc
        return reshaped_pixels

    @property
    def temperature(self):
        return self.output.temperature_uk

    @property
    def mot_population(self):
        return self.output.thermal_atom_number

    @property
    def thermal_population(self):
        return self.output.thermal_atom_number

    @property
    def condensed_population(self):
        return self.output.condensed_atom_number

    @property
    def total_population(self):
        return self.thermal_population + self.condensed_population

    @property
    def condensed_fraction(self):
        return np.round(self.condensed_population / self.total_population, 3)

    @property
    def get_bimodal_fit_parameters(self):
        if self.input.image_type == "IN_TRAP":
            raise JobReadError("Bimodal fit does not exist for IT image option.")
        else:
            return self.output.tof_fit

    def get_image_data(self, image: OutputImageType | None = None) -> np.ndarray:
        """
        Retrieve the image data for the specified image type.

        Parameters:
            image (OutputImageType | None): The type of image to retrieve. Defaults to None.

        Returns:
            np.ndarray: The image data as a NumPy array.
        """
        job_image_type = self.input.image_type
        in_trap = job_schema.ImageType.IN_TRAP
        tof = job_schema.ImageType.TIME_OF_FLIGHT

        if image is None:
            # no type specified, assume user wants output image of the correct
            # type based on the image_type used in the job
            image = in_trap if job_image_type == in_trap else tof
        if image == in_trap:
            data = self.output.it_plot.pixels
            shape = (self.output.it_plot.rows, self.output.it_plot.columns)
        elif image == tof:
            data = self.output.tof_image.pixels
            shape = (self.output.tof_image.rows, self.output.tof_image.columns)
        elif image == "MOT":
            data = self.output.mot_fluorescence_image.pixels
            shape = (
                self.output.mot_fluorescence_image.rows,
                self.output.mot_fluorescence_image.columns,
            )
        elif image == "TIME_OF_FLIGHT_FIT":
            if job_image_type == in_trap:
                raise JobReadError("no fit image available for IN_TRAP")
            data = self.output.tof_fit_image.pixels
            shape = (self.output.tof_fit_image.rows, self.output.tof_fit_image.columns)
        return np.asarray(data).reshape(shape)

    def get_image_pixcal(self, image: OutputImageType | None = None) -> float:
        """
        Get the pixcal value for the provided image type, if none provided defaults to job image type
        Args:
            image (OutputImageType): the image type to read pixcal of
        Returns:
            (float): the pixcal value
        """

        def __parse_pixcal(image_name: str) -> float:
            try:
                return getattr(self.output, image_name).pixcal
            except Exception:
                raise JobReadError(
                    f"{self.job_type} job does not contain a {image} image"
                )

        if image == OutputImageType.TIME_OF_FLIGHT:
            pixcal = __parse_pixcal("tof_image")
        elif image == OutputImageType.IN_TRAP:
            pixcal = __parse_pixcal("it_plot")
        elif image == OutputImageType.MOT:
            pixcal = __parse_pixcal("mot_fluorescence_image")
        elif image == OutputImageType.TIME_OF_FLIGHT_FIT:
            pixcal = __parse_pixcal("tof_fit_image")
        else:
            image_name = (
                "tof_image"
                if self.input.image_type == job_schema.ImageType.TIME_OF_FLIGHT
                else "it_plot"
            )
            pixcal = __parse_pixcal(image_name)
        return pixcal

    def get_slice(self, axis: AxisType = "x") -> list:
        """
        Returns a list of data points representing a slice along the specified axis.

        Parameters:
            - axis (AxisType): The axis along which to take the slice. Defaults to "x".

        Returns:
            - list: A list of data points representing the slice along the specified axis.
        """
        if axis == "x":
            data = self.output.tof_x_slice.points
            cut_data = [point["y"] for point in data]
        else:
            data = self.output.tof_y_slice.points
            cut_data = [point["y"] for point in data]
        return cut_data

    def add_notes_to_input(self, notes: str):
        self.inputs[self.active_run - 1].notes = notes

    @staticmethod
    def get_image_space(datafile=np.zeros((100, 100)), centered="y"):
        """
        Returns meshgrid of image coordinates
        :param datafile:
        :type datafile: (N,M) Matrix of Optical Density (OD) Data
        """

        lx, ly = np.shape(datafile)
        x, y = np.arange(lx), np.arange(ly)

        if centered == "y":
            x = x - round(lx / 2)
            y = y - round(ly / 2)

        xy_mesh = np.meshgrid(x, y)

        return xy_mesh, lx, ly

    def fit_bimodal_data2D(self, xi=None, lb=None, ub=None):
        """
        Performs fit via trust region reflective algorithm.
        Requires functions: bimodal_dist_2D, Gaussian_dist_2D, TF_dist_2D, get_image_space
        For better fit performance, tune initial guess 'xi' and lower/upper bounds, 'lb' and 'ub'
        :param xy_mesh:
        :type xy_mesh: (2,N,M) Matrix containing meshgrid of image data coordinates
        :param data2D:
        :type data2D: (N,M) Matrix containing image data
        :param xi:
        :type xi: (1,9) List of fit parameter initial guesses
        :param lb:
        :type lb:  (1,9) List of fit parameter lower bounds
        :param ub:
        :type ub: (1,9) List of fit parameter upper bounds
        """
        xi = xi if xi else [0.25, 8, 8, 1, 4, 6, 0, 0, 0.02]
        lb = lb if lb else [0, 7, 7, 0, 2, 2, -20, -20, 0]
        ub = ub if ub else [2, 20, 20, 2, 20, 20, 20, 20, 1]

        xy_mesh, _, _ = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh
        x = X[0]
        y = Y[:, 0]

        fit_params, cov_mat = opt.curve_fit(
            bimodal_dist_2D, xy_mesh, np.ravel(self.TOF), p0=xi, bounds=(lb, ub)
        )
        fit_residual = self.TOF - bimodal_dist_2D(xy_mesh, *fit_params).reshape(
            np.outer(x, y).shape
        )
        fit_Rsquared = 1 - np.var(fit_residual) / np.var(self.TOF)

        return fit_params, cov_mat, fit_residual, fit_Rsquared

    def plot_fit_results(
        self,
        fit_params,
        model="bimodal",
        file_name=None,
        plot_title=None,
        pix_cal: float = 1.0,
    ):
        """
        Plot the results of a fit operation

        :param fit_params:
        :type fit_params: list of parameters from a fit operation
        :param model:
        :type model: string "bimodal", "TF", or "gaussian". default "bimodal"
        :param output:
        :type output: valid filename
        :param plot_title:
        :type plot_title: string title for the plot.
            default "job: "+str(self.name)+"\nTOF fit: "+str(model)

        """

        xy_mesh, lx, ly = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh

        if model == "bimodal":
            try:
                m = bimodal_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc

        elif model == "gaussian":
            try:
                m = Gaussian_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise TypeError(
                    "PLOT FIT RESULTS: mismatched parameters and model type"
                ) from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        elif model == "TF":
            try:
                m = TF_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        else:
            print(
                f"PLOT FIT RESULTS: Invalid model specified: {model}.",
                " Select 'bimodal', 'gaussian', or 'TF'",
            )
            return

        m = m.reshape(lx, ly)
        plt.figure()
        plt.imshow(
            m,
            origin="upper",
            cmap="nipy_spectral",
            extent=[
                np.min(X) * pix_cal,
                np.max(X) * pix_cal,
                np.min(Y) * pix_cal,
                np.max(Y) * pix_cal,
            ],
        )

        if plot_title is None:
            plot_title = f"job: {self.name}\nTOF fit: {model}"

        plt.title(plot_title)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    @staticmethod
    def _save_plot_file(plot, file_name):
        file = f"{file_name}.png"
        try:
            plot.savefig(file)
            print(f"plot saved to file: {file}")
        except (FileNotFoundError, Exception):
            print(f"failed to save plot at {file}")

    def plot_tof(self, file_name=None, figsize=(12, 12), gridon=False):
        """
        Generate a 2D plot of atom OD (save or show)

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

        """

        xy_mesh, _, _ = self.get_image_space()  # TOF_data
        (X, Y) = xy_mesh

        fig2D = plt.figure(figsize=figsize)
        ax = fig2D.gca()
        plt2D = plt.imshow(
            self.TOF,
            origin="upper",
            cmap="nipy_spectral",
            extent=[
                np.min(X) * self.get_image_pixcal("TOF"),
                np.max(X) * self.get_image_pixcal("TOF"),
                np.min(Y) * self.get_image_pixcal("TOF"),
                np.max(Y) * self.get_image_pixcal("TOF"),
            ],
        )
        plt.grid(b=gridon)
        plt.colorbar(plt2D, shrink=0.8)

        ax.set_xlabel("x position (microns)", labelpad=15, fontsize=16)
        ax.set_ylabel("y position (microns)", labelpad=15, fontsize=16)
        plt.title("time of flight optical depth", fontsize=16)

        print("Peak OD: ", round(np.max(self.TOF), 3))

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def plot_slice(
        self, file_name: str = None, axis: AxisType = "x", gridon: bool = False
    ):
        """
        Generate a 1D slice plot of atom OD in x or y

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param axis:
        :axis: AxisType 'x' or 'y'
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

        """
        xy_mesh, lx, ly = self.get_image_space(self.TOF)
        (X, Y) = xy_mesh

        params, *_ = self.fit_bimodal_data2D()
        fitOD = bimodal_dist_2D(xy_mesh, *params)

        Gfit_params = [params[0], params[6], params[7], params[1], params[2], params[8]]
        fitODG = Gaussian_dist_2D(xy_mesh, *Gfit_params)

        # Reshape Fit Distributions to 2D form
        fitOD2D = fitOD.reshape(lx, ly)
        fitODG2D = fitODG.reshape(lx, ly)

        # Define Central slices
        xslice = fitOD2D[int(lx / 2), :]
        yslice = fitOD2D[:, int(ly / 2)]
        xsliceG = fitODG2D[int(lx / 2), :]
        ysliceG = fitODG2D[:, int(ly / 2)]

        if axis == "x":
            xsliceD = self.TOF[int(len(X[1]) / 2), :]
            xslice = fitOD2D[int(len(X[1]) / 2), :]
            xsliceG = fitODG2D[int(len(X[1]) / 2), :]
            plt.title("x slice", fontsize=16)
            plt.plot(X[1] * self.get_image_pixcal("TOF"), xsliceD, "ok")
            plt.plot(X[1] * self.get_image_pixcal("TOF"), xslice, "b")
            plt.plot(X[1] * self.get_image_pixcal("TOF"), xsliceG, "r")
        elif axis == "y":
            ysliceD = self.TOF[:, int(len(Y[1]) / 2)]
            yslice = fitOD2D[:, int(len(Y[1]) / 2)]
            ysliceG = fitODG2D[:, int(len(Y[1]) / 2)]
            plt.title("y slice", fontsize=16)
            plt.plot(Y[:, 1] * self.get_image_pixcal("TOF"), ysliceD, "ok")
            plt.plot(Y[:, 1] * self.get_image_pixcal("TOF"), yslice, "b")
            plt.plot(Y[:, 1] * self.get_image_pixcal("TOF"), ysliceG, "r")
        else:
            raise ValueError("input either x or y")

        plt.grid(b=gridon)
        plt.xlabel("x position (microns)", labelpad=15, fontsize=16)
        plt.ylabel("optical depth", labelpad=15, fontsize=16)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def plot_it(self, file_name=None, figsize=(12, 12)):
        IT_OD = self.get_image_data("IN_TRAP")

        plt.figure(figsize=figsize)
        plt.title("in-trap optical depth")
        IT_plot = plt.imshow(
            IT_OD, origin="upper", cmap="nipy_spectral", extent=[-256, 256, -74, 74]
        )
        plt.xlabel("x position (microns)")
        plt.ylabel("y position (microns)")
        plt.grid(visible=True)
        plt.colorbar(IT_plot, shrink=0.25)
        plt.show()

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    # This function plots the optical depth as a 3D surface with projected density contours
    def plot_tof_3d(self, file_name=None, view_angle=-45, figsize=(10, 10)):
        """
        Generate a 3D slice plot of atom OD

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param view_angle:
        :type view_angle: int (-180, 180). default -45
        :param figsize:
        :type figsize: tuple. default is (10,10)

        """

        fig3d = plt.figure(figsize=figsize)
        ax = fig3d.gca(projection="3d")

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Set axis labels
        ax.set_xlabel("x position (microns)", labelpad=10)
        ax.set_ylabel("y position (microns)", labelpad=10)
        ax.set_zlabel("optical depth", labelpad=10)

        # rotate the axes and update
        ax.view_init(30, view_angle)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()
