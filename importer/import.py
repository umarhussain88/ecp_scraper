from typing import Optional
import pandas as pd 
from pathlib import Path 
import json 


def create_tabular_files(src_path : Optional[str] = 'output') -> None:

    files = Path(__file__).parent.parent.joinpath(src_path).glob('*.json')

    for file in files:
        with open(file,'r') as f:
            j = json.load(f)
            df = pd.json_normalize(j)
            df['src'] = file
            df['extractiondate'] = pd.to_datetime(file.stem.rstrip('_parts'),format='%Y-%m-%dT%H-%M-%S')
            trg_path = Path(file.parent).joinpath(f"{file.stem}.csv")
            df.to_csv(trg_path,index=False)
            # remove src json file, no need for this anymore.
            file.unlink() 

if __name__ == '__main__':
    create_tabular_files()



