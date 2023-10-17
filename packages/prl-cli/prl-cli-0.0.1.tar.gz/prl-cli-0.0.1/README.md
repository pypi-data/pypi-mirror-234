
## Install Locally
```
cd legal-evaluator/cli
pip install -e .
```

## Run
The CLI is run as follows:
```
$ prl
```

Commands must be run from the pip environment the cli was installed in. Commands are split up into subcommand. Currently there are two subcommands: 
 - `prl suite`: relating to creating / updating tests and suites
 - `prl run`: relating to creating and querying runs and run results. 

 Example commands: 

Create a test suite from command line
```
prl suite create --interactive
```

Create a test suite from JSON file 
```
prl suite create ./example_suite.json
```

Start a new run:
```
prl run start
```

## How to Build

1. Increment version number in setup.cfg

2. Use `pip install .` to install the package's dependencies

3. Build the package with
`python -m build`
    - You may need to do `pip install build` if `build` is not installed in your computer

4. Then publish with
`python -m twine upload dist/*`
    - You may need to do
      `pip install twine` if `twine` is not installed in your computer

