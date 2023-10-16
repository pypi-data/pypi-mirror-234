def write_entity(
        path: str,
        filename: str,
        content: str
):
    with open(f"{path}/{filename}.py", "w") as file:
        file.write(content)
