import pandas as pd

from upload_access.connection import get_eng

def find_project(project: str):
    eng = get_eng()
    projects = pd.read_sql(f"select PROJECT from GB_PROJECT where PROJECT = '{project}'", eng)
    if len(projects) == 0:
        return None
    else:
        return str(projects['PROJECT'][0])