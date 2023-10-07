import abc


class DownloaderInterface(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass

    def print(self, text):
        print(text)


class DownloaderDesktop(DownloaderInterface):
    def start(self):
        print("start")


class DownloaderController(DownloaderInterface):
    def start(self):
        print("controller start")


if __name__ == '__main__':
    downloader = DownloaderController()
    downloader.start()
