v4.1.4 (2023-10-11)
===================

Misc
----

- Update metadata-store-api calls to use new framework paradigms for authorization, queries, and mutations. (`#150 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/150>`__)
- Centralize environment configuration using the dkist-service-configuration library. (`#150 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/150>`__)


v4.1.3 (2023-09-29)
===================

Misc
----

- Clean up APM spans in the WriteL1Frame task class. (`#149 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/149>`__)


v4.1.2 (2023-09-08)
===================

Misc
----

- Use the latest version dkist-processing-core which adds the ability to select different resource queues for tasks in a workflow. (`#148 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/148>`__)


v4.1.1 (2023-09-05)
===================

Misc
----

- Change how intermediate files are named to use a sequence number to enforce uniqueness across identically tagged files. (`#146 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/146>`__)
- Log when APM spans are created to provide some info in the case of SIGTERM process failures. (`#147 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/147>`__)


v4.1.0 (2023-07-28)
===================

Features
--------

- New Buds and Flower to parse per-readout exposure time and number of readouts per FPA. (`#145 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/145>`__)


v4.0.3 (2023-07-26)
===================

Misc
----

- Updating dkist-header-validator to include python 3.10 support.


v4.0.2 (2023-07-17)
===================

Bugfixes
--------

- Updates to support new major revisions of `pillow` and `pydantic`. (`#142 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/142>`__)


Misc
----

- Update to latest dkist-header-validator. (`#143 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/143>`__)


v4.0.1 (2023-07-11)
===================

Misc
----

- Update core dependency for airflow upgrade. (`#143 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/143>`__)


v4.0.0 (2023-06-29)
===================

Misc
----

- Move to dkist-processing-core 1.5.0 which includes airflow 2.6.2 and python 3.11 support. (`#141 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/141>`__)


v3.0.0 (2023-06-27)
===================

Features
--------

- Tag all files written with the name of the task that wrote the file.  This is expected to be helpful in fault analysis. (`#138 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/138>`__)
- Add DEBUG tags for writing files that are easily identifiable for later retrieval. (`#139 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/139>`__)
- Base task to facilitate "trial" workflows that save specific (and arbitrary) pipeline products to a special development bucket for further analysis. (`#139 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/139>`__)
- Redesign `WorkflowTaskBase` `read` and `write` to accept decoders and encoders. The result is that `read` and `write` are now the methods to be
  used in *all* cases of reading and writing (i.e., we no longer need different read/write functions for different data types). A library of codecs
  is also provided for all data types currently used. (`#140 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/140>`__)


v2.7.0 (2023-05-17)
===================

Misc
----

- Refactor parsing task to support more varied use cases by defining more abstract components that can be composed. (`#137 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/137>`__)


v2.6.0 (2023-05-05)
===================

Misc
----

- Update dkist-processing-core to 1.4.0 which includes an upgrade to airflow 2.6.0 (`#136 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/136>`__)


v2.5.0 (2023-05-02)
===================

Bugfixes
--------

- Replace `astropy.time.Time` with `datetime.datetime` for reading header "DATE-OBS" values in `ParseL0InputData` task. This should produce a very large speedup in the task when parsing large datasets. (`#134 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/134>`__)


Misc
----

- Set WAVEMIN and WAVEMAX header keys based on abstract method get_wavelength_range implemented by each instrument (`#133 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/133>`__)
- Improved `__repr__` in `CSStep` and `FitsAccessBase` objects. The latter affects all `*FitsAccess` subclasses as well. (`#135 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/135>`__)


v2.4.1 (2023-04-14)
===================

Misc
----

- remove spectral line support from dkist-processing-common because it now resides in `dkist-spectral-lines <https://pypi.org/project/dkist-spectral-lines/>`_ (`#128 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/128>`__)


v2.4.0 (2023-04-12)
===================

Features
--------

- Make histogram plots of all parameters that are free in local PolCal fits. (`#132 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/132>`__)


Misc
----

- Update polcal quality metric machinery for new `dkist-processing-pac` version (>=2.0.0). (`#129 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/129>`__)
- Normalize use of `logger.[thing]` across repo. Previously had also been using `logging.[thing]`. (`#130 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/130>`__)


v2.3.0 (2023-02-17)
===================

Misc
----

- Update dkist-processing-core to include new version of Airflow


v2.2.0 (2023-02-03)
===================

Features
--------

- Parse proposal and experiment IDs to aggregate information and include it in L1 headers. (`#126 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/126>`__)


v2.1.0 (2023-01-31)
===================

Features
--------

- Added capability to load parameters from files. (`#125 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/125>`__)


v2.0.0 (2022-12-15)
===================

Features
--------

- Expose tag removal at `WorkflowTaskBase` level. Thus tag removal is now directly accessible to all instrument tasks. (`#123 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/123>`__)


Bugfixes
--------

- Fix bug that caused `TagDB.remove` to fail silently if called directly. (`#123 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/123>`__)


Misc
----

- *Require* instruments to provide `DATE-END` calculation in `WriteL1` task. (`#120 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/120>`__)


v1.2.2 (2022-12-05)
===================

Bugfix
------

- Movie file is uploaded separately as movie headers need to be handled.


v1.2.1 (2022-12-02)
===================

Misc
----

- Movie file is uploaded during the Globus transfer instead of separately. (`#121 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/121>`__)
- Add environment variable to configure auth client transport parameters such as retries. (`#122 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/122>`__)


v1.2.0 (2022-11-15)
===================

Misc
----

- Use updated dkist-processing-core version 1.2.0.


v1.1.0 (2022-11-14)
===================

Bugfixes
--------

- Allow quality metric values to be sent to encoder as `np.float32` (which is a single number) type. (`#117 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/117>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#119 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/119>`__)


v1.0.3 (2022-11-09)
===================

Bugfixes
--------

- Improve Globus event logging (`#118 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/118>`__)


v1.0.2 (2022-11-08)
===================

Bugfixes
--------

- Handle an empty Globus event list. (`#116 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/116>`__)


v1.0.1 (2022-11-08)
===================

Misc
----

- Be more tolerant of globus error events during a transfer because globus retries and may recover. (`#115 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/115>`__)


v1.0.0 (2022-11-02)
===================

Misc
----

- Upgrade version of the redis client library to move with the redis infrastructure upgrade to 7.x (`#114 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/114>`__)


v0.27.1 (2022-11-02)
====================

Misc
----

- Use updated dkist-processing-core version 1.1.2.  Task startup logging enhancements.


v0.27.0 (2022-10-26)
====================

Bugfixes
--------

- Change `VELOSYS` keyword type from bool to float. (`#113 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/113>`__)


v0.26.2 (2022-10-26)
====================

Bugfixes
--------

- Remove compression and other keys from the headers before refactoring into tables. (`#112 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/112>`__)


v0.26.1 (2022-10-20)
====================

Misc
----

- Make python 3.10 the minimum supported version (`#109 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/109>`__)
- Increase the HTTP timeout for retryable status codes when connecting to the metadata-store-api. (`#111 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/111>`__)


v0.26.0 (2022-10-18)
====================

Features
--------

- Add PolCal metric showing the constant parameters (mirror and p_y) used in polcal model. (`#106 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/106>`__)


Bugfixes
--------

- Re-cast polcal transmission values in quality report as percentages to increase the number of sig figs. (`#106 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/106>`__)
- Use hard-coded location of DKIST to never again need to rely on querying `astropy` databases. (`#107 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/107>`__)


v0.25.2 (2022-10-11)
====================

Bugfixes
--------

- Fix call to globus task status API which fails on transfers greater than 60s (`#110 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/110>`__)


v0.25.1 (2022-10-11)
====================

Bugfixes
--------

- Make dkist-processing-core a pinned dependency because otherwise the automated processing framework can backrev airflow with undesirable results. (`#108 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/108>`__)


Misc
----

- Upgrade to use the globus-sdk version 3.x. (`#108 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/108>`__)


v0.24.0 (2022-09-16)
====================

Features
--------

- Refactor the input dataset mix in to support input dataset parts being accessed individually from the metadata-store-api (`#105 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/105>`__)
- Added the following keys to the 214 headers.
  - IDSPARID: Input Dataset Part Id for parameters
  - IDSOBSID: Input Dataset Part Id for observation frames
  - IDSCALID: Input Dataset Part Id for calibration frames
  - WKFLNAME: Workflow Name
  - WKFLVERS: Workflow Version (`#105 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/105>`__)


v0.23.0 (2022-08-08)
====================

Misc
----

- Update minimum required version of `dkist-processing-core` due to breaking changes in workflow naming.

v0.22.1 (2022-08-03)
====================

Bugfixes
--------

- Use nearest neighbor interpolation to resize movie frames. This helps avoid weirdness if the maps are very small. (`#101 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/101>`__)


Misc
----

- Add logging to WriteL1Frame. (`#103 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/103>`__)
- Improve/add test coverage of polcal quality metric generation. (`#104 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/104>`__)


v0.22.0 (2022-07-20)
====================

Features
--------

- Add microsecond precision to datetimes in headers. (`#98 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/98>`__)
- Compression tile size will revert to defaults chosen by astropy unless otherwise specified in the recipe run configuration. (`#99 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/99>`__)
- Prevent overwriting files on /scratch unless specified with the overwrite flag. (`#100 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/100>`__)


v0.21.1 (2022-07-12)
====================

Bugfixes
--------

- Expose polcal_label_list as property on SubmitQuality so that the polcal metrics actually get built.

v0.21.0 (2022-07-12)
====================

Features
--------

- Add support for new Polcal quality metrics. (`#97 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/97>`__)
- Replace "Polarimetric Noise" metric with "Sensitivity" metric that applies to both non-polarimetric and polarimetric data. (`#97 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/97>`__)
- Remove "Polarimetric Sensitivity" metric. (`#97 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/97>`__)


Misc
----

- Big refactor of `QualityMixin` to split up different metric task types and improve readability. (`#97 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/97>`__)


v0.20.0 (2022-06-15)
====================

Bugfixes
--------

- Repair reference to dataset ID in constructing L1 filenames. (`#96 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/96>`__)


v0.19.0 (2022-06-15)
====================

Features
--------

- Change how L1 filenames are constructed. (`#95 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/95>`__)


v0.18.0 (2022-05-02)
====================

Bugfixes
--------

- Use CAM__004 (XPOSURE) as fpa_exposure_time (`#93 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/93>`__)


v0.17.4 (2022-04-22)
====================

Bugfixes
--------

- Change movie codec to allow for playback on Chrome browsers. (`#94 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/94>`__)


v0.17.3 (2022-04-19)
====================

Bugfixes
--------

- Look for Globus vestigial folders one level higher

v0.17.2 (2022-04-19)
====================

Misc
----

- Delete folder objects created by the Globus transfer of Level 1 data to the object store. (`#92 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/92>`__)


v0.17.1 (2022-03-31)
====================

Features
--------

- Sentinel `Thorn` class that indicates a Bud/Stem shouldn't be picked. Allows for Buds that just check stuff without returning a value. (`#90 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/90>`__)


Misc
----

- Increase verbosity in message publishing APM steps (`#89 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/89>`__)


Documentation
-------------

- Add changelog (`#91 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/91>`__)


v0.17.0 (2022-03-24)
====================

Features
--------

- Exposure "teardown_enabled" configuration kwarg to optionally skip the Teardown task (`#85 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/85>`__)
- Add `.from_path` class method to FitsAccess (`#88 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/88>`__)


Bugfixes
--------

- Fix name of "fpa_exposure_time" parameter (`#86 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/86>`__)
- Report correct units (adu / s) for quality report RMS values (`#87 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/87>`__)
- Save resources in quality metrics task by using paths instead of full FitsAccess objects (`#88 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/88>`__)


v0.16.3 (2022-03-18)
====================

Bugfixes
--------

- Remove some vestigial raw `self.apm_step` calls

v0.16.2 (2022-03-18)
====================

Features
--------

- Increase usefulness of APM logging with type-specific spans (`#84 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/84>`__)

v0.16.1 (2022-03-10)
====================

Misc
----

- Add graphviz to build env so docs render correctly

v0.16.0 (2022-03-10)
====================

First version to be used on DKIST summit data
