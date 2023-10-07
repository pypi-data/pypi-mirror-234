import timeit

from FTV.Extra.Examples.BackgroundLoadingApp import App

features = {
    "Feature1": "Feature1",
    "Feature2": {
        "Feature2_1": "Feature2_1",
        "Feature2_2": "Feature2_2",
        "Feature2_3": "Feature2_3",
        "Feature2_4": "Feature2_4"
    },
    "Feature3": "Feature3",
}

def runFeatures(features, progress, weight):
    features_len = len(features)

    if isinstance(features, str):
        features = {features: features}

    for feature in features:
        temp_feature = features[feature]
        print(f"progress = {progress}: Main")
        print(f"-> FeaturesLoaderProgress.printProgress: MainUI")

        if isinstance(temp_feature, str):
            progress += weight/features_len
            print(f"\t{progress*100}%")
        else:
            runFeatures(temp_feature, progress, 1/features_len)

        print(f"<- FeaturesLoaderProgress.printProgress")

    progress += weight / features_len

def start():
    runFeatures(features, 0, 1)

# time_1 = timeit.Timer(start).timeit(10000)/10000
# print(time_1)

app = App.__new__(App)
App.runtime = timeit.Timer(app.__init__).timeit(1)
# print(time_1)

"""
settatter | MainUI : 0.0026 sec
MainUI : 0.0025 sec
settatter : 0.0026 sec
 : 0.0025 sec
 
Clean: 0.0000735 sec
"""
