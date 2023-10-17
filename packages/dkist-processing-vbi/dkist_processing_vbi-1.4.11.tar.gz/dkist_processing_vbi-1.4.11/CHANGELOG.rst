v1.4.11 (2023-10-11)
====================

Misc
----

- Use latest version of dkist-processing-common (4.1.4) which adapts to the new metadata-store-api. (`#53 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/53>`__)


v1.4.10 (2023-09-29)
====================

Misc
----

- Update dkist-processing-common to elimate APM steps in writing L1 data.


v1.4.9 (2023-09-21)
===================

Misc
----

- Update dkist-fits-specifications to conform to Revision I of SPEC-0122.


v1.4.8 (2023-09-08)
===================

Misc
----

- Use latest version of dkist-processing-common (4.1.2) which adds support for high memory tasks. (`#52 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/52>`__)


v1.4.7 (2023-09-06)
===================

Misc
----

- Update to version 4.1.1 of dkist-processing-common which primarily adds logging and scratch file name uniqueness. (`#50 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/50>`__)


v1.4.6 (2023-07-28)
===================

Misc
----

- Bump dkist-processing-common to 4.1.0


v1.4.5 (2023-07-26)
===================

Misc
----

- Update dkist-fits-specifications to include ZBLANK.


v1.4.4 (2023-07-26)
===================

Misc
----

- Update dkist-processing-common to upgrade dkist-header-validator to 4.1.0.


v1.4.2 (2023-07-17)
===================

Misc
----

- Update dkist-processing-common and the dkist-header-validator to propagate dependency breakages in PyYAML < 6.0. (`#49 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/49>`__)


v1.4.1 (2023-07-11)
===================

Misc
----

- Update dkist-processing-common to upgrade Airflow to 2.6.3.


v1.4.0 (2023-06-29)
===================

Misc
----

- Update to python 3.11 and update library package versions. (`#48 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/48>`__)


v1.3.1 (2023-06-27)
===================

Misc
----

- Update to support `dkist-processing-common` 3.0.0. Specifically the new signature of some of the `FitsDataMixin` methods. (`#47 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/47>`__)


v1.3.0 (2023-05-17)
===================

Misc
----

- Bumping common to 2.7.0: ParseL0InputData --> ParseL0InputDataBase, constant_flowers --> constant_buds (`#46 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/46>`__)


v1.2.1 (2023-05-05)
===================

Misc
----

- Update dkist-processing-common to 2.6.0 which includes an upgrade to airflow 2.6.0


v1.2.0 (2023-05-02)
===================

Features
--------

- Add support for "subcycling" that can result in multiple repeats of a mosaic for a single DSPS repeat. (`#41 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/41>`__)


Misc
----

- Offload calculation of "WAVEMIN/MAX" in L1 headers to new functionality in `*-common` that uses the already-defined `get_wavelength_range`. The result is that this logic now only lives in one place. (`#44 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/44>`__)


Documentation
-------------

- Replace use of `logging.[thing]` with `logger.[thing]` from `logging42`. (`#42 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/42>`__)
- Add machinery for a "Scientific" changelog that tracks only those changes that affect L1 output data. (`#43 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/43>`__)


v1.1.11 (2023-04-24)
====================

Misc
----

- Update `dkist-fits-specifications` to include header keys for tracking VBI mosaics.

v1.1.10 (2023-04-17)
====================

Bugfixes
--------

- Correct the determination of which spectral lines should be present in L1 frames. (`#40 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/40>`__)


v1.1.9 (2023-04-13)
===================

Misc
----
- Bump version of `dkist-processing-common`

v1.1.8 (2023-04-10)
===================

Misc
----
- FITS header specification update to add spectral line keys.


v1.1.7 (2023-03-16)
===================

Misc
----
- FITS header specification update to add new keys and change some units.


v1.1.6 (2023-03-01)
===================

Misc
----

- Logging fix in the dkist-header-validator.


v1.1.5 (2023-02-22)
===================

Misc
----

- Move the header specification to revision H of SPEC-0122.


v1.1.4 (2023-02-17)
===================

Misc
----

- Update dkist-processing-common due to an Airflow upgrade.


v1.1.3 (2023-02-06)
===================

Features
--------

- Bump `dkist-processing-common` to allow inclusion of multiple proposal or experiment IDs in headers.


v1.1.2 (2023-02-02)
===================

Misc
----
- Bump FITS specification to revision G.


v1.1.1 (2023-01-31)
===================

Misc
----

- Bump `dkist-processing-common`

v1.1.0 (2022-12-15)
===================

Bugfixes
--------

- Don't re-compress already compressed data that are processed at the summit. This maintains the *exact* data received from the summit pipeline. (`#39 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/39>`__)


Misc
----

- Calculate the `DATE-END` keyword value at the instrument level. (`#33 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/33>`__)


v1.0.0 (2022-12-08)
===================

Misc
--------

- Moving the DKIST VBI pipelines into production.



v0.16.0 (2022-12-06)
====================

Features
--------

- If data include an aborted mosaic at the last DSPS repeat then drop that mosaic from the L1 dataset. (`#38 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/38>`__)


Bugfixes
--------

- Change how intermediate CALIBRATED frames are saved so that the L1 FRAMEVOL header key reports the correct on-disk size of the compressed data. (`#32 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/32>`__)
- The "summit_data_processing" workflow now produces *all* L1 quality metrics. (`#35 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/35>`__)
- Fix incorrect DINDEX3 values in L1 data. (`#37 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/37>`__)


Misc
----

- Use a Hann window to smooth out hard mosaic edges in the browse movie. Purely aesthetic. (`#36 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/36>`__)


v0.15.2 (2022-12-05)
====================

Bugfix
------

- Update dkist-processing-common to include movie headers in transfers.


v0.15.1 (2022-12-02)
====================

Misc
----

- Update dkist-processing-common to improve handling of Globus issues.



v0.15.0 (2022-11-15)
====================

Misc
----

- Update dkist-processing-common


v0.14.0 (2022-11-14)
====================

Bugfixes
--------

- Correctly organize data when DSPSREPS (DKIST008) includes instruments other than VBI (and is therefore very large), which may also cause DSPSNUM (DKIST009) to be offset from 1 by a large number. (`#30 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/30>`__)
- Bump `dkist-processing-common` to 1.1.0 to fix bug when running summit-calibrated workflow on float32 data.

Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#31 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/31>`__)
- Fixed markdown errors in CHANGELOG.rst headers. (`#31 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/31>`__)


v0.13.3 (2022-11-09)
====================

Misc
----

- Update dkist-processing-common to improve Globus event logging


v0.13.2 (2022-11-08)
====================

Misc
----

- Update dkist-processing-common to handle empty Globus event lists
- Bump scipy to 1.9.0 and fix an associated test.


v0.13.1 (2022-11-08)
====================

Misc
----

- Update dkist-processing-common to include Globus retries in transfer tasks


v0.13.0 (2022-11-02)
====================

Misc
----

- Upgraded dkist-processing-math and dkist-processing-common to production version (`#28 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/28>`__)


v0.12.1 (2022-11-02)
====================

Misc
--------

- Use updated dkist-processing-core version 1.1.2.  Task startup logging enhancements.


v0.12.0 (2022-10-26)
====================

Misc
----

- Update versions of dkist-processing-common and dkist-fits-specifications. (`#27 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/27>`__)


v0.11.4 (2022-10-26)
====================

Misc
----

- Update versions of dkist-processing-common and astropy. (`#26 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/26>`__)


v0.11.3 (2022-10-20)
====================

Misc
----

- Require python 3.10 and above. (`#25 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/25>`__)


v0.11.2 (2022-10-18)
====================

Misc
------

- Changing metrics included in quality reports


v0.11.1 (2022-10-12)
====================

Bugfix
------

- Moving to a new version of dkist-processing-common to fix a Globus bug


v0.11.0 (2022-10-11)
====================

Misc
----

- Upgrading to a new version of Airflow


v0.10.5 (2022-09-16)
====================

Misc
----

- Update tests for new input dataset document format from `*-common >= 0.24.0` (`#24 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/24>`__)


v0.10.4 (2022-09-14)
====================

Misc
----

- FITS spec was using incorrect types for some keys.

v0.10.3 (2022-09-12)
====================

Misc
----

- Updating the underlying FITS specification used.

v0.10.1 (2022-08-09)
====================

Misc
----

- Corrected workflow naming in docs.


v0.10.0 (2022-08-08)
====================

Misc
----

- Update minimum required version of `dkist-processing-core` due to breaking changes in workflow naming.


v0.9.3 (2022-08-03)
===================

Bugfixes
--------

- Use nearest neighbor interpolation to resize movie frames. This helps avoid weirdness if the maps are very small. (`#101 <https://bitbucket.org/dkistdc/dkist-processing-common/pull-requests/101>`__)


v0.9.2 (2022-07-21)
===================

Features
--------

- Bumped version of dkist-processing-common in setup.cfg. The change adds microsecond support to datetimes, prevents quiet file overwriting by default, and sets the default fits compression tile size to astropy defaults.

v0.9.1 (2022-06-27)
===================

Bugfixes
--------

- Bumped version of dkist-header-validator in setup.cfg.
  The change fixes a bug in handling multiple fits header commentary cards (HISTORY and COMMENT). (`#23 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/23>`__)


v0.9.0 (2022-06-20)
===================

Features
--------

- Change how L1 filenames are constructed.


v0.8.0 (2022-05-03)
===================

Bugfixes
--------

- Use new version of `dkist-processing-common` (0.18.0) to correct source for "fpa exposure time" keyword
- Bump version of `dkist` to allow for installation of "grogu" target

v0.7.0 (2022-04-28)
===================

Features
--------

- FITS specification now uses Rev. F of SPEC0122 as a base. (`#22 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/22>`__)


v0.6.4 (2022-04-22)
===================

Bugfixes
--------

- Change movie codec for better compatibility.


v0.6.1 (2022-04-06)
===================

Documentation
-------------

- Add changelog and towncrier machinery (`#21 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/21>`__)


Misc
----

- Update usage of `VbiQualityL0Metrics` to reflect changes in `dkist-processing-common >= 0.17.0`

v0.6.0 (2022-03-18)
===================

Features
--------

- Increase usefulness of APM logging for debugging pipeline performance (`#20 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/20>`__)


Documentation
-------------

- Big ol' update and pydocstyle-ization of docs (`#18 <https://bitbucket.org/dkistdc/dkist-processing-vbi/pull-requests/18>`__)
