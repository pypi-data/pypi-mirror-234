# Fediverse Pasture

This python package contains tools to test Fediverse applications. This
package uses [bovine](https://bovine.readthedocs.io/en/latest/) for a lot
of the Fediverse related logic.

## Development

Install the necessary dependencies via

```bash
poetry install --with test,doc,dev
```

To lint and check code formatting run

```bash
poetry run ruff check .
```

To test the code run

```bash
poetry run pytest
```

To build the documentation run

```bash
poetry shell
cd docs
make html
```

## Funding

This code was created as part of [Fediverse Test Framework](https://nlnet.nl/project/FediverseTestFramework/).

A project funded through the [NGI0 Core](https://nlnet.nl/core) Fund,
a fund established by [NLnet](https://nlnet.nl/) with financial support from
the European Commission's [Next Generation Internet](https://ngi.eu/) programme,
under the aegis of DG Communications Networks, Content and Technology
under grant agreement No 101092990.

## Todo

In conclusion:

    poetry install --with dev, test should be included in the Installation instructions
    There are errors when running pytest
    After successfully building the dist files, they either need to be copied or a symlink could be established between python_fediverse_pasture and fediverse_pasture/dockerfiles/pasture/
    After the build succeeded, a cd to the fediverse_pasture directory should be added before running the docker-compose commands.
    The command you provided here should replace the first docker compose command in the current instructions

With those changes, the fediverse pasture ran for me.
