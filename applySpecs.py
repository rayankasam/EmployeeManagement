import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('./defaults.env'))
MAX_PERM_ADDEMPLOYEE = int(os.getenv('MAX_PERM_ADDEMPLOYEE'))


def allowedAddEmployee(permission):
    return permission <= MAX_PERM_ADDEMPLOYEE
