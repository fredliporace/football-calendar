# football-calendar

Generate ical calendars from football fixtures from web.

Currently supports scraping the fixtures from ESPN website.

May be used through CLI or deployed as a lambda function to AWS to support being imported to tools such as Google calendar.

## CLI

Clone the repository and:

```bash
pip install -e .[cli]
```

The main command is `footcal`:

```bash
Usage: footcal [OPTIONS] COMMAND [ARGS]...

  Create an icalendar from web fixtures.

  The calendar is dumped to stdout.

Options:
  -n, --name TEXT      Calendar name.  [default: Calendar]
  -t, --timezone TEXT  Calendar timezone.  [default: UTC]
  -l, --locale TEXT    Locale used to parse data such as month abbreviated
                       names.  [default: pt_BR]
  -u, --url TEXT       URL for fixtures.  [default: https://www.espn.com.br/fu
                       tebol/time/calendario/_/id/3445/fluminense; required]
  --help               Show this message and exit.

Commands:
  espn  Fixures from ESPN website.
```

Example using default options and ESPN site:

```bash
(fb) [liporace@localhost football-calendar]$ footcal espn
BEGIN:VCALENDAR
NAME:Calendar
BEGIN:VEVENT
SUMMARY:Fluminense x Botafogo
DTSTART:20240303T140000Z
DTEND:20240303T154500Z
END:VEVENT
END:VCALENDAR
```

## AWS lambda function

The application may be deployed to AWS using CDK2.

### CDK configuration

Requirements:
* node: Use [nvm](https://heynode.com/tutorial/install-nodejs-locally-nvm/) to make sure a supported node is being used, tested with 18.0.0
* AWS credentials configured

To install and check AWS CDK (tested with CDK 2.130.0):
```bash
$ npm install -g aws-cdk
$ cdk --version

# Check AWS account details:
$ aws sts get-caller-identity

# Bootstrap
$ cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

To install the aws packages required for deployment:

```bash
$ pip install -e .[aws]
```

### Deploy to lambda function

Create a `.env` file in `cdk/` with the lambda parameters. These specify the parser name (currently only `ESPNParser`) and the parameters to the parser constructor and `get_calendar` method. For instance:

```
FOOTCAL_PARSER="ESPNParser"
FOOTCAL_PARSER_CTOR_ARGS='{
        "timezone_id":"US/Eastern",
        "locale":"pt_BR"
}'
FOOTCAL_PARSER_GET_CALENDAR_ARGS='{
        "url":"https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense",
        "calendar_name":"Calendar"
}'
```

To deploy to lambda function:

```bash
cd cdk && cdk deploy
```

The output will be an URL that will output an updated calendar in ICAL format.

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
