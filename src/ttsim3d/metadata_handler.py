from datetime import datetime
import yaml

leaveout = [
    "atom_positions_zyx", 
    "atom_identities", 
    "atom_b_factors", 
    "volume"
    ]
yaml_order = [
    "mrc_filepath",
    "pdb_filepath",
    "time_simulated",
    "volume_shape",
    "pixel_spacing",
    "center_atoms",
    "additional_b_factor",
    "b_factor_scaling",
    "remove_hydrogens",
    "simulator_config",
]

def sim_to_metadata_yaml(
        sim: "ttsim3d.models.Simulator", 
        mrc_filepath: str,
    ) -> None:
    """Writes the parameters of the simulator to a YAML file.
    
    Parameters
    ----------
    sim: Simulator
        The Simulator object for which the metadata file will be written to.
    mrc_filepath: str
        The filepath where the volume (and parameter YAML) will be written to.
        
    """
    result = {}
    for attr in sim:
        key, value = attr
        if key in leaveout:
            continue

        if key == "simulator_config":
            # Handle nested simulator_config
            result[key] = {k: v for k, v in value}
        else:
            result[key] = value
    result["time_simulated"] = datetime.now()
    result["pdb_filepath"] = str(result["pdb_filepath"])
    result["mrc_filepath"] = mrc_filepath
    result["volume_shape"] = list(result["volume_shape"])
    metadata_filepath = mrc_filepath.replace(".mrc", "_sim_parameters.yaml")
    ordered_result = {key: result[key] for key in yaml_order}
    with open(metadata_filepath, 'w') as stream:
        stream.write("# Simulator Parameters\n")
        yaml.dump(ordered_result, stream, sort_keys=False)
