import os

from pytube import YouTube

from FTV.FrameWork.Apps import NIApp
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.TriggerObjects import Condition
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DyStr


class VM(VariableManager):
    def setupVariables(self):
        self.directory = DyStr()
        self.downloadLink = DyStr()
        self.afterDownloadMessage = DyStr()

    def setupTriggers(self):
        pass

    class IsDirExist(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return os.path.exists(new_val)

    class IsLinkValid(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val.startswith("https://www.youtube.com/") or new_val.startswith("https://youtu.be/")


class FM(FeatureManager):
    def setupFeatures(self):
        self.addFeature(ConsoleDownloadAudioFiles)


class ConsoleDownloadAudioFiles(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(DownloadYoutubeAudioFilesApp.vm.START).setAction(self.showIntro)
        self.addTrigger(self.showIntro).setAction(self.askForDirectory)
        self.addTrigger(self.vm.directory) \
            .setCondition(VM.IsDirExist) \
            .setAction(self.askForDownloadLink) \
            .elseAction(self.askForDirectoryAgain)
        self.addTrigger(self.vm.downloadLink) \
            .setCondition(VM.IsLinkValid) \
            .setAction(self.download) \
            .elseAction(self.askForDownloadLinkAgain)
        self.addTrigger(self.vm.afterDownloadMessage).setAction(self.showAfterDownloadMessage)
        self.addTrigger(self.showAfterDownloadMessage).setAction(self.askForDownloadLink)

    @DyMethod()
    def showIntro(self):
        Log.p("Welcome to the Youtube Downloader program!")

    @DyMethod()
    def askForDirectory(self):
        self.vm.directory.set(Log.get("Please enter your download directory: "))

    @DyMethod()
    def askForDirectoryAgain(self):
        self.vm.directory.set(Log.get("The entered directory is does not exist.\n"
                                      "Please try again: "))

    @DyMethod()
    def askForDownloadLink(self):
        self.vm.downloadLink.set(Log.get("Please enter your YouTube url: "))

    @DyMethod()
    def askForDownloadLinkAgain(self):
        self.vm.downloadLink.set(Log.get("The entered url is invalid.\n"
                                         "Please try again: "))

    @DyMethod()
    def download(self):
        self.vm.youtube = YouTube(self.vm.downloadLink.get())
        stream = self.vm.youtube.streams.get_audio_only()
        if stream is None:
            message = "Sorry, could not find an audio stream for this url. Try another one instead."
        else:
            filename = self.makeFilenameLegal(stream.title + "." + stream.subtype)
            try:
                stream.download(self.vm.directory.get(), filename=filename)
                message = f"Download completed: \"{filename}\""
            except Exception:
                message = f"Download failed: \"{filename}\""

        self.vm.afterDownloadMessage.set(message)

    @DyMethod()
    def showAfterDownloadMessage(self):
        Log.p(self.vm.afterDownloadMessage)

    @staticmethod
    def makeFilenameLegal(filename):
        return filename.replace(":", " - ") \
            .replace("?", ".") \
            .replace("/", "-") \
            .replace("\\", "-") \
            .replace("<", "(") \
            .replace(">", ")") \
            .replace("*", " ") \
            .replace("\"", "'") \
            .replace("|", " - ")


class DownloadYoutubeAudioFilesApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setFeatureManager(FM)


DownloadYoutubeAudioFilesApp()

