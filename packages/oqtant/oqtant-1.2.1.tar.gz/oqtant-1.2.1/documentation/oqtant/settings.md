Module oqtant.settings
======================

Classes
-------

`Settings(**values: Any)`
:   Base class for settings, allowing values to be overridden by environment variables.

    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku and any 12 factor app design.

    ### Ancestors (in MRO)

    * pydantic.env_settings.BaseSettings
    * pydantic.main.BaseModel
    * pydantic.utils.Representation

    ### Class variables

    `auth0_audience: str`
    :

    `auth0_base_url: str`
    :

    `auth0_client_id: str`
    :

    `auth0_scope: str`
    :

    `base_url: str`
    :

    `max_ind_var: int`
    :

    `max_job_batch_size: int`
    :

    `signin_local_callback_url: str`
    :
