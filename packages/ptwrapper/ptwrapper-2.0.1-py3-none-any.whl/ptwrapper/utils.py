import json
import os
import shutil

def create_structure(parent_path, metakernel_path='input_mk.tm', ptr_content='input_ptr.ptx', step=5, no_power=False,
                     quaternions=False):
    """
    Creates the structure and contents for an OSVE session folder

    Args:
        parent_path (str): Path to parent folder
        metakernel_path (str): Path to an existing and valid metakernel
        ptr_content (str): Content of the PTR

    Return:
        (str) absolute path to scene file
    """
    session_json_filepath = os.path.join(
        os.path.dirname(__file__), "config", "session_file.json"
    )

    agm_config_filepath = os.path.join(
        os.path.dirname(__file__), "config/age", "cfg_agm_jui_jupiter.xml"
    )

    fixed_definitions_filepath = os.path.join(
        os.path.dirname(__file__), "config/age", "cfg_agm_jui_multibody_fixed_definitions.xml"
    )

    predefine_blocks_filepath = os.path.join(
        os.path.dirname(__file__), "config/age", "cfg_agm_jui_multibody_predefined_block.xml"
    )

    event_definitions_filepath = os.path.join(
        os.path.dirname(__file__), "config/age", "cfg_agm_jui_multibody_event_definitions.xml"
    )

    bit_rate_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "BRF_MAL_SGICD_2_1_300101_351005.brf"
    )

    eps_config_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "eps.cfg"
    )

    eps_events_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "events.juice.def"
    )

    sa_cells_count_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "phs_com_res_sa_cells_count.asc"
    )

    sa_cells_efficiency_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "RES_C50_SA_CELLS_EFFICIENCY_310101_351003.csv"
    )

    eps_units_filepath = os.path.join(
        os.path.dirname(__file__), "config/ise", "units.def"
    )

    itl_downlink_filepath = os.path.join(
        os.path.dirname(__file__), "input/itl", "downlink.itl"
    )

    itl_platform_filepath = os.path.join(
        os.path.dirname(__file__), "input/itl", "platform.itl"
    )

    itl_tbd_filepath = os.path.join(
        os.path.dirname(__file__), "input/itl", "TBD.itl"
    )

    itl_top_timelines_filepath = os.path.join(
        os.path.dirname(__file__), "input/itl", "TOP_timelines.itl"
    )

    edf_spc_link_kab_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "EDF_JUI_SPC_LINK_KAB.edf"
    )

    edf_spc_link_xb_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "EDF_JUI_SPC_LINK_XB.edf"
    )

    edf_spacecraft_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "juice__spacecraft.edf"
    )

    edf_spacecraft_platform_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "juice__spacecraft_platform.edf"
    )

    edf_spacecraft_ssmm_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "juice__spacecraft_ssmm.edf"
    )

    edf_tbd_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "TBD.edf"
    )

    edf_top_experiments_filepath = os.path.join(
        os.path.dirname(__file__), "input/edf", "TOP_experiments.edf"
    )

    evf_top_events_filepath = os.path.join(
        os.path.dirname(__file__), "input", "TOP_events.evf"
    )

    evf_downlink_filepath = os.path.join(
        os.path.dirname(__file__), "input", "downlink.evf"
    )

    with open(session_json_filepath, "r") as session_json_file:
        session_json = json.load(session_json_file)

    age_config_path = os.path.join(parent_path, "config/age")
    ise_config_path = os.path.join(parent_path, "config/ise")
    os.makedirs(age_config_path, exist_ok=True)
    os.makedirs(ise_config_path, exist_ok=True)

    # age
    shutil.copy(agm_config_filepath, age_config_path)
    shutil.copy(fixed_definitions_filepath, age_config_path)
    shutil.copy(predefine_blocks_filepath, age_config_path)
    shutil.copy(event_definitions_filepath, age_config_path)
    # ise
    shutil.copy(bit_rate_filepath, ise_config_path)
    shutil.copy(eps_config_filepath, ise_config_path)
    shutil.copy(eps_events_filepath, ise_config_path)
    shutil.copy(sa_cells_count_filepath, ise_config_path)
    shutil.copy(sa_cells_efficiency_filepath, ise_config_path)
    shutil.copy(eps_units_filepath, ise_config_path)


    file_list = session_json["sessionConfiguration"]["attitudeSimulationConfiguration"][
        "kernelsList"
    ]["fileList"]

    file_list.append(
        {
            "fileRelPath": os.path.basename(metakernel_path),
            "description": f"{os.path.basename(metakernel_path)}",
        }
    )

    if not quaternions:
        del session_json['sessionConfiguration']['outputFiles']['txtAttitudeFilePath']

    if no_power:
        del session_json['sessionConfiguration']['outputFiles']['powerFilePath']
        del session_json['sessionConfiguration']['outputFiles']['powerConfig']

    session_json['sessionConfiguration']['outputFiles']['ckConfig']['ckTimeStep'] = step

    kernel_path = os.path.join(parent_path, "kernel")
    os.makedirs(kernel_path, exist_ok=True)
    try:
        shutil.copy(metakernel_path, kernel_path)
    except BaseException:
        pass

    # Dump the ptr content
    ptr_folder_path = os.path.join(parent_path, "input")
    os.makedirs(ptr_folder_path, exist_ok=True)

    ptr_path = os.path.join(ptr_folder_path, "PTR_PT_V1.ptx")
    with open(ptr_path, encoding="utf-8", mode="w") as ptr_file:
        ptr_file.write(ptr_content)

    # Create the dummy ITL and EDF inputs
    itl_folder_path = os.path.join(parent_path, "input/itl")
    os.makedirs(itl_folder_path, exist_ok=True)

    shutil.copy(itl_downlink_filepath, itl_folder_path)
    shutil.copy(itl_platform_filepath, itl_folder_path)
    shutil.copy(itl_tbd_filepath, itl_folder_path)
    shutil.copy(itl_top_timelines_filepath, itl_folder_path)

    edf_folder_path = os.path.join(parent_path, "input/edf")
    os.makedirs(edf_folder_path, exist_ok=True)

    shutil.copy(edf_spc_link_kab_filepath, edf_folder_path)
    shutil.copy(edf_spc_link_xb_filepath, edf_folder_path)
    shutil.copy(edf_spacecraft_filepath, edf_folder_path)
    shutil.copy(edf_spacecraft_platform_filepath, edf_folder_path)
    shutil.copy(edf_spacecraft_ssmm_filepath, edf_folder_path)
    shutil.copy(edf_tbd_filepath, edf_folder_path)
    shutil.copy(edf_top_experiments_filepath, edf_folder_path)

    shutil.copy(evf_top_events_filepath, ptr_folder_path)
    shutil.copy(evf_downlink_filepath, ptr_folder_path)

    # Prepare the output folder
    output_path = os.path.join(parent_path, "output")
    os.makedirs(output_path, exist_ok=True)

    # Finally dump the session file
    session_file_path = os.path.abspath(os.path.join(parent_path, "session_file.json"))
    with open(session_file_path, "w") as session_json_file:
        json.dump(session_json, session_json_file, indent=2)

    return session_file_path


def remove_directory_if_empty(directory_path):
    """Remove a directory if empty

    Args:
        directory_path (str): absolute path to the directory

    """
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        return

    if len(os.listdir(directory_path)) == 0:
        os.rmdir(directory_path)
    else:
        print(f"Directory '{directory_path}' is not empty. Skipping removal.")
