import os
import pkg_resources
import __main__
import signal

from typing import Any, Dict, Optional
from datetime import datetime

from .binding.args_bind import ArgBind
from .binding.yaml_bind import YamlBind
from .entities.run import Run
from .store import ClientStore, RunStore
from .utils import get_ip
from .job.background_task import BackGroundTask
from . import client


__HAIQV_UPLOAD_INTERVAL = 2
__HAIQV_STD_LOG_FILE = 'output_'
__active_run = None


class ActiveRun(Run):

    def __init__(self, run=None):
        if run is not None:
            Run.__init__(self, run.info)

    def __enter__(self):
        return self

    def __del__(self):
        finalize()

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = 'FINISHED' if exc_type is None else 'FAILED'
        finalize(status)


def signal_handler(signum, frame):
    if signum == signal.SIGINT:
        finalize("KILLED")
        exit(1)

    if signum == signal.SIGTERM:
        finalize("FINISHED")
        exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def _get_current_active_run() -> Run:

    assert RunStore.status() and RunStore.id() is not None, 'has not active runs, please run init() command first'
    return RunStore()


def set_client_ip(client_ip: str):
    ClientStore(client_ip)


def get_client_ip():
    if ClientStore.ip() is not None:
        return ClientStore.ip()
    else:
        return get_ip()


def get_run_name() -> str:
    assert RunStore.status() and RunStore.id() is not None, 'has not active runs, please run init() command first'
    return RunStore().name


def init(
        experiment_name: str,
        run_name: Optional[str] = None,
        auto_track_args: Optional[bool] = False,
        enable_output_upload: Optional[bool] = False
) -> ActiveRun:
    assert experiment_name, 'init need experiment name'

    client_ip = ClientStore.ip()
    if client_ip is None:
        client_ip = get_ip()
    assert client_ip, 'has not valid IP. You can specify IP address using set_client_ip() command before init()'

    if RunStore.status():
        RunStore.flush()

    if run_name:
        run_name_final = f"{run_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    else:
        run_name_final = f"run-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    run_info = client.create_run(
        exp_name=experiment_name,
        run_name=run_name_final,
        client_ip=client_ip
    )

    if not RunStore.status():
        RunStore(run_info)

    running_file = __main__.__file__
    if os.path.getsize(running_file) > 0:
        log_artifact(running_file, "code")

    dists = [str(d).replace(" ", "==") for d in pkg_resources.working_set]
    client.log_requirements(run_info.id, '\n'.join(dists), "requirements.txt")

    if auto_track_args:
        ArgBind.patch_argparse(log_params)
        YamlBind.patch_load(log_params)

    if enable_output_upload:
        bg = BackGroundTask()
        std_log_filename = f'{__HAIQV_STD_LOG_FILE}_{run_name_final}.log'
        bg.set_std_log_config(std_log_filename, __HAIQV_UPLOAD_INTERVAL, log_artifact)
        bg.start_std_log()

    run = ActiveRun()

    global __active_run
    __active_run = run

    return run


def finalize(status: str = "FINISHED") -> None:
    bg = BackGroundTask()
    if bg is not None:
        bg.end_std_log()
    if RunStore.status():
        client.update_run(
            run_id=_get_current_active_run().id,
            status=status
        )
        RunStore.flush()


def log_param(key: str, value: Any) -> None:
    run_id = _get_current_active_run().id
    client.log_param(run_id=run_id, key=key, value=value)


def log_params(params: Dict[str, Any]) -> None:
    run_id = _get_current_active_run().id
    data = [{key: str(value)} for key, value in params.items()]
    client.log_params(run_id=run_id, data=data)


def log_metric(key: str, value: float, step: int, subset: Optional[str] = None) -> None:
    run_id = _get_current_active_run().id
    client.log_metric(run_id=run_id, key=key, value=value, step=step, subset=subset)


def log_metrics(metrics: Dict[str, float], step: int, subset: Optional[str] = None) -> None:
    assert sum(['/' in k for k in metrics.keys()]) == 0, 'not allow (/) in key'
    run_id = _get_current_active_run().id
    data = [{'key': key, 'value': str(value), 'step': step, 'subset': subset} for key, value in metrics.items()]
    client.log_metrics(run_id=run_id, data=data)


def log_artifact(local_file: str, artifact_path: Optional[str] = None) -> None:
    run_id = _get_current_active_run().id
    client.log_artifact(run_id=run_id, local_file=local_file, artifact_path=f'{artifact_path}')


def log_dataset_metadata(data_nm: str, path: str, desc: str = None):
    run_id = _get_current_active_run().id
    client.log_dataset_metadata(
        run_id=run_id,
        data_nm=data_nm,
        path=path,
        desc=desc
    )


def log_model_metadata(model_nm: str, model_path: str, step: int, metric: Optional[dict] = None):
    run_id = _get_current_active_run().id
    client.log_model_metadata(
        run_id=run_id,
        model_nm=model_nm,
        model_path=model_path,
        step=step,
        metric=metric
    )
