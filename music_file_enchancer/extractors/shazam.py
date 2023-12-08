'''
class Shazam_Results:
    def __init__(self,
                 artist: str,
                 song_name: str,
                 session=cloudscraper.CloudScraper()):
        self.artist = artist
        self.song_name = song_name
        self.session = session

    def __gen_search_url(self) -> str:
        keyword = url_encode(f"{self.artist}-{self.song_name}")
        search_url = f"https://www.shazam.com/services/search/v4/en/TM/web/search?term={ keyword }&offset=0&limit=10&types=songs"
        return search_url

    def __gen_data_url(self) -> str:
        key = self.__match_names()
        url = f"https://www.shazam.com/discovery/v5/en/TM/web/-/track/{key}?shazamapiversion=v3&video=v3"
        return url

    def __match_names(self) -> int:
        search_url = self.__gen_search_url()
        try:
            data = request_data(url=search_url, session=self.session)
            if data == {}:
                raise NotFoundError
            else:
                keys = data["tracks"]["hits"]
        except NotFoundError:
            print("Not Found")
            sys.exit()

        artist_ratio = [0, 0]
        music_ratio = [0, 0]

        for index, tracks in enumerate(keys):
            music_name = tracks["track"]['title']
            artist_result = tracks["track"]["subtitle"]

            artist_title = fuzz.token_set_ratio(self.artist, artist_result)
            music_title = fuzz.token_set_ratio(self.song_name, music_name)

            if artist_title > artist_ratio[0]:
                artist_ratio[0] = artist_title
                artist_ratio[1] = index

            if music_title > music_ratio[0]:
                music_ratio[0] = music_title
                music_ratio[1] = index

        indexes = sorted([artist_ratio[1], music_ratio[1]])
        key = keys[indexes[-1]]['track']['key']

        return key

    def data_json(self) -> dict:
        # request timeout
        res2 = request_data(url=self.__gen_data_url(), session=self.session)
        music_name = res2["title"]
        artist_name = res2["subtitle"]
        album_name = res2["sections"][0]["metadata"][0]["text"]
        album_cover_url = res2["images"]["coverart"]
        backcover_url = res2["images"]["background"]
        genres = res2['genres']['primary']

        data = {
            "title": music_name,
            "artist": artist_name,
            "album": album_name,
            "front_cover_url": album_cover_url,
            "back_cover_url": backcover_url,
            "genres": genres,
            "album_artist": artist_name,
        }

        return data
'''
