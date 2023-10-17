import json
import os
import shutil

import click
import torch
from tqdm import tqdm


@click.command()
@click.option("sharding_factor","--sharding_factor", default=3, required=False)
@click.option("source_file","--source_file",required=True,prompt="Input weight file path", type=click.Path(exists=True))
@click.option("target_dir","--target_dir",required=True, prompt="Output directory", type=click.Path())
def main(sharding_factor, source_file,target_dir):
    os.makedirs(target_dir, exist_ok=True)

    state_dict = torch.load(source_file, map_location='cpu')
    index_dict = {
        "metadata": {
            "total_size": 0
        },
        "weight_map": {}
    }

    state_keys = list(state_dict.keys())
    total_keys = []
    for i in tqdm(range(sharding_factor)):
        file_name = f"pytorch_model_{i:05}-of-{sharding_factor-1:05}.bin"
        sharded_state_dict = {}
        for key in state_keys[i::sharding_factor]:
            param = state_dict[key]
            index_dict["metadata"]["total_size"] += sum([param.nelement()*param.element_size()])
            index_dict["weight_map"][key] = file_name 
            sharded_state_dict[key] = param
            total_keys.append(key)

        target_file =os.path.join(target_dir, file_name) 
        torch.save(sharded_state_dict,target_file)

    if sorted(total_keys) != sorted(state_keys):
        raise ValueError()

    target_index_file = os.path.join(target_dir, "pytorch_model.bin.index.json")
    with open(target_index_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(index_dict, indent=2, sort_keys=True) + "\n")

if __name__ == '__main__':
    main()






