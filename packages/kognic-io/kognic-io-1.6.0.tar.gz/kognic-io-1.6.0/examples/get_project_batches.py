from typing import List

import kognic.io.client as IOC
from kognic.io import model as IAM


def run(client: IOC.KognicIOClient, project: str) -> List[IAM.ProjectBatch]:
    print("Listing project batches...")

    return client.project.get_project_batches(project)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    project = "Project-Identifier"
    project_batches = run(client, project=project)
