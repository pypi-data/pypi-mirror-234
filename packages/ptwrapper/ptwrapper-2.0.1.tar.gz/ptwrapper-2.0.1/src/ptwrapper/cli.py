"""PTR Command Line Interface module."""
import os
import shutil as sh
from argparse import ArgumentParser

from .utils import create_structure
from .utils import remove_directory_if_empty

from osve import osve

def execute(root_scenario_path, session_file_path):
    sim = osve.osve()
    sim.execute(root_scenario_path, session_file_path)

def cli(test=False):
    """CLI Resolve a PTR and generate a SPICE CK."""
    parser = ArgumentParser(description='Pointing Tool Wrapper (PTWrapper) simulates a PTR and generates the corresponding SPICE CK, resolved PTR, '
                                        'available Power, and quaternions dump file. PTWrapper uses OSVE to simulate the PTR.')

    # Exclusive group for session-file and the other parameters
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    exclusive_group.add_argument("-s", "--session-file", help="Path to the session file to run the simulation. "
                                 "If provided the other arguments are ignored.")

    parser.add_argument("-m", "--meta-kernel", help="Path to the meta-kernel file.")
    parser.add_argument("-p", "--ptr", help="Path to the PTR/PTX file input file.")
    parser.add_argument("-w", "--working-dir", default=os.getcwd(),
                        help="Path to the working directory. Default is the current directory.")
    parser.add_argument("-o", "--output-dir", help="Path to the output directory. Overwrites "
                        "default output file names. Default is the structure of the built-in session file.")
    parser.add_argument("-t", "--time-step", default=5,
                        help="Output CK file time step in seconds. Default is 5s.")
    parser.add_argument("-n", "--no-power", action="store_true", help="Indicate not to calculate available power. "
                        "Default is that the Available Power will be computed.")
    parser.add_argument("-q", "--quaternions", action="store_true", help="Indicate to calculate quaternions. "
                        "Default is that the quaternions will not be computed.")

    args = parser.parse_args()

    # Process the arguments and perform further actions
    if args.session_file:
        # Handle session-file exclusively
        # Do something with args.session_file
        session_file_path = args.session_file
        if not os.path.exists(session_file_path):
            raise ValueError("session-file does not exist")

        session_file_path = os.path.abspath(session_file_path)
        root_scenario_path = os.path.dirname(os.path.abspath(session_file_path))
    else:
        # Handle the other parameters exclusively
        if args.ptr is None:
            parser.error("PTR argument is missing")

        if args.meta_kernel is None:
            parser.error("META_KERNEL argument is missing")

        try:
            with open(args.ptr, 'r') as p:
                ptr_content = p.read()
        except FileNotFoundError:
            raise ValueError("PTR/PTX file not found")

        if not os.path.exists(args.meta_kernel):
            raise ValueError("meta-kernel does not exist")

        session_file_path = create_structure(args.working_dir, args.meta_kernel, ptr_content,
                                             step=int(args.time_step),
                                             no_power=args.no_power,
                                             quaternions=args.quaternions)
        root_scenario_path = os.path.dirname(session_file_path)

    print("ptwrapper session execution")

    execute(root_scenario_path, session_file_path)

    if args.output_dir:
        # Post-process the result
        fname = args.ptr.split(os.sep)[-1]
        if '.xml' in fname:
            fname = fname.split('.xml')[0]
        elif '.XML' in fname:
            fname = fname.split('.XML')[0]
        elif '.PTX' in fname:
            fname = fname.split('.PTX')[0]
        elif '.ptx' in fname:
            fname = fname.split('.ptx')[0]
        elif '.ptr' in fname:
            fname = fname.split('.ptr')[0]
        elif '.PTR' in fname:
            fname = fname.split('.PTR')[0]
        else:
            raise ValueError('Input PTR extension incorrect (not .xml, .XML ,.ptr, .PTR, .ptx or .PTX)')

        mkname = args.meta_kernel.split(os.sep)[-1]
        output_dir = os.path.abspath(args.output_dir)

        if args.quaternions:
            print(f'Renaming quaternions.csv to {fname}_quaternions.csv')
            sh.move(f'{root_scenario_path}/output/quaternions.csv', f'{output_dir}/{fname}_quaternions.csv')

        if not args.no_power:
            print(f'Renaming power.csv to {fname}_power.csv')
            sh.move(f'{root_scenario_path}/output/power.csv', f'{output_dir}/{fname}_power.csv')

        print(f'Renaming ptr_resolved.ptx to {fname}_resolved.ptx')
        sh.move(f'{root_scenario_path}/output/ptr_resolved.ptx', f'{output_dir}/{fname}_resolved.ptx')

        print(f'Renaming juice_sc_ptr.bc to {fname}.bc')
        sh.move(f'{root_scenario_path}/output/juice_sc_ptr.bc', f'{output_dir}/{fname}.bc')

        print(f'Renaming log.json to {fname}_log.json')
        sh.move(f'{root_scenario_path}/output/log.json', f'{output_dir}/{fname}_log.json')

        print('Cleaning up OSVE execution files and directories')
        os.remove(f'{root_scenario_path}/input/PTR_PT_V1.ptx')
        os.remove(f'{root_scenario_path}/input/downlink.evf')
        os.remove(f'{root_scenario_path}/input/TOP_events.evf')
        sh.rmtree(f'{root_scenario_path}/input/edf')
        sh.rmtree(f'{root_scenario_path}/input/itl')
        os.remove(f'{root_scenario_path}/session_file.json')
        sh.rmtree(f'{root_scenario_path}/config/age')
        sh.rmtree(f'{root_scenario_path}/config/ise')

        if args.meta_kernel != f'{root_scenario_path}/kernel/{mkname}':
            os.remove(f'{root_scenario_path}/kernel/{mkname}')

        for directory in ['kernel', 'output', 'input', 'config']:
            remove_directory_if_empty(f'{root_scenario_path}/{directory}')

    if test:
        return parser
