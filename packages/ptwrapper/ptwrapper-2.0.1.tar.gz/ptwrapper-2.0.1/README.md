# Pointing Tool Wrapper

A JUICE SOC [Pointing Tool](https://juicept.esac.esa.int/) wrapper (`PTwrapper`) for LINUX and MACOSX for use in a local computer.

Allows to simulate a Pointing Timeline Request (PTR) and to generate the corresponding SPICE CK, resolved PTR, 
available Power, and quaternions dump file.

`PTwrapper` is based on OSVE and mainly provides a shortcut to use the required functionalities and setup limited
to simulate PTRs. You can find more information on OSVE [here](https://juigitlab.esac.esa.int/core-system/uplink/phs/osve).


### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code.

Additional documentation is available at the [JUICE SOC Toolkit Help](https://juicesoc.esac.esa.int/panel/#/navigation/help).


## Installation

```shx
pip install ptwrapper
```

## Development and testing

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

Install the package and its dependencies:

```sh
poetry install
```

Then, after your edits, check that flake8 is happy:

```sh
poetry run flake8

```

and all the tests passed:

```sh
poetry run pytest -s
```

You can also run the tests with in the `tests` directory with:

```shell
python3 -m unittest
```


## Using the library

After installing the library can be used with the Python Shell or with its CLI.


### Python Shell

A basic test of the library for a PTR processing is provided. The sample creates in the working directory a structure 
folder to invoke the execution and dumps inside the OUTPUT folder the expected products (SPICE CK, resolved PTR, 
available Power, and quaternions CSV)

```
import os

from ptwrapper import execute
from ptwrapper import create_structure

ptr_content = """<prm>
   <body>
      <segment>
         <data>
            <timeline frame="SC">
               <block ref="OBS">
                  <startTime>2030-10-15T03:40:00</startTime>
                  <endTime>2030-10-15T04:15:00</endTime>
                  <attitude ref="track">
                     <boresight ref="SC_Zaxis"/>
                     <target ref="Jupiter"/>
                     <phaseAngle ref="powerOptimised">
                        <yDir>false</yDir>
                     </phaseAngle>
                     </attitude>
                     <metadata>
                        <comment>Track Power Optimised C3.0</comment>
                     </metadata>
               </block>
            </timeline>
         </data>
     </segment>
   </body>
</prm>
"""
mk_path = 'metakernel.tm'
session_file_path = create_structure('.', mk_path, ptr_content)
execute(os.path.dirname(session_file_path), session_file_path)
```

### Command line interface

The package has a CLI entry point:

```shell
ptwrapper -h

usage: ptwrapper [-h] [-s SESSION_FILE] [-m META_KERNEL] [-p PTR] [-w WORKING_DIR] [-o OUTPUT_DIR] [-t TIME_STEP] [-n] [-q]

Pointing Tool Wrapper (PTWrapper) simulates a PTR and generates the corresponding SPICE CK, resolved PTR, available Power, and quaternions dump file. PTWrapper uses OSVE to simulate the PTR.

options:
  -h, --help            show this help message and exit
  -s SESSION_FILE, --session-file SESSION_FILE
                        Path to the session file to run the simulation. If provided the other arguments are ignored.
  -m META_KERNEL, --meta-kernel META_KERNEL
                        Path to the meta-kernel file.
  -p PTR, --ptr PTR     Path to the PTR/PTX file with
  -w WORKING_DIR, --working-dir WORKING_DIR
                        Path to the working directory. Default is the current directory.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to the output directory. Overwrites default output file names. Default is the structure of the built-in session file.
  -t TIME_STEP, --time-step TIME_STEP
                        Output CK file time step in seconds. Default is 5s.
  -n, --no-power        Indicate not to calculate available power. Default is that the Available Power will be computed.
  -q, --quaternions     Indicate to calculate quaternions. Default is that the quaternions will not be computed.

```

You can either run the CLI using an OSVE configuration file (`SESSION_FILE`) or by specifying a 
number of inputs and assume the rest of parameters as provided by the default configuration file 
included in the package. 

In addition, if you do not specify an output directory (`OUTPUT_DIR`), the package will replicate
the canonical output directory and file structure and will also generate a `SESSION_FILE` that can
be reused. Contrarily, if you specify an `OUTPUT_DIR` the output will be simplified and provided in
that directory; additionally the output files will inherit the name of the input `PTR` file.

> **WARNING:** Remember that the input `META_KERNEL` needs to have an adequate 
> relative or absolute path for its `PATH_VALUES` variable value.

A couple of examples are provided hereunder. First specifying the output directory:

```shell
ptwrapper -m kernels/juice_mini_local.tm -p ptr_simphony.xml -o . 

ptwrapper session execution
AGM version:  9.3.0.p1
OSVE version: 1.6.0
[INFO]    <AGE>  Attitude Generation Module initialization started
[INFO]    <AGE>  AGE module setup started
[INFO]    <AGE>  AGE module setup successfully completed
[INFO]    <AGE>  Attitude Generation Module initialization completed
[INFO]    <AGE>  Loading Attitude Timeline
[INFO]    <AGE>  Checking Attitude Timeline
[INFO]    <AGE>  Initializing Attitude Timeline
[INFO]    <AGE>   TOTAL ENERGY for POINTING block from 2030-10-15T03:40:00Z to 2030-10-15T04:15:00Z
[INFO]    <AGE>   Attitude from actual PTR: 812.096753 Wh (812.096753 Wh)
[INFO]    <AGE>   Attitude from loaded CK:  812.096096 Wh (812.096096 Wh)
[INFO]    <PIF>  XML PTR file: "ptr_resolved.ptx" generated
[INFO]    <PIF>  Generating CK file with the following USER DEFINED parameters:
[INFO]    <PIF>  CK frame ID:  -28001
[INFO]    <PIF>  CK time step: 5 s
[INFO]    <AGE>  Writing Attitude Spice CK File: juice_sc_ptr.bc
[INFO]    <PIF>  CK file: "juice_sc_ptr.bc" generated
[INFO]    <AGE>  Writing Attitude Text File
[INFO]    <PIF>  POWER CSV file: "power.csv" generated
Renaming quaternions.csv to ptr_simphony_quaternions.csv
Renaming power.csv to ptr_simphony_power.csv
Renaming ptr_resolved.ptx to ptr_simphony_resolved.ptx
Renaming juice_sc_ptr.bc to ptr_simphony.bc
Cleaning up OSVE execution files and directories
```

This will generate the following output files.

```shell
.
|-- ptr_simphony.bc
|-- ptr_simphony.csv
|-- ptr_simphony.xml
|-- ptr_simphony_log.json
`-- ptr_simphony_resolved.ptx
```

The same run without specifying the `OUTPUT_DIRECTORY` yields the following directory structure:

```shell
.
|-- config
|   |-- age
|   |   |-- AGMConfig.xml
|   |   |-- CFG_AGM_JUI_MULTIBODY_EVENT_DEFINITIONS.xml
|   |   |-- CFG_AGM_JUI_MULTIBODY_FIXED_DEFINITIONS.xml
|   |   `-- CFG_AGM_JUI_MULTIBODY_PREDEFINED_BLOCK.xml
|   `-- ise
|       |-- BRF_MAL_SGICD_2_1_300101_351005.brf
|       |-- RES_C50_SA_CELLS_EFFICIENCY_310101_351003.csv
|       |-- eps.cfg
|       |-- events.juice.def
|       |-- phs_com_res_sa_cells_count.asc
|       `-- units.def
|-- kernel
|   `-- juice_mini_local.tm
|-- output
|   |-- juice_sc_ptr.bc
|   |-- power.csv
|   |-- ptr_resolved.ptx
|   |-- log.json
|   `-- quaternions.csv
|-- ptr
|   `-- PTR_PT_V1.ptx
`-- session_file.json
```