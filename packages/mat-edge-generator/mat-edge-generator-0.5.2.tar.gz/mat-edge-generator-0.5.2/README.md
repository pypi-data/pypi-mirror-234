# MAT Edge Generator

## Introduction

`matEdgeGenerator` is a tool designed for automatically generating Edge configurations suitable for the MAT software.

## Running the software

To run the software you need to import from *matEdgeGenerator.generator* the function *generateConfiguration*. This function accepts two arguments:
  - `config_path`: Path of the folder containing the input configurations.
  - `output_path`: Path of the folder in which the output configuration will be generated.

The folder in `config_path` must contains the following files:
  - `profiles`: Folder containing the factoryedge profiles used for the current configuration. Supported profiles are S7, OPC-UA and MODBUS. Each profile is a file .json.
  - `cloudConfig.json`: json file used to indicate the cloud configuration
  - `utils.json`: json file containining the utils function used in the BSW (if any)
  - `configBsw.json`: metaconfiguration used to create the BSW configuration file


## Getting an Example Configuration

To obtain an example configuration, you can execute the following script:

```python
from matEdgeGenerator.example import getExampleConfig

getExampleConfig('your_target_folder')
```

this will generate an example input configuration that can be used as a starting point.

### configBsw

This configuration file is a dictionary containing the a KEY-VALUE pair for each sub-machine in the asset configuration. If only a machine is present, only the KEY `line` must be used.
Below are the keys that make up the configuration for eache sub-machine (i.e. the sub-machine dictionary value). Note that whenever the term "variable" is mentioned, it refers to a BSW input. If this input does not come directly from the PLC (so is not present in one of the profile present in the `profile` folder) but needs to be calculated, the variable must be indicated as *utils.-variable name-*. All `utils` variables will be set up in a dedicated aspect that needs to be filled out manually.

The configuration is done for each sub-machine (including the line) and for each machine; it presents the following keys:

- **cycle** (Optional): Dictionary containing the following keys:
  - `id`: String variable used to understand cycle changes.
  - `aux_var`: List of auxiliary variables to include in the cycle history.

- **phase** (Optional): Dictionary of phases - possible only if the `cycle` dictionary exists:
  - `id`: String variable used to understand phase changes.
  - `aux_var`: List of auxiliary variables to include in the phase history.

- **state**: Dictionary containing the following keys:
  - `var`: String variable used for the state.
  - `faulty`: List of integers representing fault states.
  - `productive`: List of integers representing productive states.
  - `external`: List of integers representing external stop states.
  - `possible_vals`: List of all possible state integers.

- **mainCounter** (Optional): Dictionary containing:
  - `id`: String variable used for the incremental production counter.
  - `scale`: Number indicating possible data scaling.

- **badCounter** (Optional): Dictionary containing:
  - `id`: String variable used for the incremental waste counter.
  - `scale`: Number indicating possible data scaling.

- **scrapReasons** (Optional): List of dictionaries, each containing:
  - `id`: String variable used for the nth scrap reason counter.
  - `scale`: Number indicating possible data scaling.

- **goodCounter** (Optional): Dictionary containing:
  - `id`: String variable used for the incremental good pieces counter.
  - `scale`: Number indicating possible data scaling.

- **idealSpeed** (Optional): Dictionary containing:
  - `id`: String variable used to determine ideal speed.
  - `scale`: Number indicating possible data scaling.

- **aggr**: List of machine aggregates.

- **counters** (Optional): List of dictionaries, each containing:
  - `id`: String variable used for the nth generic counter.
  - `scale`: Number indicating possible data scaling.

- **consIntegral** (Optional): List of dictionaries, each containing:
  - `id`: String variable used for the consumable to integrate over time.
  - `scale`: Number indicating possible data scaling.

- **consSum** (Optional): List of dictionaries, each containing:
  - `id`: String variable used for the consumable to sum.
  - `scale`: Number indicating possible data scaling.

- **raws** (Optional): List of dictionaries, each containing:
  - `sampling`: Integer indicating the sampling time in milliseconds.
  - `sendToMqtt`: Boolean; if True, the raw aspect will be made available as an MQTT channel output.
  - `vars`: 
    - List of variables to acquire without modifications.
    - Dictionary with keys corresponding to the variables to be recorded and values equal to their data types (e.g., "var_01": "float").

- **warnings** (Optional): List of strings, containing variables used for warnings (boolean type data).

- **alarms** (Optional): List of strings, containing variables used for alarms (boolean type data).

- **breakdowns** (Optional): Dictionary containing:
  - `mode`: String indicating the breakdown search mode. Possible values are:
    - 'pre': Only alarms started before the breakdown can be the cause.
    - 'post': Only alarms started after the breakdown can be the cause.
    - 'prepost': Alarms started both before and after the breakdown can be the cause.
  - `params`: List of parameters to acquire at the beginning and end of breakdown.

- **buttons** (Optional): List of strings, containing variables used for buttons (boolean type data).

- **snapshot**: Boolean; if True, BSW output snapshots will be created for all RAW aspects.

- **recipe** (Optional): 
  - Option 1:
    - List of strings, containing variables used as recipe parameters.
  - Option 2:
    - Dictionary with keys corresponding to the variables to be recorded and values equal to their data types (e.g., "var_01": "float").

### cloudConfig

This configuration file is dedicated to the cloud configuration, contains the following keys:

- **active**: Boolean that says if the cloud configuration must be configured

- **platform**: Cloud platform used, possible values are 'azure' or 'mindsphere'

- **name**: Identifier of the asset in the edge configuration, up to the user.


### utils

`utils.json` contains the function used in the BSW in the  *utils* aspect. Object configured in this file will be automatically substituted inside the aspect when the BSW is configured