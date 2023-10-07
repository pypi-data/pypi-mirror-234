from typing import List

import kognic.io.client as IOC
from kognic.io import model as IAM


def run(client: IOC.KognicIOClient) -> List[IAM.Project]:
    print("Listing projects...")

    return client.project.get_projects()


if __name__ == "__main__":
    client = IOC.KognicIOClient()
    projects = run(client)

    for project in projects:
        print(f"Project: {project.external_id}")
        batches = client.project.get_project_batches(project.external_id)

        print(", ".join([batch.external_id for batch in batches]))
