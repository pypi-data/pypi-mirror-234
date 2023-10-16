from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod


class VM(VariableManager):
    def setupVariables(self):
        self.domain = "http://www.example.com"
        self.post_message_format = "/login?username={}&password={}"
        self.usernames = []
        self.passwords = []

    def setupTriggers(self):
        pass


class LoginBrute(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        pass

    @DyMethod()
    def post(self):
        pass
