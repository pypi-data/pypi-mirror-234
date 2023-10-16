from enum import Enum

from tecton_core import conf


class ValidationMode(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "auto"


def set_validation_mode(mode: ValidationMode):
    """Convenience utility to set the Tecton object validation mode for the lifetime of the Python process.

    Must be either "explicit" (tecton.ValidationMode.EXPLICIT) or "auto" (tecton.ValidationMode.AUTOMATIC). "explicit"
    is the default.

    In "auto" mode, locally defined Tecton objects will automatically trigger validation when needed.

    .. code-block:: python

        import tecton

        tecton.set_validation_mode("auto")

        credit_scores_batch = tecton.BatchSource(
            name='credit_scores_batch',
            batch_config=tecton.HiveConfig(database='demo_fraud', table='credit_scores'),
        )

        df = credit_scores_batch.get_dataframe()  # Will automatically trigger validation.

    In "explicit" mode, locally defined Tecton objects must be validated before they can be used to execute many
    methods.

    .. code-block:: python

        import tecton

        tecton.set_validation_mode("auto")

        credit_scores_batch = tecton.BatchSource(
            name='credit_scores_batch',
            batch_config=tecton.HiveConfig(database='demo_fraud', table='credit_scores'),
        )

        credit_scores_batch.validate()

        df = credit_scores_batch.get_dataframe()


    Note: Tecton objects fetched from the Tecton backend have already been validated during `tecton plan` and do
    not need to be re-validated.
    """
    if mode is None or mode.lower() not in (
        ValidationMode.AUTOMATIC,
        ValidationMode.EXPLICIT,
    ):
        raise ValueError(f"Mode should be one of 'auto' or 'explicit', got {mode}")
    conf.set("TECTON_VALIDATION_MODE", mode)
