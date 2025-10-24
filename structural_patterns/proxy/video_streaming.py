""" A Proxy is an object that acts as a stand-in for another object, controlling access to it.
It has the same interface as the real object but adds extra behavior:

- Access control / security
- Lazy loading
- Caching
- Logging monitoring, validation
- Remote communication

Proxy = "same interface + extra logic around the real object

"""

# Step 1: The subject interface
from abc import ABC, abstractmethod

class VideoService(ABC):
    @abstractmethod
    def get_video(self, video_id: str) -> str:
        pass

# Step 2: The real Object
import time

class YoutubeService(VideoService):
    def get_video(self, video_id: str) -> str:
        print(f"Fetching video '{video_id}' from YouTube servers...")
        time.sleep(2) # Simulate slow network
        return f"Video data for {video_id}"
    
# Step 3: The Proxy
class YoutubeProxy(VideoService):
    def __init__(self, real_service: YoutubeService):
        self._real_service = real_service
        self._cache = {}

    def get_video(self, video_id: str) -> str:
        # Check cache first

        if video_id in self._cache:
            print(f"[Proxy] Returning cached video '{video_id}'")
            return self._cache[video_id]
        
        print(f"[Proxy] Cache miss for '{video_id}'. Fetching from Youtube...")
        video = self._real_service.get_video(video_id)
        self._cache[video_id] = video

        return video
    

# Step 4: Client code
if __name__ == '__main__':
    youtube = YoutubeService()
    proxy = YoutubeProxy(youtube)

    # First access: slow, fetches from server
    print(proxy.get_video("cats_vs_dogs"))
    print()

    # Second access: instant, from cache
    print(proxy.get_video("cats_vs_dogs"))
    print()

    # Another video: new fetch, then cached
    print(proxy.get_video("python_tutorial"))
    print(proxy.get_video("python_tutorial"))