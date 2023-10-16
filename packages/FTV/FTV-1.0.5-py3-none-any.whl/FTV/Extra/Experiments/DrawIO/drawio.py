import os
from pathlib import Path

from FTV.Extra.Examples.BIUAutomation.Tools.Files import Json

from bs4 import BeautifulSoup


def read(path):
    with open(path, 'r') as f:
        data = f.read()

    xml_data = BeautifulSoup(data, "lxml")
    return xml_data.find("diagram").find("root")


def processGraph(graph):
    ref_architecture = {
        "App": {
            "name": "DownloadYoutubeAudioFilesApp",
            "dy_variables": [
                "START"
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

    architecture = {
        "App": {},
        "Features": []
    }

    # Create components
    xml_components = [item for item in graph.find_all("mxcell") if "value" in item.attrs.keys()]
    components = []
    component_types = {
        "AppOrFeature": 'swimlane;strokeColor=#994C00;fillColor=#FF8000;fontSize=13;fontColor=#ffffff;rounded=1;shadow=0;swimlaneFillColor=#ffffff;glass=0;startSize=30;',
        "DyVariable": 'html=1;rounded=1;shadow=0;glass=0;comic=0;startSize=26;strokeColor=#6c8ebf;fillColor=#dae8fc;fontSize=13;fontStyle=1;swimlaneFillColor=#ffffff;arcSize=29;',
        "Method": 'html=1;rounded=1;shadow=0;glass=0;comic=0;startSize=26;strokeColor=#d79b00;fillColor=#ffe6cc;fontSize=13;fontStyle=1;swimlaneFillColor=#ffffff;arcSize=29;',
        "Condition": 'rhombus;whiteSpace=wrap;html=1;fontSize=13;fillColor=#FF9933;'
    }

    for xml_component in xml_components:
        _type = next((key for key, value in component_types.items() if value == xml_component["style"]), "__unknown__")
        name = xml_component["value"]
        parent_id = xml_component["parent"]
        _id = xml_component["id"]

        if _type == "DyVariable":
            name = f"vm.{name}"

        target_component = {
            "id": _id,
            "type": _type,
            "name": name,
            "parent_name": None,
            "parent_id": parent_id
        }

        components.append(target_component)

    # Add parent names
    for target_component in components:
        target_parent_name = next((item["name"] for item in components if item["id"] == target_component["parent_id"]), None)
        target_component["parent_name"] = target_parent_name

    # Create arrows
    xml_arrows = [item for item in graph.find_all("mxcell") if "source" in item.attrs.keys() and "target" in item.attrs.keys()]
    arrows = []
    arrow_types = {
        "Trigger": 'startFill=1;endFill=1;strokeColor=#9673a6;strokeWidth=2;fillColor=#e1d5e7;',
        "Action": 'strokeColor=#009900;',
        "ElseAction": 'strokeColor=#CC0000;',
        "RelatedVar": 'Arrow=diamondThin;endSize=12;'
    }
    for xml_arrow in xml_arrows:
        _type = next((key for key, value in arrow_types.items() if value in xml_arrow["style"]), "__unknown__")
        source_id = xml_arrow["source"]
        target_id = xml_arrow["target"]
        _id = xml_arrow["id"]

        arrow = {
            "type": _type,
            "source_id": source_id,
            "target_id": target_id,
            "source_full_name": None,
            "target_full_name": None,
        }

        arrows.append(arrow)

    # Add source and target names
    for arrow in arrows:
        source_item = next((item for item in components if item["id"] == arrow["source_id"]), None)
        source_name = source_item["name"]
        source_parent_name = source_item["parent_name"]
        source_full_name = f"{source_parent_name}.{source_name}"

        target_item = next((item for item in components if item["id"] == arrow["target_id"]), None)
        target_name = target_item["name"]
        target_parent_name = target_item["parent_name"]
        target_full_name = f"{target_parent_name}.{target_name}"

        arrow.update({
            "source_name": source_name,
            "target_name": target_name,
            "source_full_name": source_full_name,
            "target_full_name": target_full_name
        })

    # Add App
    app_name = next((item["name"] for item in components if item["type"] == "AppOrFeature" and item["parent_name"] is None), None)
    app_children = [item for item in components if item["parent_name"] == app_name]
    app_dy_variables = [item["name"] for item in app_children if item["type"] == "DyVariable"]
    app_methods = {item["name"].replace("()", ""): [] for item in app_children if item["type"] == "Method"}

    architecture["App"] = {
        "name": app_name,
        "dy_variables": app_dy_variables,
        "methods": app_methods,
        "triggers": []
    }

    # Add Features
    features = [item for item in components if item["type"] == "AppOrFeature" and item["parent_name"] is not None]

    for feature_item in features:
        feature_parent_name = feature_item["parent_name"]
        feature_name = feature_item["name"]
        feature_children = [item for item in components if item["parent_name"] == feature_name]
        feature_dy_variables = [item["name"] for item in feature_children if item["type"] == "DyVariable"]
        feature_methods = {item["name"].replace("()", ""): [] for item in feature_children if item["type"] == "Method"}
        feature = {
            "name": feature_name,
            "dy_variables": feature_dy_variables,
            "methods": feature_methods,
            "triggers": []
        }

        if feature_parent_name == app_name:
            architecture["Features"].append(feature)
        else:
            print("Please implement SubFeatures")

    # Add Methods

    # Add App Triggers
    app_conditions = [item["name"] for item in app_children if item["type"] == "Condition"]
    triggers = [item for item in arrows if item["type"] == "Trigger"]

    for trigger_item in triggers:
        source_id = trigger_item["source_id"]
        source_component = next(item for item in components if item["id"] == source_id)
        source_parent_name = source_component["parent_name"]

        target_id = trigger_item["target_id"]
        target_component = next(item for item in components if item["id"] == target_id)
        target_parent_name = target_component["parent_name"]

        if target_parent_name == architecture["App"]["name"]:
            source_name = trigger_item["source_name"].replace("()", "")
            target_name = trigger_item["target_name"].replace("()", "")

            trigger = {
                "dy_module": f"{source_parent_name}.{source_name}",
                "condition": None,
                "action": target_name,
                "else_action": None,
                "thread": None
            }  # TODO lahav Please apply the condition/action/else_action
            architecture["App"]["triggers"].append(trigger)

    # Add Feature Triggers
    features = architecture["Features"]
    feature_triggers = []

    for feature in features:
        for trigger_item in triggers:
            source_id = trigger_item["source_id"]
            source_component = next(item for item in components if item["id"] == source_id)
            source_parent_name = source_component["parent_name"]
            source_type = source_component["type"]

            target_id = trigger_item["target_id"]
            target_component = next(item for item in components if item["id"] == target_id)
            target_parent_name = target_component["parent_name"]
            target_type = target_component["type"]

            source_name = trigger_item["source_name"].replace("()", "")
            target_name = trigger_item["target_name"].replace("()", "")

            condition_name = None
            else_action_name = None
            action_name = target_name

            if target_type == "Condition":
                action_arrows = [item for item in arrows if item["type"] == "Action"]
                else_action_arrows = [item for item in arrows if item["type"] == "ElseAction"]

                action_component = next(item for item in action_arrows if item["source_name"] == target_name)
                else_action_component = next(item for item in else_action_arrows if item["source_name"] == target_name)

                condition_name = target_name
                action_name = action_component["target_name"]
                else_action_name = else_action_component["target_name"]

            if source_parent_name != feature["name"]:
                dy_module_name = f"{source_parent_name}.{source_name}"
            else:
                dy_module_name = source_name

            trigger = {
                "dy_module": dy_module_name,
                "condition": condition_name,
                "action": action_name,
                "else_action": else_action_name,
                "thread": None
            }  # TODO lahav Please apply the condition/action/else_action
            feature_triggers.append(trigger)

        feature["triggers"] = feature_triggers

        methods = feature["methods"]
        for method, related_vars in methods.items():
            related_var_arrows = [item for item in arrows if item["type"] == "RelatedVar" and item["source_name"].replace("()", "") == method]

            for arrow in related_var_arrows:
                related_var = arrow["target_name"]
                related_vars.append(related_var)

    return architecture


def generateCode(architecture, path):
    # Create project folder
    app_name = architecture["App"]["name"]
    app_dir = f"{path}{app_name}/"
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)

    # Create Main.py file
    main_file_path = app_dir_path / "Main.py"
    with main_file_path.open(mode="w") as main_file:
        main_file.write(
f"""from {app_name}.App import App

App()
"""
        )

    # Create App file
    app_file_path = app_dir_path / "App.py"
    with app_file_path.open(mode="w") as app_file:
        app_file.write(
f"""
from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicObjects import DyInt


class VM(VariableManager):
    def setupVariables(self):
        self.tenth_seconds = DyInt(0)
        self.seconds = DyInt(0)
        self.minutes = DyInt(0)
        self.hours = DyInt(0)

    def setupTriggers(self):
        pass


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.DyClockExample.Features.IntegratedClock import IntegratedClock
        from FTV.Extra.Examples.DyClockExample.Features.VisualClock import VisualClock

        self.addFeature(IntegratedClock)
        self.addFeature(VisualClock)


class ClockApp(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)
        self.setVariableManager(VM)

"""
        )

    # Create init file
    init_file_path = app_dir_path / "__init__.py"
    init_file_path.touch()

    # Create Features folder
    features_dir = app_dir_path / "Features"
    features_dir.mkdir(exist_ok=True)

    # Create Features files (empty classes)
    for feature in architecture.get("Features", []):
        feature_name = feature.get("name", "UnnamedFeature")
        feature_file_path = features_dir / f"{feature_name}.py"
        with feature_file_path.open(mode="w") as feature_file:
            feature_file.write(f"# {feature_name}.py - Your feature-specific logic goes here")


if __name__ == '__main__':
    graph_dir = "D:/Users/Lahav/ProgramingProjects/FTV/FTV/Extra/Demos/Posts/Post 1/Upload Resources/"
    graph_path = graph_dir + "DownloadYoutubeSongsApp - Flow Chart.drawio"
    temp_path = graph_dir + "temp.drawio"

    data = read(graph_path)
    architecture = processGraph(data)
    Json.print(architecture)
    
    path = "D:/Users/Lahav/ProgramingProjects/FTV/"
    generateCode(architecture, path)
