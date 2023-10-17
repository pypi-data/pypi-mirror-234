v2.7.5 (2023-10-11)
===================

Misc
----

- Use latest version of dkist-processing-common (4.1.4) which adapts to the new metadata-store-api. (`#126 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/126>`__)


v2.7.4 (2023-09-29)
====================

Misc
----

- Update dkist-processing-common to elimate APM steps in writing L1 data.


v2.7.3 (2023-09-21)
===================

Misc
----

- Update dkist-fits-specifications to conform to Revision I of SPEC-0122.



v2.7.2 (2023-09-08)
===================

Misc
----

- Use latest version of dkist-processing-common (4.1.2) which adds support for high memory tasks. (`#125 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/125>`__)


v2.7.1 (2023-09-06)
===================

Misc
----

- Update to version 4.1.1 of dkist-processing-common which primarily adds logging and scratch file name uniqueness. (`#124 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/124>`__)


v2.7.0 (2023-07-28)
===================

Bugfixes
--------

- Use the exposure time *per readout* to compute and correct for dark signal. A single FPA (i.e., frame) can be
  made up of multiple on-camera readouts and it is the exposure time of a single readout that is important for correcting
  the dark current. (`#123 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/123>`__)


v2.6.3 (2023-07-26)
===================

Misc
----

- Update dkist-fits-specifications to include ZBLANK.


v2.6.2 (2023-07-26)
===================

Misc
----

- Update dkist-processing-common to upgrade dkist-header-validator to 4.1.0.


v2.6.1 (2023-07-17)
===================

Misc
----

- Update dkist-processing-common and the dkist-header-validator to propagate dependency breakages in PyYAML < 6.0. (`#122 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/122>`__)


v2.6.0 (2023-07-14)
===================

Features
--------

- Enable intensity mode observations to be calibrated with polarized calibration data. (`#121 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/121>`__)


Bugfixes
--------

- Include Lamp Gain intermediate files in default trial output. (`#120 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/120>`__)


v2.5.1 (2023-07-11)
===================

Misc
----

- Update dkist-processing-common to upgrade Airflow to 2.6.3.


v2.5.0 (2023-06-29)
===================

Misc
----

- Update to python 3.11 and update library package versions. (`#119 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/119>`__)


v2.4.0 (2023-06-27)
===================

Features
--------

- Wield `*-common`'s development framework to tag DEBUG frames and create new trial workflows for local and PROD-level testing. (`#116 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/116>`__)


Misc
----

- Update to support `dkist-processing-common` 3.0.0. Specifically the new signature of some of the `FitsDataMixin` methods. (`#117 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/117>`__)


v2.3.1 (2023-06-15)
===================

Bugfixes
--------

- Fix failure in Geometric task that happened when some modstates had a a different number of identified hairline regions than others. (`#118 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/118>`__)


v2.3.0 (2023-05-17)
===================

Misc
----

- Bumping common to 2.7.0: ParseL0InputData --> ParseL0InputDataBase, constant_flowers --> constant_buds (`#115 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/115>`__)


v2.2.0 (2023-05-16)
===================

Bugfixes
--------

- Lots of small updates to harden the beam angle calculation against pathological data. We are now resistant to lamp data with large gradients and/or data with a high density of bad pixels. (`#114 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/114>`__)


v2.1.1 (2023-05-05)
===================

Misc
----

- Update dkist-processing-common to 2.6.0 which includes an upgrade to airflow 2.6.0


v2.1.0 (2023-05-02)
===================

Features
--------

- Support for a parameter that sets the number of spatial bins used when computing demodulation matrices. This is mostly to speed up testing and deployment; real science data will probably not be binned at all. (`#112 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/112>`__)


Misc
----

- Offload calculation of "WAVEMIN/MAX" in L1 headers to new functionality in `*-common` that uses the already-defined `get_wavelength_range`. The result is that this logic now only lives in one place. (`#113 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/113>`__)


v2.0.2 (2023-04-24)
===================

Misc
----

- Update `dkist-fits-specifications` to include new header keys.


v2.0.1 (2023-04-17)
===================

Bugfixes
--------

- Correct the determination of which spectral lines should be present in L1 frames. (`#111 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/111>`__)


v2.0.0 (2023-04-13)
===================

Features
--------

- Large improvements to gain algorithm. Primary improvement is usage of lamp gain images to help separate optical/spectral signals
  and improve solar characteristic spectra removal from solar gain images. (`#105 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/105>`__)
- Improve spatial residuals in polarimetric data by computing a demodulation matrix for every spatial pixel and then
  smoothing the resulting demodulation matrices in the spatial dimension. (`#106 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/106>`__)
- Normalize Q, U, and V polarimetric beams by their respective Stokes-I prior to beam combination, then multiply the combination
  by the average Stokes-I data. (`#107 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/107>`__)
- Improvement to accuracy of beam angle calculation. The angle is now measured directly from the hairlines instead of using a Hough transform,
  which has less accuracy due to the width of the hairlines. (`#108 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/108>`__)
- Use new and improved PAC fit mode for improved polarimetric accuracy. Also update code to support/interact with
  `dkist-processing-pac` >= 2.0.0. This is mostly renaming kwargs on API calls. Also removed unneeded dummy dimensions
  and renamed a matrix multiple function. (`#109 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/109>`__)


Misc
----

- Replace `logging.[thing]` with `logging42.logger.[thing]` for logging bliss. (`#104 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/104>`__)


Documentation
-------------

- Add machinery for a "Scientific" changelog that tracks only those changes that affect L1 output data. (`#110 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/110>`__)


v1.6.1 (2023-04-10)
===================

Misc
----
- FITS header specification update to add spectral line keys.


v1.6.0 (2023-03-16)
===================

Misc
----
- FITS header specification update to add new keys and change some units.


v1.5.6 (2023-03-01)
===================

Misc
----

- Logging fix in the dkist-header-validator.


v1.5.5 (2023-02-22)
===================

Misc
----

- Move the header specification to revision H of SPEC-0122.


v1.5.4 (2023-02-17)
===================

Misc
----

- Update dkist-processing-common due to an Airflow upgrade.


v1.5.3 (2023-02-06)
===================

Features
--------

- Bump `dkist-processing-common` to allow inclusion of multiple proposal or experiment IDs in headers.


v1.5.2 (2023-02-02)
===================

Misc
----

- Bump FITS specification to revision G.


v1.5.1 (2023-01-31)
===================

Misc
----

- Don't include always-unused polcal dark frames as part of the frame counts quality metric for the Background task. (`#102 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/102>`__)
- Bump `dkist-processing-common`

v1.5.0 (2022-12-15)
===================

Features
--------

- Add parameter to switch on/off the background light correction. This parameter is based of the time *of observation* not the time of pipeline execution. (`#101 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/101>`__)


Bugfixes
--------

- Remove overriding method to allow `HLSVERS` to be written into the data. (`#100 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/100>`__)


v1.4.2 (2022-12-05)
===================

Bugfix
------

- Update dkist-processing-common to include movie headers in transfers.


v1.4.1 (2022-12-02)
===================

Misc
----

- Update dkist-processing-common to improve handling of Globus issues.


v1.4.0 (2022-11-15)
====================

Misc
----

- Update dkist-processing-common


v1.3.0 (2022-11-14)
===================

Bugfixes
--------

- Fix bug in how final beam overlap is computed. (`#97 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/97>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#99 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/99>`__)


v1.2.4 (2022-11-09)
===================

Misc
----

- Update dkist-processing-common to improve Globus event logging


v1.2.3 (2022-11-08)
===================

Misc
----

- Update dkist-processing-common to handle empty GLobus event lists


v1.2.2 (2022-11-08)
===================

Misc
----

- Update dkist-processing-common to include Globus retries in transfer tasks


v1.2.1 (2022-11-04)
===================

Bugfixes
--------

- Change how intermediate CALIBRATED frames are saved so that the L1 FRAMEVOL header key reports the correct on-disk size of the compressed data. (`#98 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/98>`__)


v1.2.0 (2022-11-02)
===================

Misc
----

- Upgraded dkist-processing-math, dkist-processing-pac, and dkist-processing-common to production versions (`#96 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/96>`__)


v1.1.1 (2022-11-02)
====================

Misc
--------

- Use updated dkist-processing-core version 1.1.2.  Task startup logging enhancements.


v1.1.0 (2022-11-01)
===================

Bugfixes
--------

- Bump `dkist-processing-pac` to 0.9.0 to fix bug in how Telescope Mueller matrices were calculated. (`#95 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/95>`__)


v1.0.0 (2022-10-31)
====================

Misc
----

- Scientific acceptance of the VISP pipeline.



v0.26.1 (2022-10-27)
====================

Features
--------

- All Background Light parameters are now wavelength dependent for finer control. (`#92 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/92>`__)


Misc
----

- Update dependency versions in "grogu" dev testing install target. (`#92 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/92>`__)


v0.26.0 (2022-10-26)
====================

Misc
----

- Update versions of dkist-processing-common and dkist-fits-specifications. (`#94 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/94>`__)


v0.25.2 (2022-10-26)
====================

Misc
----

- Update versions of dkist-processing-common and astropy. (`#93 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/93>`__)


v0.25.1 (2022-10-20)
====================

Misc
----

- Require python 3.10+. (`#91 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/91>`__)


v0.25.0 (2022-10-19)
====================

Bugfixes
--------

- Dataset axes in L1 headers now assign dynamically based on L0 CTYPE headers. (`#90 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/90>`__)


v0.24.0 (2022-10-19)
====================

Features
--------

- Trim L1 frames to only include the region where both beams overlap. (`#87 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/87>`__)


v0.23.0 (2022-10-19)
====================

Features
--------

- Expose parameter to switch on/off the fitting and removal of a linear intensity trend across a whole PolCal Calibration Sequence. (`#86 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/86>`__)


v0.22.0 (2022-10-18)
====================

Misc
----

- Only record the constant polcal parameters to the quality report once (i.e., not for both beams; it's the same for both). (`#85 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/85>`__)


v0.21.3 (2022-10-18)
====================

Misc
----

- Even more memory savings in the BackgroundLight algorithm. (`#89 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/89>`__)


v0.21.2 (2022-10-18)
====================

Misc
------

- Changing metrics included in quality reports



v0.21.1 (2022-10-12)
====================

Bugfix
------

- Moving to a new version of dkist-processing-common to fix a Globus bug


v0.21.0 (2022-10-11)
====================

Misc
----

- Upgrading to a new version of Airflow


v0.20.1 (2022-10-06)
====================

Misc
----

- Refactor spatial binning in Background Light algorithm to use less memory. (`#88 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/88>`__)


v0.20.0 (2022-10-05)
====================

Features
--------

- Add functionality to compute and correct for residual background light (`#84 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/84>`__)


Misc
----

- Remove world coordinate system transposition to level set all L1 data. (`#83 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/83>`__)


v0.19.4 (2022-09-16)
====================

Misc
----

- Update tests for new input dataset document format from `*-common >= 0.24.0` (`#82 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/82>`__)


v0.19.3 (2022-09-14)
====================

Misc
----

- FITS spec was using incorrect types for some keys.


v0.19.2 (2022-09-12)
====================

Misc
----

- Updating the underlying FITS specification used.

v0.19.0 (2022-09-08)
====================

Features
--------

- Use bi-quintic interpolation for rotation and offset corrections to minimize residuals in very narrow lines. (`#77 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/77>`__)
- Big update of gain algorithm to use high-pass-filtered lamp gains and more thoughtfully filtered solar gains in tandem
  to remove both detector and optical response variations. (`#77 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/77>`__)
- Compute beam 2's rotation angle so that its spectra line up with those from beam 1 (instead of just straightening the hairlines). (`#81 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/81>`__)
- Improve beam/modstate offset matching in cases where the beams have low-frequency illumination differences. (`#81 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/81>`__)


Bugfixes
--------

- Update version of `dkist-processing-math` to fix bug in angle finding algorithm. (`#78 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/78>`__)


Misc
----

- Re-pin `asdf == 2.10.1` in "grogu" install target. Needed because `airflow`. (`#79 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/79>`__)
- Move to `scipy==1.9.0`. This has some implications with calculations in the WriteL1 task; constant arrays will now cause this task to fail. (`#80 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/80>`__)


v0.18.1 (2022-08-09)
====================

Misc
----

- Corrected workflow naming in docs.


v0.18.0 (2022-08-08)
====================

Misc
----

- Update minimum required version of `dkist-processing-core` due to breaking changes in workflow naming.


v0.17.1 (2022-08-03)
====================

Bugfixes
--------

- Use nearest neighbor interpolation to resize movie frames. This helps avoid weirdness if the maps are very small. (`#101 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/101>`__)


v0.17.0 (2022-07-28)
====================

Features
--------

- Add ability to handle transposed WCS headers and reorder them correctly in output L1 data. (`#76 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/76>`__)


v0.16.0 (2022-07-21)
====================

Bugfixes
--------

- Fix ordering of dataset header keywords. (`#75 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/75>`__)

Features
--------

- Bumped version of dkist-processing-common in setup.cfg. The change adds microsecond support to datetimes, prevents quiet file overwriting by default, and sets the default fits compression tile size to astropy defaults.


v0.15.0 (2022-07-14)
====================

Features
--------

- Save PolCal metrics for inclusion in quality report document. (`#71 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/71>`__)
- Use bi-cubic interpolation when upsampling to produce smoother demodulation matrices. (`#72 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/72>`__)
- Modstate/beam offset calculation now ignores regions that aren't associated with strong spectral features when computing offset. (`#74 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/74>`__)


v0.14.1 (2022-06-27)
====================

Bugfixes
--------

- Bumped version of dkist-header-validator in setup.cfg.
  The change fixes a bug in handling multiple fits header commentary cards (HISTORY and COMMENT). (`#73 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/73>`__)


v0.14.0 (2022-06-20)
====================

Features
--------

- Change how L1 filenames are constructed.

v0.13.1 (2022-06-14)
====================

Features
--------

- Add capability to handle summit aborts or cancellations mid observation. (`#69 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/69>`__)


v0.13.0 (2022-06-13)
====================

Features
--------

- Compute Calibration Unit parameters once over entire FOV prior to fitting demodulation matrices for the requested bins (`#70 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/70>`__)


v0.12.1 (2022-06-03)
====================

Misc
----

- Update for new `dkist_processing_pac` API (version 0.7.0) (`#68 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/68>`__)


v0.12.0 (2022-05-12)
====================

Features
--------

- Remove `RewriteInputFramesToCorrectHeaders` and the "l0_to_l1_visp_rewrite_input_headers_workflow". (`#67 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/67>`__)
- Use map scan numbers to build movie images. (`#67 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/67>`__)
- Move determination of map scan structure to the `Parse` task. (`#67 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/67>`__)
- Use map scan numbers as the DINDEXn value for the second spatial dimension. (`#67 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/67>`__)


Misc
----

- Replace all code usages of "DSPS repeat" with "map scan". (`#67 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/67>`__)


v0.11.0 (2022-05-02)
====================

Features
--------

- Allow non-integer binning of FOV when computing demodulation matrices (`#64 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/64>`__)

Bugfixes
--------

- Use new version of `dkist-processing-common` (0.18.0) to correct source for "fpa exposure time" keyword

Misc
----

- Raise KeyError if a header doesn't have a key expected by the `VispFitsAccess` classes (`#65 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/65>`__)


v0.10.0 (2022-04-28)
====================

Features
--------

- FITS specification now uses Rev. F of SPEC0122 as a base. (`#66 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/66>`__)


v0.9.1 (2022-04-22)
===================

Bugfixes
--------

- Change movie codec for better compatibility.

v0.9.0 (2022-04-21)
===================

Features
--------

- Add support for (somewhat) arbitrary sampling of FOV when computing demodulation matrices (`#62 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/62>`__)
- Save best-fit flux from Calibration Unit fit (`#63 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/63>`__)


Misc
----

- Polcal binning values moved from `dkist_processing_visp.models.constants` to `dkist_processing_visp.models.parameters` (`#62 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/62>`__)
- Collect InstPolCal QA-esq object generation into a single function (`#63 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/63>`__)


v0.8.3 (2022-04-19)
===================

Misc
----

- Bump version of `dkist-processing-common` to 0.17.3

v0.8.2 (2022-04-06)
===================

Misc
----

- Refactor Science task to save some I/O (`#61 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/61>`__)


v0.8.1 (2022-04-04)
===================

Features
--------

- APM steps added to RewriteInputFramesToCorrectHeaders task.


v0.8.0 (2022-04-04)
===================

Features
--------

- Fail fast if multiple frames are found for a single (dsps, modstate, raster step) tuple. (`#58 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/58>`__)
- New workflow that includes a task to dynamically overwrite DKIST008 and DKIST009 header values. (`#60 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/60>`__)


v0.7.2 (2022-03-25)
===================

Bugfixes
--------
- Restore correct passing of PA&C fit parameters

v0.7.1 (2022-03-25)
===================

Bugfixes
--------
- Don't fail in spectrographic mode with compressed inputs

v0.7.0 (2022-03-25)
===================

Features
--------

- Don't split beams in separate task (`#53 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/53>`__)
- Fail fast if an incomplete raster map is detected (`#54 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/54>`__)


Bugfixes
--------

- Fix DPNAME descriptions in L1 data and start DINDEX3 at 1 (`#50 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/50>`__)
- Processed polarimetric frames now have DATE-BEG equal to earliest input modstate and DATE-END equal to latest input modstate + exposure time (`#52 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/52>`__)
- Fix negative sign error and issue with low slit-hairline contrast in Geometric task (`#56 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/56>`__)


Misc
----

- Update `VispL0QualityMetrics` to use new paradigm in `dkist-procesing-common` v0.17.0 `#55 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/55>`__


v0.6.0 (2022-03-18)
===================

Features
--------

- Increase usefulness of APM logging for debugging pipeline performance (`#48 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/48>`__)


Bugfixes
--------

- Fix bug mismatching tags when writing intermediate frames (`#49 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/49>`__)


Documentation
-------------

- Update docs to conform to pydocstyle (`#51 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/51>`__)


v0.5.1 (2022-03-11)
===================

Documentation
-------------

- Use `use_M12` PA&C Fit mode as default
- Add full code documentation (`#45 <https://bitbucket.org/dkistdc/dkist-processing-visp/pull-requests/45>`__)

v0.5.1 (2022-03-10)
===================

First release to be run on DKIST summit data
