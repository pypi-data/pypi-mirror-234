v0.0.13 (2023-10-11)
====================

Misc
----

- Use latest version of dkist-processing-common (4.1.4) which adapts to the new metadata-store-api. (`#68 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/68>`__)


v0.0.12 (2023-10-06)
====================

Misc
----

- Identify ramps with only one frame as invalid and do not linearize them. (`#62 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/62>`__)


v0.0.11 (2023-10-05)
====================

Features
--------

- Removes casts and flips used when loading parameter files. The files are now changed to be in the format we want. (`#68 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/68>`__)


v0.0.10 (2023-09-29)
====================

Misc
----

- Remove and edit selected APM spans to reduce load on aggregating span data. (`#64 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/64>`__)


v0.0.9 (2023-09-29)
===================

Features
--------

- Removes all references to the FitsDataMixin and its methods, which are deprecated. Uses the new self.read() and self.write() methods with encoder and decoder support. (`#63 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/63>`__)


Misc
----

- Update pillow to address security vulnerability. (`#66 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/66>`__)


v0.0.8 (2023-09-21)
===================

Misc
----

- Update dkist-fits-specifications to conform to Revision I of SPEC-0122.


v0.0.7 (2023-09-11)
===================

Bugfixes
--------

- Fixes error in intermediate file mixin log statement. (`#57 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/57>`__)


Misc
----

- Refactor to reduce complexity and hidden mixin->mixin dependency. (`#55 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/55>`__)


v0.0.6 (2023-09-08)
===================

Misc
----

- Use the latest version of dkist-processing-common (4.1.2) to allow the Linearity Correction task to be run on a higher memory worker. (`#60 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/60>`__)


v0.0.5 (2023-09-06)
===================

Misc
----

- Refactor linearity correction to improve memory usage. (`#59 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/59>`__)


v0.0.4 (2023-09-06)
===================

Misc
----

- Update to version 4.1.1 of dkist-processing-common which primarily adds logging and scratch file name uniqueness. (`#58 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/58>`__)


v0.0.3 (2023-08-31)
===================

Misc
----

- Remove parallel computations from the linearity correction task. (`#56 <https://bitbucket.org/dkistdc/dkist-processing-cryonirsp/pull-requests/56>`__)


v0.0.2 (2023-08-25)
===================

Misc
----

- Change workflow names in documentation builds.


v0.0.1 (2023-08-25)
===================

Misc
----

- Initial release of pipeline for science review
