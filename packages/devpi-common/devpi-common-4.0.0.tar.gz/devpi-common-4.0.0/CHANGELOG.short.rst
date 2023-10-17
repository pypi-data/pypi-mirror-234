

=========
Changelog
=========




.. towncrier release notes start

4.0.0 (2023-10-11)
==================

Deprecations and Removals
-------------------------

- Removed ``HTMLPage`` class originally vendored from pip.

- Dropped support for Python <= 3.6.



Features
--------

- Add ``chdir`` context handler in devpi_common.contextlib. Starting with Python 3.11 the original from ``contextlib`` is used.

- Hide username from URL representation.

- Added stripped down TerminalWriter from ``py`` library which only supports coloring.



Bug Fixes
---------

- Fix #939: custom legacy version parsing (non PEP 440) after packaging >= 22.0 removed support.


3.7.2 (2023-01-24)
==================





Bug Fixes
---------

- Fix #928: correct default for pre-release matching after switching from ``pkg_resources`` to ``packaging``.

- Fix #949: correct parsing of wheel tags for Python 3.10 and above.


3.7.1 (2022-12-16)
==================

Bug Fixes
---------

- Fix #939: pin packaging to <22 as it removed the deprecated LegacyVersion.


3.7.0 (2022-08-16)
==================

Features
--------

- Add ``hash_type`` and ``fragment`` attributes to URL class.

- Replace ``pkg_resources`` usage with ``packaging``.


Bug Fixes
---------

- Fix #895: return content of data-yanked.

- Fixed some cases where name and version weren't split off correctly from filename.


3.6.0 (2020-09-13)
==================

Features
--------

- Hide password from URL representation.

- Allow replacement of individual netloc parts with URL.replace method.

