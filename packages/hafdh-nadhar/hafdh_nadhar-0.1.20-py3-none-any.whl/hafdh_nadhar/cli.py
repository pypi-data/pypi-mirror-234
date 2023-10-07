import typer

from hafdh_nadhar.hafdh import hafdh_img

app = typer.Typer()


@app.command()
def hafdh(img_path: str):
    """Remove human representations from an image by blurring them"""
    hafdh_img(img_path=img_path)


if __name__ == "__main__":
    app()
