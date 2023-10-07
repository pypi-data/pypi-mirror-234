# Module oqtant.schemas.job

## Functions

`Gaussian_dist_2D(xy_mesh, GpOD, xc, yc, sigx, sigy, os)`
: Defines 2D gaussian distribution characteristic of a thermal ensemble of atoms
Requires function(s): get_image_space
:param xy_mesh:
:type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
:param GpOD:
:type GpOD: float - Gaussian peak Optical Density (OD)
:param sigx:
:type sigx: float - Gaussian spread along the x-direction
:param sigy:
:type sigy: float - Gaussian spread along the y-direction (along gravity)
:param xc:
:type xc: float - Cloud center along the x-direction (along gravity)
:param yc:
:type yc: float - Cloud center along the y-direction
:param os:
:type os: float - Constant offset

`TF_dist_2D(xy_mesh, TFpOD, xc, yc, rx, ry, os)`
: Defines 2D Thomas-Fermi distribution characteristic of zero-temperature Bose-gas
Requires function(s): get_image_space
:param xy_mesh:
:type xy_mesh: (2,N,M) Matrix of floats containing mesh grid of image coordinates
:param TFpOD:
:type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
:param rx:
:type rx: float - Thomas-Fermi radius along the x-direction
:param ry:
:type ry: float - Thomas-Fermi radius along the y-direction (along gravity)
:param xc:
:type xc: float - Cloud center along the x-direction (along gravity)
:param yc:
:type yc: float - Cloud center along the y-direction
:param os:
:type os: float - Constant offset

`bimodal_dist_2D(xy_mesh, GpOD, sigx, sigy, TFpOD, rx, ry, xc, yc, os)`
: Defines 2D bimodal distribution characteristic of finite-temperature Bose-gas
Requires functions: Gaussian_dist_2D, TF_dist_2D, get_image_space
:param xy_mesh:
:type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
:param GpOD:
:type GpOD: float - Gaussian peak Optical Density (OD)
:param sigx:
:type sigx: float - Gaussian spread along the x-direction
:param sigy:
:type sigy: float - Gaussian spread along the y-direction (along gravity)
:param TFpOD:
:type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
:param rx:
:type rx: float - Thomas-Fermi radius along the x-direction
:param ry:
:type ry: float - Thomas-Fermi radius along the y-direction (along gravity)
:param xc:
:type xc: float - Cloud center along the x-direction (along gravity)
:param yc:
:type yc: float - Cloud center along the y-direction
:param os:
:type os: float - Constant offset

`round_sig(x: float, sig: int = 2)`
:

## Classes

`OqtantJob(**data: Any)`
: Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * bert_schemas.job.JobCreate
    * bert_schemas.job.JobBase
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `Config`
    :

    `external_id: uuid.UUID | None`
    :

    `omega_x: float`
    :

    `omega_y: float`
    :

    `pix_cal: float`
    :

    `sig_abs: float`
    :

    `time_submit: datetime.datetime | None`
    :

    ### Static methods

    `get_image_space(datafile=array([[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]]), centered='y')`
    :   Returns meshgrid of image coordinates
        :param datafile:
        :type datafile: (N,M) Matrix of Optical Density (OD) Data

    ### Methods

    `atom_numbers(self, bimodalfit_params, print_results=True)`
    :

    `atoms_2dplot(self, file_name=None, figsize=(12, 12), gridon=False)`
    :   Generate a 2D plot of atom OD (save or show)

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

    `atoms_3dplot(self, file_name=None, view_angle=-45, figsize=(10, 10))`
    :   Generate a 3D slice plot of atom OD

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param view_angle:
        :type view_angle: int (-180, 180). default -45
        :param figsize:
        :type figsize: tuple. default is (10,10)

    `atoms_sliceplot(self, file_name=None, sliceaxis='x', gridon=False)`
    :   Generate a 1D slice plot of atom OD in x or y

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param sliceaxis:
        :type sliceaxis: string 'x' or 'y'
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

    `calculate_temperature(self, bimodalfit_params)`
    :

    `fit_bimodal_data2D(self, xi=None, lb=None, ub=None)`
    :   Performs fit via trust region reflective algorithm.
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

    `IF(self)`
    :   Returns shaped IT image if it exists
        :returns: reshaped pixels numpy array (100,100)

    `TOF(self)`
    :   Returns shaped TOF image if it exists
        :returns: reshaped pixels numpy array (100,100)

    `plot_fit_results(self, fit_params, model='bimodal', file_name=None, plot_title=None)`
    :   Plot the results of a fit operation

                :param fit_params:
                :type fit_params: list of parameters from a fit operation
                :param model:
                :type model: string "bimodal", "TF", or "gaussian". default "bimodal"
                :param output:
                :type output: valid filename
                :param plot_title:
                :type plot_title: string title for the plot.
                    default "job: "+str(self.name)+"
        TOF fit: "+str(model)
