""" music_playlist.py

The iterator pattern provides a way to access elements of a collection sequentially without exposing
its internal representation (lists, dits, trees)"""

from typing import List, Iterator

# The Element
class Song:
    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration


    def __repr__(self):
        mins, secs = divmod(self.duration, 60)
        return f"{self.title} by {self.artist} [{mins}:{secs:02d}]"
    
# The Iterator
class PlaylistIterator(Iterator):
    def __init__(self, songs: List[Song]):
        self._songs = songs
        self._index = 0
    

    def __next__(self) -> Song:
        if self._index < len(self._songs):
            song = self._songs[self._index]
            self._index += 1
            return song
        
        raise StopIteration
    
# The Aggregate (iterable)
class Playlist:
    def __init__(self, name: str):
        self.name = name
        self._songs: List[Song] = []

    def add_song(self, song: Song):
        self._songs.append(song)

    def __iter__(self) -> PlaylistIterator:
        """ Return an iterator that can go through the playlist"""   
        return PlaylistIterator(self._songs)

# Example usage
if __name__ == "__main__":
    playlist = Playlist("Morning vibes")
    playlist.add_song(Song("sunrise", "lo-fi", 180))
    playlist.add_song(Song("Coffee Time", "Accoustic mood", 210))
    playlist.add_song(Song("Easy start", "Calm Piano", 400))

    print(f"Playlist: {playlist.name}\n Songs:")
    for song in playlist:
        print("->", song)

""" Advantages of the iterator pattern"""
""" 
Encapsulation 
"""