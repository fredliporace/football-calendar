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

## Deploy to AWS

The application may be deployed to AWS using CDK.

### CDK configuration

Requirements:
* node: Use [nvm](https://heynode.com/tutorial/install-nodejs-locally-nvm/) to make sure a supported node is being used, tested with 16.16.0
* AWS credentials configured

To install and check AWS CDK:
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

To install the lambda function requirements:

```bash
pip install . --upgrade -t ./cdk/lambda/
```

To deploy to lambda function:

```bash
cd cdk && cdk deploy
```

To clean the cdk lambda directory:

```bash
cd cdk/lambda
rm -rf -v !("code.py")
```
