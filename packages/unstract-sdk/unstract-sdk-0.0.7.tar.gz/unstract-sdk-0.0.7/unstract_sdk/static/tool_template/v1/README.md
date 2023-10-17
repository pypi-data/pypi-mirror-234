### TODO: Replace the contents of this file with the README for your tool

## Your Tool Name

Description of your tool

### Required environment variables

| Variable           | Description                                       |
| ------------------ | ------------------------------------------------- |
| `PLATFORM_HOST`    | The host in which the platform service is running |
| `PLATFORM_PORT`    | The port in which the service is listening        |
| `PLATFORM_API_KEY` | The API key for the platform                      |

_TODO: Add more variables here if required_

### Testing the tool locally

Setup a virtual environment and install the requirements:

```commandline
python -m venv venv
```

Once a virtual environment is created or if you already have created one, activate it:

```commandline
source venv/bin/activate
```

Install the requirements:

> If you want to use the local sdk, make sure you comment out the `unstract-sdk` line in the `requirements.txt` file.

```commandline
pip install -r requirements.txt
```

To use the local development version of the _unstract sdk_ install it from the local repository. Replace the path with
the path to your local repository:

```commandline
pip install ~/Devel/Github/pandora/sdks/.
```

Load the environment variables:

Make a copy of the `sample.env` file and name it `.env`. Fill in the required values.

```commandline
source .env
```

#### Run SPEC command

```commandline
python main.py --command SPEC
```

#### Run PROPERTIES command

```commandline
python main.py --command PROPERTIES
```

#### Run ICON command

```commandline
python main.py --command ICON
```

#### Run RUN command to index a document

#### TODO: Update the example below with the correct parameters

The format of the jsons required for settings and params can be found by running the SPEC command and the PROPERTIES
command respectively. Alternatively in you have access to the code base, it is located in the `config` folder
as `json_schema.json` and `properties.json`.

```commandline
python main.py \
    --command RUN \
    --params '{
        }' \
    --settings '{
        }' \
    --project-guid '00000000-0000-0000-0000-000000000000' \
    --log-level DEBUG

```

### Testing the tool from its docker image

To test the tool from its docker image, run the following command:

```commandline
docker run \
    -v /Users/arun/Devel/pandora_storage:/mnt/unstract/fs_input \
    unstract-tool-fileops:0.1 \
    python main.py \
    --command RUN \
    --params '{
        }' \
    --settings '{
        }' \
    --project-guid '00000000-0000-0000-0000-000000000000' \
    --log-level DEBUG

```

Notes for Docker:

* The `-v` option mounts the `/Users/arun/Devel/pandora_storage` folder on the host machine to
  the `/mnt/unstract/fs_input`. Replace the path with the path to your documents folder.
* When this command is called by the workflow execution subsystem, the path to the input files configured by the user in
  the UI is automatically mounted and loaded as a volumne in the `/mnt/unstract/fs_input` folder in the container.
