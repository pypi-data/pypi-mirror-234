import kognic.io.client as IOC


def run(client: IOC.KognicIOClient, input_uuid: str) -> None:
    print("Deleting input...")
    return client.input.delete_input(input_uuid=input_uuid)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    input_uuid = "Input-identifier"
    run(client, input_uuid)
