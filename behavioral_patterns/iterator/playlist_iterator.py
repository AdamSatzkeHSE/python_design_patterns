# Requirements:

# Create a Song class with:

# title

# artist

# __repr__() that prints "title by artist"

# Create a Playlist class (the aggregate) that:

# Stores a list of Song objects.

# Has a method add_song(song).

# Implements __iter__() that returns a PlaylistIterator.

# Create a PlaylistIterator class (the iterator) that:

# Implements __iter__() (returns self).

# Implements __next__() to return songs one by one.

# Raises StopIteration when finished.

# Use a for loop to iterate through all songs in the playlist.

# from typing import List, Iterator

# 1. Element class
class Song:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def __repr__(self):
        return f"{self.title} by {self.artist}"


# 2. Iterator class
class PlaylistIterator(Iterator[Song]):
    def __init__(self, songs: List[Song]):
        self._songs = songs
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Song:
        if self._index < len(self._songs):
            song = self._songs[self._index]
            self._index += 1
            return song
        else:
            raise StopIteration


# 3. Aggregate class
class Playlist:
    def __init__(self, name: str):
        self.name = name
        self._songs: List[Song] = []

    def add_song(self, song: Song):
        self._songs.append(song)

    def __iter__(self) -> PlaylistIterator:
        return PlaylistIterator(self._songs)


# 4. Usage
if __name__ == "__main__":
    playlist = Playlist("Road Trip Mix")
    playlist.add_song(Song("Highway to Hell", "AC/DC"))
    playlist.add_song(Song("On the Road Again", "Willie Nelson"))
    playlist.add_song(Song("Life is a Highway", "Tom Cochrane"))

    print(f"Songs in '{playlist.name}':")
    for song in playlist:
        print("🎵", song)
