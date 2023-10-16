import unittest

from FTV.Extra.Experiments.DrawIO.drawio import read, processGraph
from FTV.Tools.Files import Json


class TestArchitectureComparison(unittest.TestCase):
    def setUp(self):
        # Define the reference architecture dictionary
        self.ref_architecture = {
            "App": {
                "name": "DownloadYoutubeAudioFilesApp",
                "dy_variables": [
                    "START",
                    "END"
                ],
                "methods": {},
                "triggers": []
            },
            "Features": [
                {
                    "name": "ConsoleDownloadAudioFiles",
                    "dy_variables": [
                        "directory",
                        "downloadLink",
                        "afterDownloadMessage",
                    ],
                    "methods": {
                        "showIntro": [],
                        "askForDirectory": ["vm.directory"],
                        "askForDirectoryAgain": ["vm.directory"],
                        "askForDownloadLink": ["vm.downloadLink"],
                        "askForDownloadLinkAgain": ["vm.downloadLink"],
                        "download": ["vm.afterDownloadMessage"],
                        "showAfterDownloadMessage": []
                    },
                    "triggers": [
                        {
                            "dy_module": "DownloadYoutubeAudioFilesApp.vm.START",
                            "condition": None,
                            "action": "showIntro",
                            "else_action": None,
                            "thread": None,
                        },
                        {
                            "dy_module": "showIntro",
                            "condition": None,
                            "action": "askForDirectory",
                            "else_action": None,
                            "thread": None,
                        },
                        {
                            "dy_module": "vm.directory",
                            "condition": "IsDirExist",
                            "action": "askForDownloadLink",
                            "else_action": "askForDownloadLinkAgain",
                            "thread": None,
                        },
                        {
                            "dy_module": "vm.downloadLink",
                            "condition": "IsLinkValid",
                            "action": "download",
                            "else_action": "askForDownloadLinkAgain",
                            "thread": None,
                        },
                        {
                            "dy_module": "vm.afterDownloadMessage",
                            "condition": None,
                            "action": "showAfterDownloadMessage",
                            "else_action": None,
                            "thread": None,
                        },
                        {
                            "dy_module": "showAfterDownloadMessage",
                            "condition": None,
                            "action": "askForDownloadLink",
                            "else_action": None,
                            "thread": None,
                        },
                    ]
                }
            ]
        }

    def test_architecture_comparison(self):
        # Define the dictionary to be tested (replace with your actual dictionary)
        graph_dir = "D:/Users/Lahav/ProgramingProjects/FTV/FTV/Extra/Demos/Posts/Post 1/Upload Resources/"
        graph_path = graph_dir + "DownloadYoutubeSongsApp - Flow Chart.drawio"
        temp_path = graph_dir + "temp.drawio"

        data = read(graph_path)
        test_architecture = processGraph(data)

        # Iterate through the reference architecture and check keys and values
        self.assertDictEqual(self.ref_architecture, test_architecture)


if __name__ == '__main__':
    unittest.main()
