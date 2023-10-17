"""Components of the Tag model.  Stem + Optional Suffix = Tag."""
from enum import Enum

# This is here to avoid a circular import in parsers.time
EXP_TIME_ROUND_DIGITS: int = 6


class StemName(str, Enum):
    """Controlled list of Tag Stems."""

    output = "OUTPUT"
    input = "INPUT"
    intermediate = "INTERMEDIATE"
    input_dataset = "INPUT_DATASET"
    frame = "FRAME"
    movie = "MOVIE"
    stokes = "STOKES"
    movie_frame = "MOVIE_FRAME"
    task = "TASK"
    cs_step = "CS_STEP"
    modstate = "MODSTATE"
    dsps_repeat = "DSPS_REPEAT"
    calibrated = "CALIBRATED"  # A flag to indicate the data has been calibrated but not yet output
    quality = "QUALITY"
    exposure_time = "EXP_TIME"
    readout_exp_time = "READOUT_EXP_TIME"
    quality_task = "QUALITY_TASK"
    parameter = "PARAMETER"
    workflow_task = "WORKFLOW_TASK"
    debug = "DEBUG"


class Tag:
    """Controlled methods for creating tags from stems + optional suffixes."""

    @staticmethod
    def format_tag(stem: StemName | str, *parts):
        """
        Create a formatted tag sting given the input parts.

        Parameters
        ----------
        stem
            The name of the stem
        parts
            The remaining tag parts
        Returns
        -------
        The concatenated tag name
        """
        if isinstance(stem, Enum):
            stem = stem.value
        parts = [stem, *parts]
        return "_".join([str(part).upper() for part in parts])

    # Static Tags
    @classmethod
    def movie_frame(cls):
        """
        Return a movie frame tag.

        Returns
        -------
        A movie frame tag
        """
        return cls.format_tag(StemName.movie_frame)

    @classmethod
    def input(cls):
        """
        Return an input tag.

        Returns
        -------
        An input tag
        """
        return cls.format_tag(StemName.input)

    @classmethod
    def calibrated(cls) -> str:
        """
        Return a calibrated tag.

        Returns
        -------
        A calibrated tag
        """
        return cls.format_tag(StemName.calibrated)

    @classmethod
    def output(cls):
        """
        Return an output tag.

        Returns
        -------
        An output tag
        """
        return cls.format_tag(StemName.output)

    @classmethod
    def frame(cls):
        """
        Return a frame tag.

        Returns
        -------
        A frame tag
        """
        return cls.format_tag(StemName.frame)

    @classmethod
    def intermediate(cls):
        """
        Return an intermediate tag.

        Returns
        -------
        An intermediate tag
        """
        return cls.format_tag(StemName.intermediate)

    @classmethod
    def input_dataset_observe_frames(cls):
        """
        Return an input dataset observe frames tag.

        Returns
        -------
        An input dataset observe frames tag
        """
        return cls.format_tag(StemName.input_dataset, "observe_frames")

    @classmethod
    def input_dataset_calibration_frames(cls):
        """
        Return an input dataset calibration frames tag.

        Returns
        -------
        An input dataset calibration frames tag
        """
        return cls.format_tag(StemName.input_dataset, "calibration_frames")

    @classmethod
    def input_dataset_parameters(cls):
        """
        Return an input dataset parameters tag.

        Returns
        -------
        An input dataset parameters tag
        """
        return cls.format_tag(StemName.input_dataset, "parameters")

    @classmethod
    def movie(cls):
        """
        Return a movie tag.

        Returns
        -------
        A movie tag
        """
        return cls.format_tag(StemName.movie)

    @classmethod
    def debug(cls) -> str:
        """Return a debug tag."""
        return cls.format_tag(StemName.debug)

    # Dynamic Tags
    @classmethod
    def task(cls, ip_task_type: str):
        """
        Return a task tag for the given task type.

        Parameters
        ----------
        ip_task_type
            The task type
        Returns
        -------
        A task tag for the given type
        """
        return cls.format_tag(StemName.task, ip_task_type)

    @classmethod
    def cs_step(cls, n: int):
        """
        Return a cs step tag for the given cs_step number.

        Parameters
        ----------
        n
            The cs Step number

        Returns
        -------
        A cs Step tag for the given CS number
        """
        return cls.format_tag(StemName.cs_step, n)

    @classmethod
    def modstate(cls, n: int):
        """
        Return a modstate tag for the given modstate number.

        Parameters
        ----------
        n
            The modstate number

        Returns
        -------
        A modstate tag for the given modstate number
        """
        return cls.format_tag(StemName.modstate, n)

    @classmethod
    def stokes(cls, stokes_state: str) -> str:
        """
        Return a stokes tag for the given stokes value (I, Q, U, V).

        Parameters
        ----------
        stokes_state
            The input stokes state

        Returns
        -------
        A stokes tag for the given stokes state
        """
        return cls.format_tag(StemName.stokes, stokes_state)

    @classmethod
    def dsps_repeat(cls, dsps_repeat_number: int):
        """
        Return a dsps repeat tag for the given dsps_repeat number.

        Parameters
        ----------
        dsps_repeat_number
            The dsps repeat number

        Returns
        -------
        A dsps Repeat tag for the given dsps repeat number
        """
        return cls.format_tag(StemName.dsps_repeat, dsps_repeat_number)

    @classmethod
    def quality(cls, quality_metric: str) -> str:
        """
        Return a quality tag for the given quality metric.

        Parameters
        ----------
        quality_metric
            The input quality metric

        Returns
        -------
        A quality tag for the given quality metric
        """
        return cls.format_tag(StemName.quality, quality_metric)

    @classmethod
    def exposure_time(cls, exposure_time_s: float) -> str:
        """
        Return an FPA exposure time tag for the given exposure time.

        Parameters
        ----------
        exposure_time_s
            The exposure time in seconds
        Returns
        -------
        An exposure time tag for the given exposure time
        """
        return cls.format_tag(
            StemName.exposure_time, round(float(exposure_time_s), EXP_TIME_ROUND_DIGITS)
        )

    @classmethod
    def readout_exp_time(cls, readout_exp_time: float) -> str:
        """Return a readout exposure time tag for the given readout exposure time."""
        return cls.format_tag(
            StemName.readout_exp_time, round(float(readout_exp_time), EXP_TIME_ROUND_DIGITS)
        )

    @classmethod
    def quality_task(cls, quality_task_type: str) -> str:
        """
        Return a quality task tag for the given quality task type.

        Parameters
        ----------
        quality_task_type

        Returns
        -------
        A quality task tag for the given quality task type
        """
        return cls.format_tag(StemName.quality_task, quality_task_type)

    @classmethod
    def parameter(cls, object_name: str) -> str:
        """
        Return a unique parameter file tag.

        Parameters
        ----------
        object_name
            The unique value identifying this parameter file, typically the file name portion of a
            path e.g. For object_key 'parameters/abc123.fits' the object name is 'abc123.fits'

        Returns
        -------
        A parameter file tag for the given object_name
        """
        return cls.format_tag(StemName.parameter, object_name)

    @classmethod
    def workflow_task(cls, class_name: str) -> str:
        """
        Return a unique workflow task tag.

        Parameters
        ----------
        class_name
            The unique value identifying the workflow task class that wrote the file.
            e.g. TaskClass().__class__.__name__  # TaskClass

        Returns
        -------
        A workflow task class tag for the given class_name
        """
        return cls.format_tag(StemName.workflow_task, class_name)
