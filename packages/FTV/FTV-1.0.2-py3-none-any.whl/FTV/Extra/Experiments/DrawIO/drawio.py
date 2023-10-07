from FTV.Extra.Examples.BIUAutomation.Tools.Files import Json

from bs4 import BeautifulSoup


def read(path):
    with open(path, 'r') as f:
        data = f.read()

    xml_data = BeautifulSoup(data)
    return xml_data.find("diagram").find("root")


def processGraph(graph):
    ref_architecture = {
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

        component = {
            "id": _id,
            "type": _type,
            "name": name,
            "parent_name": None,
            "parent_id": parent_id
        }

        components.append(component)

    # Add parent names
    for component in components:
        parent_name = next((item["name"] for item in components if item["id"] == component["parent_id"]), None)
        component["parent_name"] = parent_name

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

    # for trigger_item in triggers:
    #     trigger = {
    #         "dy_module": "DownloadYoutubeAudioFilesApp.vm.START",
    #         "condition": None,
    #         "action": "showIntro",
    #         "else_action": None,
    #         "thread": None,
    #     }
    #     architecture["App"]["triggers"].append(trigger)

    # # Add Feature Triggers
    # app_conditions = [item["name"] for item in app_children if item["type"] == "Condition"]

    return architecture


def write(path, data):
    pass


if __name__ == '__main__':
    graph_dir = "D:/Users/Lahav/ProgramingProjects/FTV/Demos/Posts/Post 1/Upload Resources/"
    graph_path = graph_dir + "DownloadYoutubeSongsApp - Flow Chart.drawio"
    temp_path = graph_dir + "temp.drawio"

    data = read(graph_path)
    architecture = processGraph(data)
    Json.print(architecture)
