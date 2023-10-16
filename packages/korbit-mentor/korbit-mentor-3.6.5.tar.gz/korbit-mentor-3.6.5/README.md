# Korbit

Korbit mentor CLI will allow you to analyze any local files. See official documentation [here](https://docs.korbit.ai/cli/cli_quickstart)

## Installation

### Pip

To install Korbit, you can use pip:

```
pip install korbit-mentor
```

### Binary

#### Linux - MacOS

1. Automatically installation

```sh
curl https://mentor-resources.korbit.ai/cli/install.sh | bash
# or
sudo curl https://mentor-resources.korbit.ai/cli/install.sh | sudo bash
```

1. Linux and Macos x86

```sh
sudo wget https://mentor-resources.korbit.ai/cli/latest/korbit-x86_64 -O /usr/local/bin/korbit
sudo chmod +x /usr/local/bin/korbit
```

1. MacOS arm64

```sh
sudo wget https://mentor-resources.korbit.ai/cli/latest/korbit-aarch64 -O /usr/local/bin/korbit
sudo chmod +x /usr/local/bin/korbit
```

#### Windows

```sh
wget https://mentor-resources.korbit.ai/cli/latest/korbit.exe -O korbit.exe
```

## Usage

To use Korbit, simply run the `korbit` command followed by the path of the file or folder you want to zip. For example, to zip the current folder, you can run:

```
korbit scan example/subfolder
```

This will create a zip file containing all the files and folders in the current directory.

## Development

### Set environment variables

Fill the missing values.

```sh
cp .env.example .env
```

### Create env

```
conda env update -f environment.yml -n korbit-cli
```

### Run

#### Full scan

If you don't have the environment variables set you can use the login command and export at least `KORBIT_HOST` to use dev server for testing.

```sh
export KORBIT_HOST=https://oracle.korbit.ai:8000 # use this line only if you test on dev

python -m korbit/cli login

python -m korbit/cli scan example/subfolder


# Or
KORBIT_HOST=https://localhost:8000 python -m korbit/cli scan example/subfolder
```

##### PR Scan

To utilize this feature, please ensure the following conditions are met:

- You are currently operating within a Git repository.
- The branch you intend to compare against has been fetched and is available in your environment.
- You are not on a detached HEAD state, as this feature requires an active branch context.

By meeting these conditions, you will be able to analyze only the files that you have modified in your current branch, specifically when compared to the target branch of your choice. This allows for a focused and efficient analysis of the changes made within your development workflow.

```sh
export KORBIT_HOST=https://oracle.korbit.ai:8000 # use this line only if you test on dev
python -m korbit/cli login


python -m korbit/cli scan-pr /path/to/repository master
python -m korbit/cli scan-pr path/to/repository master
python -m korbit/cli scan-pr # Default use current directory (`.`), as the repository and `master` as the base branch
```

It will take your current active branch and find the diff files. Using this it will be requesting a review only on those files.
_Note: You will be able to use all the same options as the `korbit scan` explained bellow._

#### Output

We introduce the ability to run a scan headless, meaning that there will be no output in the terminal. But in the following default path:

```sh
# In the working directory where the korbit scan command has been executed.
cat .korbit/scan.log
```

If Korbit AI mentor find issues the command will exit with a specific code number (see `--headless` option documentation).

```sh
korbit scan --help
```

This `korbit scan --headless` flag option will be used mainly in CI/CD pipelines, to automatically stop it.
Along with the --headless command you can specify certain thresholds for only 2 metrics at the moment:

1. confidence (scale 1-10): represents how confident Korbit AI Mentor is that a particular issue is real. A higher confidence score indicates a greater level of certainty that the identified issue is valid and requires attention.
1. priority (scale 1-10): represents the level of importance or urgency assigned by Korbit AI Mentor to a particular issue. A higher priority score indicates a greater sense of urgency and the need for immediate attention to address the identified issue.

```sh
korbit scan --headless
```

**Note**: You can use the `--thresholds-*` even if the scan isn't in headless mode, this will filter the issue found and display only the one that matters for you.

#### Progress view

After you start to run a `korbit scan` command and that our system accepted the request (might take some time regarding load on our server), you will see in your terminal the progress of the scan. Each files will be updated in real time with their status.

```sh
Analysis in progress (1/1)
├── afile.js ⏳
└── afile.py ✅
Analyzing files (2)... ━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━  50% -:--:--
```

#### Result

At the end when every file will be analyzed you will see in your terminal different tables containing the issues' descriptions and their placement in the given file. Along that will see the priority and confidence about that issue.

```sh
                                         Category: Critical Errors
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Error Description                                  ┃ File Path                  ┃ Confidence ┃ Priority ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ There is an error on the line X, because...        │ folder/afile.js            │ 10         │ 9        │
└────────────────────────────────────────────────────┴────────────────────────────┴────────────┴──────────┘
```

#### Debug

You can add the flag --verbose to the command in order to see the details of the exception (logging.exception).

```sh
korbit scan example --verbose

# or
korbit scan-pr example --verbose
```

### Troubleshooting

We are using Python=3.11.3 because Python=3.11.4 and pyinstaller are causing a crash on execution of the script.

https://stackoverflow.com/a/76731974

<details>
<summary>Exception on python==3.11.4</summary>

```
❯ dist/korbit example/subfolder
[8650] Module object for pyimod02_importers is NULL!
Traceback (most recent call last):
  File "PyInstaller/loader/pyimod02_importers.py", line 22, in <module>
  File "pathlib.py", line 14, in <module>
  File "urllib/parse.py", line 40, in <module>
ModuleNotFoundError: No module named 'ipaddress'
Traceback (most recent call last):
  File "PyInstaller/loader/pyiboot01_bootstrap.py", line 17, in <module>
ModuleNotFoundError: No module named 'pyimod02_importers'
[8650] Failed to execute script 'pyiboot01_bootstrap' due to unhandled exception!
```

</details>

## Building

### Linux and MacOS (x86)

You can just run the github action for that.

### MacOS (arm64)

You will need to have an arm64 computer and manually run the command:

```
conda activate korbit-cli
make build-cli
```

### Windows

You just ran the github action. You want to make sure the korbit.exe file is correctly signed by Korbit Technologies Inc afterward. The github action should take care of it.

## AutoUpdate

In order to publish a new version of the CLI you will need to upload a version.txt to our s3 buckets:

### Dev (publish-dev-version.yaml)

Using the github action, you will be able to publish the current master branch version number to the dev s3 bucket.

### Prod (publish-version.yaml)

Will release to production the new version number. All our client will need to update to that exact version. So the binary and Pypi release should have been done beforehand.

### Backend endpoints

We have 2 endpoints in the backend that the CLI use intensively:

1. `/cli`: allow us to know if a new version is required.
1. `/cli/telemetry`: allow us to log stuff on the server.

## Contributing

Contributions are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue or submit a pull request.

## Contact

If you have any questions or need further assistance, feel free to reach out to us at [support@korbit.ai](mailto:support@korbit.ai).

You can also open new Issue tickets on this repository.
