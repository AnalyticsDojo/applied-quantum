import pandas as pd
import numpy as np
import csv
import logging
import subprocess
import yaml
import builder as bd
from pathlib import Path
import sitemap_construct as sc
base_path=Path('..')
config_path = base_path / 'config'
cf=bd.load_yaml_file(config_path / 'config.yml')
excel_file= config_path / cf['excel_file']
class_path= base_path / cf['class']
content_path = class_path / 'content'

print('====STARTING=====')
print('CALLING SCRIPT')
sc.notebooks_read()
