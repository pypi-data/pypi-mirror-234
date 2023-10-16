# FTV

The purpose of the project is to make programming modular, well-structured, and user-friendly. It
enables shorter development and debugging time, a coherent code, an option of combining
programs written by different authors, and a flexible code structure for changes. (Python, C++)

More information will be out once with the first release is aired.

## Suggested Examples
Under Examples directory

### Modules
- DyWifiExample.py - demonstrates simple flow in a custom dynamic module.
- DyVarsExample.py - demonstrates multiple dynamic variable types and their triggers.
- DyIntExample.py - demonstrates dynamic int triggers.
- DyBoolListExample.py - demonstrates dynamic boolean trees. It is quite obvious from the example.

### Apps (without UI)
- DownloadFileFeature.py - great example with multiple use-cases. (this is the only example by far which I also created a corresponding visual flowchart)
- DyClockExample/Main.py - Example clock app with a timer feature. Notice that the clock app has two features. One is the integrated clock which runs the functionality and the over is the visual representation.
    If you disable one of them the other one is still active and ready to affect (or be affected) by other features.
    For example, here you can disable the VisualClock feature:
    ```class VisualClock(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()```
- Algorithms/Main.py - Very similar to the clock app. An algorithm runs on a dedicated thread and the update progressbar function is runs on a UI thread.
