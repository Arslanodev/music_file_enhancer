import cloudscraper

from bs4 import BeautifulSoup
from typing import Tuple


from .extractors import Extractor_interface
from music_file_enchancer.utils import url_encode, request_base_html
from music_file_enchancer.extractors.extractors import NotFoundError


DETAILS_URL_SELECTOR = "#scrollable-page > main > div > div.desktop-search-page.svelte-e9u219 > div:nth-of-type(1) > div > ul > li:nth-child(1) > div > div > div.top-search-lockup__action.svelte-ldozvk > a"


class Apple_Music_Template_Extractor(Extractor_interface):
    """Extracts necessary data from Apple Music website"""

    def __init__(self, name: str, session: cloudscraper.CloudScraper):
        self.name = name
        self.session = session

    def __gen_search_url(self):
        name = url_encode(self.name)
        return f"https://music.apple.com/us/search?term={name}"

    def __main_op(self):
        # Generate search url
        url = self.__gen_search_url()

        # Request base html
        bs_html = request_base_html(url=url, s=self.session)

        # Parse search result html tag
        search_result_html = bs_html.select_one(DETAILS_URL_SELECTOR)

        # Get url link from results for details
        if search_result_html:
            url = search_result_html.get("href")
            # Request details html
            details_html = request_base_html(url=url, s=self.session)

            # From details html get album cover url
            album_cover_url = self.__get_album_cover(details_html)

            # From details html get album description
            album_name, genre = self.__get_album_desc(details_html)

            # from search results html get artist and song name
            artist, song_name = self.__get_music_names(search_result_html)

            self.artist = artist
            self.song_name = song_name
            self.music_type = genre
            self.album_name = album_name
            self.cover_url = album_cover_url
        else:
            raise NotFoundError

    def __get_music_names(self, search_res_html: BeautifulSoup) -> Tuple[str]:
        """returns artist name and song name"""
        full_name = search_res_html.get("aria-label").split("·")
        song_name = full_name[0].strip()
        artist = full_name[-1].strip()

        return artist, song_name

    def __get_album_cover(self, details_html: BeautifulSoup) -> str:
        """returns url for downloading album cover"""
        image_tag = details_html.find("picture").find_all("source")[1].get("srcset")
        album_cover_url = image_tag.split(",")[-1].split()[0]

        return album_cover_url

    def __get_album_desc(self, details_html: BeautifulSoup) -> Tuple[str]:
        """returns album name and genre name"""
        headings = details_html.find("div", class_="headings")
        album_name = headings.find("h1").text
        genre = headings.find("div", class_="headings__metadata-bottom").text

        return album_name, genre.split()[0]

    def data_json(self) -> dict:
        try:
            self.__main_op()
            return {
                "title": self.song_name,
                "artist": self.artist,
                "album": self.album_name,
                "front_cover_url": self.cover_url,
                "genres": self.music_type,
            }
        except NotFoundError:
            return None
