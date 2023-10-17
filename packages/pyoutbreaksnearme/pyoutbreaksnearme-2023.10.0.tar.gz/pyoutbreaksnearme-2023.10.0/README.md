# 🚰 pyoutbreaksnearme: A Python3 API for Outbreaks Near Me

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`pyoutbreaksnearme` is a Python3, asyncio-based library for getting data from
[Outbreaks Near Me][outbreaksnearme].

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```bash
pip install pyoutbreaksnearme
```

# Python Versions

`pyoutbreaksnearme` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Usage

```python
import asyncio

from aiohttp import ClientSession

from pyoutbreaksnearme import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    client = await Client()

    # Get user-reported data for the location closest to a latitude/longitude:
    nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
        40.7152, -73.9877
    )

    # Get totals for user-reported data:
    user_totals_data = await client.user_data.async_get_totals()

    # Get CDC data for the location closest to a latitude/longitude:
    nearest_user_data = await client.cdc_data.async_get_nearest_by_coordinates(
        40.7152, -73.9877
    )


asyncio.run(main())
```

By default, the library creates a new connection to Outbreaks Near Me with each
coroutine. If you are calling a large number of coroutines (or merely want to squeeze
out every second of runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can
be used for connection pooling:

```python
import asyncio

from aiohttp import ClientSession

from pyoutbreaksnearme import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        # Create a Notion API client:
        client = await Client(session=session)

        # Get to work...


asyncio.run(main())
```

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov pyoutbreaksnearme tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[ci-badge]: https://github.com/bachya/pyoutbreaksnearme/workflows/CI/badge.svg
[ci]: https://github.com/bachya/pyoutbreaksnearme/actions
[codecov-badge]: https://codecov.io/gh/bachya/pyoutbreaksnearme/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/pyoutbreaksnearme
[contributors]: https://github.com/bachya/pyoutbreaksnearme/graphs/contributors
[fork]: https://github.com/bachya/pyoutbreaksnearme/fork
[issues]: https://github.com/bachya/pyoutbreaksnearme/issues
[license-badge]: https://img.shields.io/pypi/l/pyoutbreaksnearme.svg
[license]: https://github.com/bachya/pyoutbreaksnearme/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/4707fac476249d515511/maintainability
[maintainability]: https://codeclimate.com/github/bachya/pyoutbreaksnearme/maintainability
[new-issue]: https://github.com/bachya/pyoutbreaksnearme/issues/new
[new-issue]: https://github.com/bachya/pyoutbreaksnearme/issues/new
[outbreaksnearme]: https://outbreaksnearme.org
[pypi-badge]: https://img.shields.io/pypi/v/pyoutbreaksnearme.svg
[pypi]: https://pypi.python.org/pypi/pyoutbreaksnearme
[version-badge]: https://img.shields.io/pypi/pyversions/pyoutbreaksnearme.svg
[version]: https://pypi.python.org/pypi/pyoutbreaksnearme
