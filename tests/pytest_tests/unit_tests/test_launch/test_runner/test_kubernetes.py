import asyncio
import base64
import json
from typing import Any
from unittest.mock import MagicMock

import pytest
import yaml
from kubernetes_asyncio.client import ApiException
from wandb.sdk.launch._project_spec import LaunchProject
from wandb.sdk.launch.errors import LaunchError
from wandb.sdk.launch.runner.kubernetes_monitor import (
    CRD_STATE_DICT,
    LaunchKubernetesMonitor,
    _state_from_conditions,
)
from wandb.sdk.launch.runner.kubernetes_runner import (
    KubernetesRunner,
    KubernetesSubmittedRun,
    add_entrypoint_args_overrides,
    add_label_to_pods,
    add_wandb_env,
    maybe_create_imagepull_secret,
)


@pytest.fixture
def clean_monitor():
    """Fixture for cleaning up the monitor class between tests."""
    LaunchKubernetesMonitor._instance = None
    yield
    LaunchKubernetesMonitor._instance = None


@pytest.fixture
def manifest():
    return {
        "kind": "Job",
        "spec": {
            "template": {
                "metadata": {
                    "labels": {
                        "app": "wandb",
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "master",
                            "image": "${image_uri}",
                            "imagePullPolicy": "IfNotPresent",
                            "env": [
                                {"name": "MY_ENV_VAR", "value": "MY_VALUE"},
                            ],
                        },
                        {
                            "name": "worker",
                            "image": "${image_uri}",
                            "workingDir": "/home",
                            "imagePullPolicy": "IfNotPresent",
                        },
                    ],
                    "restartPolicy": "OnFailure",
                },
            }
        },
    }


def test_add_env(manifest):
    """Test that env vars are added to custom k8s specs."""
    env = {
        "TEST_ENV": "test_value",
        "TEST_ENV_2": "test_value_2",
        "WANDB_RUN_ID": "test_run_id",
    }
    add_wandb_env(manifest, env)
    assert manifest["spec"]["template"]["spec"]["containers"][0]["env"] == [
        {"name": "MY_ENV_VAR", "value": "MY_VALUE"},
        {"name": "TEST_ENV", "value": "test_value"},
        {"name": "TEST_ENV_2", "value": "test_value_2"},
        {"name": "WANDB_RUN_ID", "value": "test_run_id"},
    ]
    assert manifest["spec"]["template"]["spec"]["containers"][1]["env"] == [
        {"name": "TEST_ENV", "value": "test_value"},
        {"name": "TEST_ENV_2", "value": "test_value_2"},
    ]


def test_add_label(manifest):
    """Test that we add labels to pod specs correctly."""
    add_label_to_pods(manifest, "test_label", "test_value")
    assert manifest["spec"]["template"]["metadata"]["labels"] == {
        "app": "wandb",
        "test_label": "test_value",
    }


def test_add_entrypoint_args_overrides(manifest):
    """Test that we add entrypoint args to pod specs correctly."""
    overrides = {"args": ["--test_arg", "test_value"], "command": ["test_entry"]}
    add_entrypoint_args_overrides(manifest, overrides)
    assert manifest["spec"]["template"]["spec"]["containers"][0]["args"] == [
        "--test_arg",
        "test_value",
    ]
    assert manifest["spec"]["template"]["spec"]["containers"][1]["args"] == [
        "--test_arg",
        "test_value",
    ]
    assert manifest["spec"]["template"]["spec"]["containers"][0]["command"] == [
        "test_entry"
    ]
    assert manifest["spec"]["template"]["spec"]["containers"][1]["command"] == [
        "test_entry"
    ]


@pytest.fixture
def volcano_spec():
    return {
        "apiVersion": "batch.volcano.sh/v1alpha1",
        "kind": "Job",
        "metadata": {"name": "test-job"},
        "tasks": [
            {
                "name": "master",
                "replicas": 1,
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": "master",
                                "image": "${image_uri}",
                                "imagePullPolicy": "IfNotPresent",
                                "env": [
                                    {"name": "MY_ENV_VAR", "value": "MY_VALUE"},
                                ],
                            },
                            {
                                "name": "worker",
                                "image": "${image_uri}",
                                "workingDir": "/home",
                                "imagePullPolicy": "IfNotPresent",
                            },
                        ],
                        "restartPolicy": "OnFailure",
                    }
                },
            }
        ],
    }


class MockDict(dict):
    # use a dict to mock an object
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = MockDict(v)
            elif isinstance(v, list):
                self[k] = [MockDict(i) if isinstance(i, dict) else i for i in v]


class MockPodList:
    def __init__(self, pods):
        self.pods = pods

    @property
    def items(self):
        return self.pods


class MockEventStream:
    """Mocks a kubernetes event stream that can be populated from tests."""

    def __init__(self):
        self.queue = []

    async def __aiter__(self):
        while True:
            while not self.queue:
                await asyncio.sleep(0)
            yield self.queue.pop(0)

    async def add(self, event: Any):
        self.queue.append(event)


class MockBatchApi:
    """Mocks a kubernetes batch API client."""

    def __init__(self):
        self.jobs = dict()

    async def read_namespaced_job(self, name, namespace):
        return self.jobs[name]

    async def read_namespaced_job_status(self, name, namespace):
        return self.jobs[name]

    async def patch_namespaced_job(self, name, namespace, body):
        if body.spec.suspend:
            self.jobs[name].status.conditions = [MockDict({"type": "Suspended"})]
            self.jobs[name].status.active -= 1

    async def delete_namespaced_job(self, name, namespace):
        del self.jobs[name]

    async def list_namespaced_job(self, namespace, field_selector=None):
        return [self.jobs[name] for name in self.jobs]

    async def create_job(self, body):
        self.jobs[body["metadata"]["generateName"]] = body
        return body


class MockCoreV1Api:
    def __init__(self):
        self.pods = dict()
        self.secrets = []

    async def list_namespaced_pod(
        self, label_selector=None, namespace="default", field_selector=None
    ):
        ret = []
        for _, pod in self.pods.items():
            ret.append(pod)
        return MockPodList(ret)

    async def read_namespaced_pod(self, name, namespace):
        return self.pods[name]

    async def delete_namespaced_secret(self, namespace, name):
        pass

    async def create_namespaced_secret(self, namespace, body):
        self.secrets.append((namespace, body))


class MockCustomObjectsApi:
    def __init__(self):
        self.jobs = dict()

    async def create_namespaced_custom_object(
        self, group, version, namespace, plural, body
    ):
        self.jobs[body["metadata"]["name"]] = body
        return body

    async def delete_namespaced_custom_object(
        self, group, version, namespace, plural, name, body
    ):
        del self.jobs[name]

    async def read_namespaced_custom_object(
        self, group, version, namespace, plural, name, body
    ):
        return self.jobs[name]

    async def get_namespaced_custom_object_status(
        self, group, version, namespace, plural, name, body
    ):
        return self.jobs[name]

    async def list_namespaced_custom_object(
        self, group, version, namespace, plural, field_selector=None
    ):
        return [self.jobs[name] for name in self.jobs]


@pytest.fixture
def mock_event_streams(monkeypatch):
    """Patches the kubernetes event stream with a mock and returns it."""
    job_stream = MockEventStream()
    pod_stream = MockEventStream()

    def _select_stream(_, api_call, *args, **kwargs):
        if api_call.__name__ == "list_namespaced_pod":
            return pod_stream
        elif api_call.__name__ == "list_namespaced_job":
            return job_stream
        elif api_call.__name__ == "list_namespaced_custom_object":
            return job_stream
        raise Exception(
            f"Event stream requested for unsupported API call: {api_call.__name__} "
        )

    monkeypatch.setattr(
        "wandb.sdk.launch.monitor.kubernetes_monitor.SafeWatch.stream",
        _select_stream,
    )
    return job_stream, pod_stream


@pytest.fixture
def mock_batch_api(monkeypatch):
    """Patches the kubernetes batch api with a mock and returns it."""
    batch_api = MockBatchApi()
    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.client.BatchV1Api",
        lambda *args, **kwargs: batch_api,
    )
    return batch_api


@pytest.fixture
def mock_core_api(monkeypatch):
    """Patches the kubernetes core api with a mock and returns it."""
    core_api = MockCoreV1Api()
    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.client.CoreV1Api",
        lambda *args, **kwargs: core_api,
    )
    return core_api


@pytest.fixture
def mock_custom_api(monkeypatch):
    """Patches the kubernetes custom api with a mock and returns it."""
    custom_api = MockCustomObjectsApi()
    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.client.CustomObjectsApi",
        lambda *args, **kwargs: custom_api,
    )
    return custom_api


@pytest.fixture
def mock_kube_context_and_api_client(monkeypatch):
    """Patches the kubernetes context and api client with a mock and returns it."""

    async def _mock_get_kube_context_and_api_client():
        return (None, None)

    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.get_kube_context_and_api_client",
        lambda *args, **kwargs: _mock_get_kube_context_and_api_client(),
    )


@pytest.fixture
def mock_maybe_create_image_pullsecret(monkeypatch):
    """Patches the kubernetes context and api client with a mock and returns it."""

    async def _mock_maybe_create_image_pullsecret():
        return None

    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.maybe_create_imagepull_secret",
        lambda *args, **kwargs: _mock_maybe_create_image_pullsecret(),
    )


@pytest.fixture
def mock_create_from_yaml(monkeypatch):
    """Patches the kubernetes create_from_yaml with a mock and returns it."""
    function_mock = MagicMock()
    function_mock.return_value = [[MockDict({"metadata": {"name": "test-job"}})]]

    async def _mock_create_from_yaml(*args, **kwargs):
        return function_mock(*args, **kwargs)

    monkeypatch.setattr(
        "kubernetes_asyncio.utils.create_from_yaml",
        lambda *args, **kwargs: _mock_create_from_yaml(*args, **kwargs),
    )
    return function_mock


@pytest.mark.asyncio
async def test_launch_kube_works(
    monkeypatch,
    mock_event_streams,
    mock_batch_api,
    mock_kube_context_and_api_client,
    mock_maybe_create_image_pullsecret,
    mock_create_from_yaml,
    test_api,
    manifest,
    clean_monitor,
):
    """Test that we can launch a kubernetes job."""
    mock_batch_api.jobs = {"test-job": MockDict(manifest)}
    project = LaunchProject(
        docker_config={"docker_image": "test_image"},
        target_entity="test_entity",
        target_project="test_project",
        resource_args={"kubernetes": manifest},
        launch_spec={},
        overrides={
            "args": ["--test_arg", "test_value"],
            "command": ["test_entry"],
        },
        resource="kubernetes",
        api=test_api,
        git_info={},
        job="",
        uri="https://wandb.ai/test_entity/test_project/runs/test_run",
        run_id="test_run_id",
        name="test_run",
    )
    runner = KubernetesRunner(
        test_api, {"SYNCHRONOUS": False}, MagicMock(), MagicMock()
    )
    submitted_run = await runner.run(project, "hello-world")
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "unknown"
    job_stream, pod_stream = mock_event_streams
    await pod_stream.add(  # This event does nothing. Added for code coverage of the path where there is no status.
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {"labels": {"job-name": "test-job"}},
                    "status": {"phase": "Pending"},
                },
            }
        )
    )
    await pod_stream.add(
        MockDict(
            {
                "type": "ADDED",
                "object": {
                    "metadata": {"name": "test-pod"},
                    "status": {"phase": "Pending"},
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "unknown"
    await pod_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {
                        "name": "test-pod",
                        "labels": {"job-name": "test-job"},
                    },
                    "status": {
                        "phase": "Pending",
                        "container_statuses": [
                            {
                                "name": "master",
                                "state": {"waiting": {"reason": "ContainerCreating"}},
                            }
                        ],
                    },
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "running"
    await job_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {"name": "test-job"},
                    "status": {"succeeded": 1},
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "finished"
    assert mock_create_from_yaml.call_count == 1
    submitted_manifest = mock_create_from_yaml.call_args_list[0][0][1]
    with open(submitted_manifest) as f:
        submitted_manifest = yaml.safe_load(f)
    assert submitted_manifest["spec"]["template"]["spec"]["containers"][0]["args"] == [
        "--test_arg",
        "test_value",
    ]
    assert (
        submitted_manifest["spec"]["template"]["spec"]["containers"][0][
            "imagePullPolicy"
        ]
        == "IfNotPresent"
    )
    # Test cancel
    assert "test-job" in mock_batch_api.jobs
    await submitted_run.cancel()
    assert "test-job" not in mock_batch_api.jobs

    def _raise_api_exception(*args, **kwargs):
        raise ApiException()

    mock_batch_api.delete_namespaced_job = _raise_api_exception
    with pytest.raises(LaunchError):
        await submitted_run.cancel()


@pytest.mark.asyncio
async def test_launch_crd_works(
    monkeypatch,
    mock_event_streams,
    mock_batch_api,
    mock_custom_api,
    mock_kube_context_and_api_client,
    mock_create_from_yaml,
    test_api,
    volcano_spec,
    clean_monitor,
):
    """Test that we can launch a kubernetes job."""
    monkeypatch.setattr(
        "wandb.sdk.launch.runner.kubernetes_runner.maybe_create_imagepull_secret",
        lambda *args, **kwargs: None,
    )
    mock_batch_api.jobs = {"test-job": MockDict(volcano_spec)}
    project = LaunchProject(
        docker_config={"docker_image": "test_image"},
        target_entity="test_entity",
        target_project="test_project",
        resource_args={"kubernetes": volcano_spec},
        launch_spec={},
        overrides={
            "args": ["--test_arg", "test_value"],
            "command": ["test_entry"],
        },
        resource="kubernetes",
        api=test_api,
        git_info={},
        job="",
        uri="https://wandb.ai/test_entity/test_project/runs/test_run",
        run_id="test_run_id",
        name="test_run",
    )
    runner = KubernetesRunner(
        test_api, {"SYNCHRONOUS": False}, MagicMock(), MagicMock()
    )
    submitted_run = await runner.run(project, MagicMock())
    assert str(await submitted_run.get_status()) == "unknown"
    job_stream, pod_stream = mock_event_streams
    # add container creating event
    await pod_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {
                        "name": "test-pod",
                        "labels": {"job-name": "test-job"},
                    },
                    "status": {
                        "phase": "Pending",
                        "container_statuses": [
                            {
                                "name": "master",
                                "state": {"waiting": {"reason": "ContainerCreating"}},
                            }
                        ],
                    },
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "running"
    await job_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {"name": "test-job"},
                    "status": {"state": {"phase": "Running"}},
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "running"
    await job_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {"name": "test-job"},
                    "status": {
                        "conditions": [
                            {
                                "type": "Succeeded",
                                "status": "True",
                                "lastTransitionTime": "2021-09-06T20:04:12Z",
                            }
                        ]
                    },
                },
            }
        )
    )
    await asyncio.sleep(1)
    assert str(await submitted_run.get_status()) == "finished"


@pytest.mark.timeout(320)
@pytest.mark.asyncio
async def test_launch_kube_failed(
    monkeypatch,
    mock_batch_api,
    mock_kube_context_and_api_client,
    mock_create_from_yaml,
    mock_maybe_create_image_pullsecret,
    mock_event_streams,
    test_api,
    manifest,
    clean_monitor,
):
    """Test that we can launch a kubernetes job."""
    mock_batch_api.jobs = {"test-job": manifest}
    project = LaunchProject(
        docker_config={"docker_image": "test_image"},
        target_entity="test_entity",
        target_project="test_project",
        resource_args={"kubernetes": manifest},
        launch_spec={},
        overrides={
            "args": ["--test_arg", "test_value"],
            "command": ["test_entry"],
        },
        resource="kubernetes",
        api=test_api,
        git_info={},
        job="",
        uri="https://wandb.ai/test_entity/test_project/runs/test_run",
        run_id="test_run_id",
        name="test_run",
    )
    runner = KubernetesRunner(
        test_api, {"SYNCHRONOUS": False}, MagicMock(), MagicMock()
    )
    job_stream, _ = mock_event_streams
    await job_stream.add(
        MockDict(
            {
                "type": "MODIFIED",
                "object": {
                    "metadata": {"name": "test-job"},
                    "status": {"failed": 1},
                },
            }
        )
    )
    submitted_run = await runner.run(project, "test_image")
    await submitted_run.wait()
    assert str(await submitted_run.get_status()) == "failed"


@pytest.mark.asyncio
async def test_maybe_create_imagepull_secret_given_creds():
    mock_registry = MagicMock()

    async def _mock_get_username_password():
        return ("testuser", "testpass")

    mock_registry.get_username_password.return_value = _mock_get_username_password()
    mock_registry.uri = "test.com"
    api = MockCoreV1Api()
    await maybe_create_imagepull_secret(
        api,
        mock_registry,
        "12345678",
        "wandb",
    )
    namespace, secret = api.secrets[0]
    assert namespace == "wandb"
    assert secret.metadata.name == "regcred-12345678"
    assert secret.data[".dockerconfigjson"] == base64.b64encode(
        json.dumps(
            {
                "auths": {
                    "test.com": {
                        "auth": "dGVzdHVzZXI6dGVzdHBhc3M=",  # testuser:testpass
                        "email": "deprecated@wandblaunch.com",
                    }
                }
            }
        ).encode("utf-8")
    ).decode("utf-8")


# Test monitor class.


def job_factory(name, statuses):
    """Factory for creating job events."""
    return MockDict(
        {
            "object": {
                "status": {f"{status}": 1 for status in statuses},
                "metadata": {"name": name},
            }
        }
    )


def pod_factory(event_type, job_name, condition_types, condition_reasons, phase=None):
    """Factory for creating pod events.

    Args:
        event_type (str): The type of event to create.
        condition_types (list): The types of conditions to create.
        condition_reasons (list): The reasons of conditions to create.

    Returns:
        dict: The pod event.
    """
    return MockDict(
        {
            "type": event_type,
            "object": {
                "metadata": {
                    "labels": {"job-name": job_name},
                },
                "status": {
                    "phase": phase,
                    "conditions": [
                        {
                            "type": condition_type,
                            "reason": condition_reason,
                        }
                        for condition_type, condition_reason in zip(
                            condition_types, condition_reasons
                        )
                    ],
                },
            },
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reason",
    ["EvictionByEvictionAPI", "PreemptionByScheduler", "TerminationByKubelet"],
)
async def test_monitor_preempted(
    mock_event_streams, mock_batch_api, mock_core_api, reason, clean_monitor
):
    """Test if the monitor thread detects a preempted job."""
    await LaunchKubernetesMonitor.ensure_initialized()
    LaunchKubernetesMonitor.monitor_namespace("wandb")
    _, pod_event_stream = mock_event_streams
    await pod_event_stream.add(pod_factory("ADDED", "test-job", [], []))
    await asyncio.sleep(0.1)
    await pod_event_stream.add(
        pod_factory("MODIFIED", "test-job", ["DisruptionTarget"], [reason])
    )
    await asyncio.sleep(0.1)
    assert LaunchKubernetesMonitor.get_status("test-job").state == "preempted"


@pytest.mark.asyncio
async def test_monitor_succeeded(
    mock_event_streams, mock_batch_api, mock_core_api, clean_monitor
):
    """Test if the monitor thread detects a succeeded job."""
    await LaunchKubernetesMonitor.ensure_initialized()
    LaunchKubernetesMonitor.monitor_namespace("wandb")
    job_event_stream, pod_event_stream = mock_event_streams
    await asyncio.sleep(0.1)
    await pod_event_stream.add(pod_factory("ADDED", "job-name", [], []))
    await asyncio.sleep(0.1)
    await job_event_stream.add(job_factory("job-name", ["succeeded"]))
    await asyncio.sleep(0.1)
    assert LaunchKubernetesMonitor.get_status("job-name").state == "finished"


@pytest.mark.asyncio
async def test_monitor_failed(
    mock_event_streams, mock_batch_api, mock_core_api, clean_monitor
):
    """Test if the monitor thread detects a failed job."""
    await LaunchKubernetesMonitor.ensure_initialized()
    LaunchKubernetesMonitor.monitor_namespace("wandb")
    job_event_stream, pod_event_stream = mock_event_streams
    await asyncio.sleep(0.1)
    await pod_event_stream.add(pod_factory("ADDED", "job-name", [], []))
    await asyncio.sleep(0.1)
    await job_event_stream.add(job_factory("job-name", ["failed"]))
    await asyncio.sleep(0.1)
    assert LaunchKubernetesMonitor.get_status("job-name").state == "failed"


@pytest.mark.asyncio
async def test_monitor_running(
    mock_event_streams, mock_batch_api, mock_core_api, clean_monitor
):
    """Test if the monitor thread detects a running job."""
    await LaunchKubernetesMonitor.ensure_initialized()
    LaunchKubernetesMonitor.monitor_namespace("wandb")
    job_event_stream, pod_event_stream = mock_event_streams
    await asyncio.sleep(0.1)
    await pod_event_stream.add(pod_factory("ADDED", "job-name", [], []))
    await asyncio.sleep(0.1)
    await job_event_stream.add(job_factory("job-name", ["active"]))
    await pod_event_stream.add(
        pod_factory("MODIFIED", "job-name", [""], [""], phase="Running")
    )
    await asyncio.sleep(0.1)
    assert LaunchKubernetesMonitor.get_status("job-name").state == "running"


# Test util functions


def condition_factory(
    condition_type, condition_status, condition_reason, transition_time
):
    """Factory for creating conditions."""
    return MockDict(
        {
            "type": condition_type,
            "status": condition_status,
            "reason": condition_reason,
            "lastTransitionTime": transition_time,
        }
    )


@pytest.mark.parametrize(
    "conditions, expected",
    [
        (
            [
                condition_factory("PodScheduled", "True", "", "2023-09-06T20:04:11Z"),
                condition_factory("Initialized", "True", "", "2023-09-06T20:04:12Z"),
                condition_factory(
                    "ContainersReady", "True", "", "2023-09-06T20:04:13Z"
                ),
                condition_factory("Running", "True", "", "2023-09-06T20:04:14Z"),
            ],
            "running",
        ),
        (
            [
                condition_factory("PodScheduled", "True", "", "2023-09-06T20:04:11Z"),
                condition_factory("Initialized", "True", "", "2023-09-06T20:04:12Z"),
                condition_factory(
                    "ContainersReady", "True", "", "2023-09-06T20:04:13Z"
                ),
                condition_factory("Running", "False", "", "2023-09-06T20:04:14Z"),
            ],
            None,
        ),
    ],
)
def test_state_from_conditions(conditions, expected):
    """Test that we extract CRD state from conditions correctly."""
    state = _state_from_conditions(conditions)
    if isinstance(state, str):
        assert CRD_STATE_DICT[state.lower()] == expected
    else:
        assert state == expected is None


# Tests for KubernetesSubmittedRun


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pods,logs,expected",
    [
        (
            MockPodList(
                [
                    MockDict(
                        {
                            "metadata": MockDict(
                                {
                                    "name": "test_pod",
                                    "labels": {"job-name": "test_job"},
                                }
                            )
                        }
                    )
                ]
            ),
            "test_log",
            "test_log",
        ),
        (MockPodList([]), "test_log", None),
        (Exception(), "test_log", None),
        (
            MockPodList(
                [
                    MockDict(
                        {
                            "metadata": MockDict(
                                {
                                    "name": "test_pod",
                                    "labels": {"job-name": "test_job"},
                                }
                            )
                        }
                    )
                ]
            ),
            Exception(),
            None,
        ),
    ],
)
async def test_kubernetes_submitted_run_get_logs(pods, logs, expected):
    core_api = MagicMock()

    async def _mock_list_namespaced_pod(*args, **kwargs):
        if isinstance(pods, Exception):
            raise pods
        return pods

    async def _mock_read_namespaced_pod_log(*args, **kwargs):
        if isinstance(logs, Exception):
            raise logs
        return logs

    core_api.list_namespaced_pod = _mock_list_namespaced_pod
    core_api.read_namespaced_pod_log = _mock_read_namespaced_pod_log

    submitted_run = KubernetesSubmittedRun(
        batch_api=MagicMock(),
        core_api=core_api,
        namespace="wandb",
        name="test_run",
    )
    # Assert that we get the logs back.
    assert await submitted_run.get_logs() == expected
