import os
import json
import yaml
import tempfile
import requests
import posixpath
import contextlib

from typing import Dict, Optional, Any

from .entities import experiment, run
from .error.value_error import HaiqvValueError
from .utils.common import get_millis, key_subset_split
from .utils.files import guess_mime_type


# Run
def create_run(exp_name: str, run_name: str, client_ip: str) -> run.Run:
    data = {
        'exp_name': exp_name,
        'run_name': run_name,
        'client_ip': client_ip
    }

    run_info = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})

    if run_info.status_code == 200:
        return run.Run(id=run_info.json()['run_id'], name=run_name)
    else:
        raise HaiqvValueError(run_info.text)


def update_run(
        run_id: str,
        status: Optional[str] = None
) -> None:
    data = {
        'run_id': run_id
    }

    if status:
        data['status'] = status

    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run/update',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})

    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Parameter
def log_param(run_id: str, key: str, value: Any) -> None:
    data = [
        {
            key: str(value)
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_params(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Metric
def log_metric(run_id: str, key: str, value: float, step: int, subset: Optional[str] = None) -> None:
    data = [
        {
            'key': key,
            'value': str(value),
            'step': step,
            'subset': subset
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_metrics(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Artifact
def log_artifact(run_id: str, local_file: str, artifact_path: str) -> None:
    filename = os.path.basename(local_file)
    mime = guess_mime_type(filename)
    with open(local_file, 'rb') as f:
        res = requests.post(
            f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run/set-artifacts?run_id={run_id}&artifact_path={artifact_path}',
            files={'local_file': (filename, f, mime)}
        )
        if res.status_code != 200:
            raise HaiqvValueError(res)


# Requirements
def log_requirements(run_id: str, text: str, requirement_file: str) -> None:
    with _log_artifact_helper(run_id, requirement_file) as tmp_path:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(text)


# metadata
def log_dataset_metadata(run_id: str, data_nm: str, path: str, desc: str = None):
    # TBD
    pass


def log_model_metadata(run_id: str, model_nm: str, model_path: str, step: int, metric: Optional[dict] = None):
    # TBD
    pass


@contextlib.contextmanager
def _log_artifact_helper(run_id, artifact_file):
    norm_path = posixpath.normpath(artifact_file)
    filename = posixpath.basename(norm_path)
    artifact_dir = posixpath.dirname(norm_path)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, filename)
        yield tmp_path
        log_artifact(run_id, tmp_path, artifact_dir)

###########################################################################################################
# def _get_run(run_id: str, client_ip=None) -> run.Run:
#     run_item = requests.get(
#         f'{os.environ.get("_HAIQV_BASE_URL")}/get-run-via-run-id',
#         params={'run_id': run_id, 'client_ip': client_ip}
#     )
#     if run_item.status_code == 200:
#         return run.Run(info=run_item.json()['run']['info'])
#     else:
#         raise HaiqvValueError(run_item.json())


# @contextlib.contextmanager
# def _log_artifact_helper(run_id, artifact_file):
#     norm_path = posixpath.normpath(artifact_file)
#     filename = posixpath.basename(norm_path)
#     artifact_dir = posixpath.dirname(norm_path)
#     # artifact_dir = None if artifact_dir == "" else artifact_dir

#     with tempfile.TemporaryDirectory() as tmp_dir:
#         tmp_path = os.path.join(tmp_dir, filename)
#         yield tmp_path
#         log_artifact(run_id, tmp_path, artifact_dir)


# def log_text(run_id: str, text: str, artifact_file: str) -> None:
#     with _log_artifact_helper(run_id, artifact_file) as tmp_path:
#         with open(tmp_path, "w", encoding="utf-8") as f:
#             f.write(text)


# def log_dict(run_id: str, dictionary: Any, artifact_file: str) -> None:
#     extension = os.path.splitext(artifact_file)[1]

#     with _log_artifact_helper(run_id, artifact_file) as tmp_path:
#         with open(tmp_path, "w") as f:
#             # Specify `indent` to prettify the output
#             if extension in [".yml", ".yaml"]:
#                 yaml.dump(dictionary, f, indent=2, default_flow_style=False)
#             else:
#                 json.dump(dictionary, f, indent=2)


# def log_model_metadata(
#         run_id: str,
#         model_nm: str,
#         model_path: str,
#         step: int,
#         metric: Optional[dict] = None,
#         tags: Optional[dict] = None,
#         client_ip=None) -> None:

#     runs = _get_run(run_id, client_ip)

#     model_tags = dict()
#     model_tags['model_path'] = os.path.abspath(model_path)
#     model_tags['step'] = step

#     if metric is None:
#         # 1. Step에 맞춰 Metric 가져오기
#         # model_tags['metric'] = dict()
#         # for m in runs.data['metrics']:
#         #     key, subset = key_subset_split(m['key'])

#         #     metric = [metric for metric in get_metric_history(key, subset=subset, run_id=runs.info['run_id']) if metric['step'] == step]
#         #     for item in metric:
#         #         k, s = key_subset_split(item['key'])
#         #         if k in model_tags['metric'].keys():
#         #             model_tags['metric'][k].update({s: item['value']} if s else item['value'])
#         #         else:
#         #             model_tags['metric'].update({
#         #                 k: {s: item['value']} if s else item['value']
#         #             })

#         # 2. Latest Metric 가져오기
#         model_tags['metric'] = dict()
#         for m in runs.data['metrics']:
#             (key, subset), value = key_subset_split(m['key']), m['value']
#             if key in model_tags['metric'].keys():
#                 model_tags['metric'][key].append({
#                     'subset': subset,
#                     'value': value
#                 })
#             else:
#                 model_tags['metric'][key] = [{
#                     'subset': subset,
#                     'value': value
#                 }]
#     else:
#         model_tags['metric'] = metric

#     if tags:
#         model_tags.update(tags)

#     log_dict(run_id, model_tags, f'models/{model_nm}_step_{step}.txt')



