# football-calendar

Generate ical files from football fixtures from web.

## Development

After cloning the repository you are required to execute the following steps.

Install the package with *edit* mode and with the `dev` extra:
```bash
$ pip install -e .[dev]
```

Install `pre-commit` to run *isort*, *pylint*, *pydocstring*, *black* and *mypy* when committing new code.
```bash
$ pre-commit install
```

### act

Use [act](https://github.com/nektos/act) to test github actions locally:

```bash
act --reuse -j tests
```
