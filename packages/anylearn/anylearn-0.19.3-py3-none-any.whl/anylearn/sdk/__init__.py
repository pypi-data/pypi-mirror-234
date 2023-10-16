from anylearn.sdk.artifacts.algorithm import AlgorithmArtifact
from anylearn.sdk.artifacts.artifact import Artifact, ArtifactState
from anylearn.sdk.artifacts.dataset import DatasetArtifact
from anylearn.sdk.artifacts.file import FileArtifact
from anylearn.sdk.artifacts.model import ModelArtifact
from anylearn.sdk.project import Project
from anylearn.sdk.task import Task


def get_task_output(task_id: str) -> FileArtifact:
    task = Task.from_id(task_id)
    return FileArtifact.from_id(task.output_artifact_id)
