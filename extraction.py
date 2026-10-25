import pandas as pd
import yaml
from pathlib import Path

def read_yaml(path:str):
    with open(path, 'r', encoding='utf-8') as file:
        return pd.DataFrame(yaml.safe_load(file))
pd.read_yaml = read_yaml

def extract(path:str):
    ext = Path(path).suffix.lower()[1:]
    return getattr(pd, f"read_{ext}")(path)