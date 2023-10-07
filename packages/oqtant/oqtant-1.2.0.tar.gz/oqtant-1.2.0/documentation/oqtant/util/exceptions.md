Module oqtant.util.exceptions
=============================

Classes
-------

`AuthorizationError(message=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`DatabaseError(message)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`JobError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * oqtant.util.exceptions.JobPlotFitError
    * oqtant.util.exceptions.JobPlotFitMismatchError

`JobPlotFitError()`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * oqtant.util.exceptions.JobError
    * builtins.Exception
    * builtins.BaseException

`JobPlotFitMismatchError()`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * oqtant.util.exceptions.JobError
    * builtins.Exception
    * builtins.BaseException

`JobReadError(message)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`JobWriteError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`ParameterError(message)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`ValidationError(message)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`VersionWarning(message)`
:   Base class for warning categories.

    ### Ancestors (in MRO)

    * builtins.Warning
    * builtins.Exception
    * builtins.BaseException
