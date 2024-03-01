import click
import os

from .standardize import Standardize
from .extractors.apple_music import Apple_Music_Template_Extractor


def runner(filepath):
    """Enchances mp3 files by changing its tags

    FILEPATH you input location of your music file
    """

    # Get file extension
    filename = os.path.splitext(filepath)
    file_ext = filename[1]
    music_name = filename[0].split("/")[-1]

    # Check if file extensions is supported
    if file_ext == ".mp3":
        print(music_name)
        obj = Standardize(music_name=music_name, filepath=filepath)
        obj.standardize(Extractor=Apple_Music_Template_Extractor)
    else:
        return click.echo("Unsupported filetype")


@click.command(
    help="Simple cli application that helps to enchance mp3 file downloaded from third parties"
)
@click.argument("filepath", nargs=1)
def enchance_mp3_file(filepath):
    """function for getting input and run runner function"""
    isfile = os.path.isfile(filepath)
    # Check if intput filepath is folder
    if isfile:
        runner(filepath)
    else:
        for file in os.listdir(filepath):
            fl_path = os.path.join(filepath, file)
            if os.path.isdir(fl_path):
                continue
            else:
                runner(fl_path)


if __name__ == "__main__":
    enchance_mp3_file()
