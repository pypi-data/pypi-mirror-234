Changelog
=========

3.0.0 (07.10.2023)
------------------

 * **Attention**: Support for Unpoly 2 is dropped with this release.
 * Added support for Python 3.12.
 * `Unpoly.validate` returns a list of fields to validate now.
 * `Cache.clear` is replaced with `Cache.expire` to follow upstream changes.
 * Removed `reload_from_time`, standard `Last-Modified`/`If-Modified-Since`-headers should get used.

0.4.0 (31.03.2023)
------------------

 * Send `X-Up-Location` only if it difers from the request URL.
 * JSON encode `X-Up-Title` with Unpoly 3.
 * Internal: Use hatchling as build backend for reproducible builds.

0.3.0 (11.03.2023)
------------------

 * Removed support for Python 3.7 and added support for Python 3.11.

0.2.1 (02.01.2022)
------------------

 * Removed support for Python 3.6 and added explicit support for 3.10.
 * Internal: Replaced poetry with pdm.

0.2.0 (25.08.2021)
------------------

 * Fixed Python 3.6 compat.
 * Added documentation.

0.1.0 (24.08.2021)
------------------

 * Initial release. Test coverage exists, docs are still missing :)
