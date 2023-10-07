import os
import pathlib
from dotenv import load_dotenv

stage = os.environ.get('STAGE', None)
if stage == 'dev':
    load_dotenv(f'{pathlib.Path(__file__).parent.resolve()}/.env.develop')
else:    
    load_dotenv(f'{pathlib.Path(__file__).parent.resolve()}/.env')

from . import client

from .api import (
    set_client_ip,
    get_client_ip,
    init,
    finalize,
    get_run_name,
    log_param,
    log_params,
    log_metric,
    log_metrics,
    log_artifact,
    log_dataset_metadata,
    log_model_metadata,
    )

__all__ = [
    "set_client_ip",
    "get_client_ip",
    "init",
    "finalize",
    "get_run_name",
    "log_param",
    "log_params",
    "log_metric",
    "log_metrics",
    "log_artifact",
    "log_dataset_metadata",
    "log_model_metadata"
    ]
