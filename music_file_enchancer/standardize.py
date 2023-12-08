import eyed3
import cloudscraper

from eyed3.id3.frames import ImageFrame

from .extractors.apple_music import Extractor_interface
from music_file_enchancer.utils import request_data


class Standardize:
    """Standardizes music file given filepath and name"""

    def __init__(self, music_name: str, filepath: str):
        self.music_name = music_name
        self.filepath = filepath
        self.session = cloudscraper.CloudScraper()

    def __change_tags(
        self, artist: str, title: str, album: str, genre: str, front_cover_bin
    ) -> None:
        """changes tags of mp3 file"""

        audiofile = eyed3.load(self.filepath)
        if audiofile.tag is None:
            audiofile.initTag()

        audiofile.tag.album = album
        audiofile.tag.artist = artist
        audiofile.tag.title = title
        audiofile.tag.genre = genre
        audiofile.tag.comments.set("No", "comment")
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, front_cover_bin, "image/jpeg")

        audiofile.tag.save()

    def standardize(self, Extractor: Extractor_interface) -> None:
        data = Extractor(name=self.music_name, session=self.session).data_json()

        if data:
            self.__change_tags(
                artist=data["artist"],
                title=data["title"],
                album=data["album"],
                genre=data["genres"],
                front_cover_bin=request_data(
                    url=data["front_cover_url"], session=self.session
                ).content,
            )
        else:
            print("Not Found")
