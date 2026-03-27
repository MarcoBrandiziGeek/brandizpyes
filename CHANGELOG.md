# Changelog

*This file was updated on 2026-03-27. Please keep this note up to date.*

## 2.2.0 (2026-03-27)
* `async_reader_helper()` added.


## 2.1.0 (2026-03-12)
* `dump_output()` and `reader_helper()` now support iterables as output sinks and input sources, respectively.


## 2.0.0 (2026-03-12)
* Progress loggers added
* `brandizpyes.threading` added (`ReadWriteLock`).
* `brandizpyes.ioutils` renamed to `brandizpyes.io`.


## 1.2.0 (2026-03-06)
* `reader_helper()` added.
* `dump_output()` checks its arguments better.


## 1.1.7 (2026-02-27)
It's identical to 1.1.5, published by mistake.

## 1.1.6 (2026-02-27)
It's identical to 1.1.5, published by mistake.


## 1.1.5 (2026-02-27)
* Migrated from personal GitHub repo to my own organisation, MarcoBrandiziGeek.


## 1.1.4 (2026-02-23)
* Python version requirement downgraded to 3.11, to accomodate existing projects.


## 1.1.3 (2026-02-14)
* Python version requirement downgraded to 3.13, to accomodate existing projects.
* logging utils: issue with default log file path [fixed](https://github.com/marco-brandizi/brandizpyes/issues/57c36787).


## 1.1.2 (2026-01-16)
* `src/resources/` moved back to package dirs, since it's the only sane way to have them included in the distro files.


## 1.1.1
* Package files moved to `resources/` directories.


## 1.1.0 (2025-12-04)
* Logging via our own logging configure added to our own pytest runs
* [ioutils](src/brandizpyes/ioutils.py) added
* Sphinx docs removed (for the moment, we don't use it in this small project)


## 1.0.1 (2025-11-27)
* Test code improvements (refactoring, comments, assertpy )
* Documentation improvements


## 1.0.0 (2025-11-25)
* First release to PyPI and github
* Dependencies upgraded


## 0.1.0 (2025-09-23)
* First release (in the test registry)
* `logging` module added
