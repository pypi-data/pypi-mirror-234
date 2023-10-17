

=========
Changelog
=========




.. towncrier release notes start

7.0.0 (2023-10-11)
==================

Deprecations and Removals
-------------------------

- Use ``build`` instead of deprecated ``pep517`` package.

- Removed dependency on py package.
  Plugins which expect py.path.local need to be adjusted to work with pathlib.Path.

- Dropped support for Python <= 3.6.



Other Changes
-------------

- .. note::
      Potentially breaking fix #939: devpi-common 4.x now has custom legacy version parsing (non PEP 440) after packaging >= 22.0 removed support. This might affect commands like ``devpi remove`` if used with version ranges. Legacy versions were always and still are sorted before PEP 440 compliant versions, but the ordering between legacy versions might be affected.

- Fix #946: output ``name==version`` instead of ``name-version`` for ``devpi list -v``.


6.0.6 (2023-10-11)
==================

Bug Fixes
---------

- Fix #997: Directly use ``BDist``, ``SDist`` and ``Wheel`` from ``pkginfo`` based on file extension instead of ``get_metadata``, as the latter does auto-detection on content which fails in some cases.

- Fix #1002: cleanup ``build`` directory before running Sphinx to prevent build artifacts from being added to documentation zip.


6.0.5 (2023-07-02)
==================

Bug Fixes
---------

- Remember URL when ``devpi use`` causes a 403, so one can use ``devpi login`` afterwards.

- Fix #978: Quote username and password when adding to URL.

- Fix #980: Remove long deprecated backward compatibility for old pluggy versions to fix error with pluggy 1.1.0.


6.0.4 (2023-04-13)
==================

Bug Fixes
---------

- Fix precedence of URL from command line over DEVPI_INDEX environment variable for ``devpi use``.

- Fix relative DEVPI_INDEX environment variable with user and index causing an invalid URL in some cases.

- Fix persistence of username when DEVPI_INDEX environment variable is used with ``devpi login``.

- Fix precedence of ``--sdist`` and ``--wheel`` over ``formats`` setting from setup.cfg ``[devpi:upload]`` section.


6.0.3 (2023-02-20)
==================

Bug Fixes
---------

- Fix #919: Retry 3 times and wait a moment on PermissionError during file removal to fix race condition after running tox.

- Restore ability to build docs if project uses separate build and source directories for documentation.

- Fix for changes in pypitoken 6.x.

