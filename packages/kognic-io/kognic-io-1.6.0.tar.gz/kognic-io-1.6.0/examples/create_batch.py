import kognic.io.client as IOC
from kognic.io.model.projects.project_batch import ProjectBatch


def run(client: IOC.KognicIOClient, project: str, batch: str) -> ProjectBatch:
    print(f"Create batch {batch} in project {project}")

    return client.project.create_batch(project, batch)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    project = "Project-Identifier"
    batch = "New-Batch-Identifier"
    annotation_types = run(client, project, batch)
