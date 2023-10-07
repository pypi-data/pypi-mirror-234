import typer

app = typer.Typer()


@app.command()
def hafdh(img_path: str):
    print(f"Hello {img_path}")


if __name__ == "__main__":
    app()
