import copy


class MethodContentPattern(object):
    def __init__(self, pattern: str, methods: list, classes: list=None, arguments=None):
        self.methods = methods
        self.pattern = pattern
        self.classes = classes
        self.arguments = arguments

    def getContent(self, class_name, method_name):
        content = "\n".join(list(map(lambda line: " "*8 + line, self.pattern.split("\n"))))
        if "{method}" in self.pattern and "{cls}" in self.pattern:
            content = content.format(cls=class_name, method=method_name)

        elif "{method}" in self.pattern and "{cls}" not in self.pattern:
            content = content.format(method=method_name)

        elif "{method}" not in self.pattern and "{cls}" in self.pattern:
            content = content.format(cls=class_name)

        return content

    def isClassAllowed(self, cls: str):
        if self.classes is not None:
            return cls in self.classes
        return True

    def areArgumentsExist(self):
        return self.arguments is not None

class IMethodContentPattern(MethodContentPattern):
    def __init__(self, *args, **kwargs):
        super(IMethodContentPattern, self).__init__(*args, **kwargs)
        self.iMethods = [m.replace("__", f"__i", 1) for m in self.methods]

class RMethodContentPattern(MethodContentPattern):
    def __init__(self, *args, **kwargs):
        super(RMethodContentPattern, self).__init__(*args, **kwargs)
        self.rMethods = [m.replace("__", f"__r", 1) for m in self.methods]

class FileString(dict):

    SEPARATOR = "%LAHAV%"

    def __init__(self, file_data: str, relevant_classes=None, file_hints_data: str=None, only_magic_methods = False):
        super(FileString, self).__init__()
        if relevant_classes is None:
            relevant_classes = []
        self.fileData = file_data
        self.newFileData = ""
        self.newFileString = None
        self.fileHintsData = file_hints_data

        self.classes = []
        self.classesNames = []
        self.methodsContentPatterns = []
        self.iMethodsContentPatterns = []
        self.rMethodsContentPatterns = []

        if relevant_classes is None:
            relevant_classes = []
        self.relevantClasses = relevant_classes

        self.only_magic_methods = only_magic_methods

        self.sliceFile()

    def sliceFile(self):
        self.__updateClasses()
        self.__updateClassesNames()

        for class_name in self.classesNames:
            self[class_name] = ClassString(self.getClass(class_name), only_magic_methods=self.only_magic_methods)

        self.newFileString = copy.copy(self)

    def joinFile(self):
        self.__updateMethodsContent()

        file_data = ""
        for cls in self:
            file_data += cls.joinClass() + "\n\n\n"

        return file_data.strip()

    def __updateMethodsContent(self):
        for cls in self:
            mew_i_methods = {}
            mew_r_methods = {}
            for method in cls:
                for iPat in self.iMethodsContentPatterns:
                    if iPat.isClassAllowed(cls.getOriginName()):
                        if method.getName() in iPat.methods:
                            i_method = copy.copy(method)
                            i_method.setName(method.getName().replace("__", "__i", 1))
                            i_method.setContent(iPat.getContent(cls.getOriginName(), method.getName()))
                            if iPat.areArgumentsExist():
                                method.setArguments(iPat.arguments)

                            mew_i_methods[i_method.getName()] = i_method

                for rPat in self.rMethodsContentPatterns:
                    if rPat.isClassAllowed(cls.getOriginName()):
                        if method.getName() in rPat.methods:
                            r_method = copy.copy(method)
                            r_method.setName(method.getName().replace("__", "__r", 1))
                            r_method.setContent(rPat.getContent(cls.getOriginName(), method.getName()))
                            if rPat.areArgumentsExist():
                                r_method.setArguments(rPat.arguments)

                            mew_r_methods[r_method.getName()] = r_method

                for pat in self.methodsContentPatterns:
                    if pat.isClassAllowed(cls.getOriginName()):
                        if method.getName() in pat.methods:
                            method.setContent(pat.getContent(cls.getOriginName(), method.getName()))
                            if pat.areArgumentsExist():
                                method.setArguments(pat.arguments)

            cls.update(mew_i_methods)
            cls.update(mew_r_methods)

    def getFileLines(self) -> [str]:
        return self.fileData.split("\n")

    def __updateClasses(self) -> [str]:
        classes: list = (self.SEPARATOR + "\nclass ").join(self.fileData.split("\nclass ")).split(self.SEPARATOR)[1::]
        classes[-1] = "\n".join(list(filter(lambda cls: cls.startswith("class ") or cls.startswith("    "), classes[-1].split("\n"))))
        classes = list(map(lambda cls: cls.strip(), classes))
        classes = list(filter(lambda cls: cls.replace("class ", "", 1).split("(", 1)[0].split(":", 1)[0] in self.relevantClasses, classes))
        self.classes = classes

    def __updateClassesNames(self) -> [str]:
        self.classesNames = list(map(lambda cls: cls.split("(", 1)[0].split("class ", 1)[-1].split(":", 1)[0], self.getClasses()))

    def getClassesNames(self):
        return self.classesNames

    def getClasses(self):
        return self.classes

    def getClass(self, class_name) -> str:
        return self.getClasses()[self.getClassesNames().index(class_name)]

    def replaceClassesNames(self, rep_dict):
        for old_class, new_class in rep_dict.items():
            self.newFileString[old_class].replaceName(new_class)

    def replaceClassParentsNames(self, rep_dict):
        for cls in self.newFileString:
            for old_parent, new_parent in rep_dict.items():
                cls.replaceParent(old_parent, new_parent)

    def addMethodsContent(self, content_pattern, methods_names, classes=None, arguments=None):
        for cls in self:
            cls.relevant_methods += methods_names

        self.methodsContentPatterns.append(MethodContentPattern(content_pattern, methods_names, classes=classes, arguments=arguments))

    def __addNewCharMethod(self, content_pattern, methods_names, char=""):
        for cls in self:
            for method in methods_names:
                if method in cls.getMethodsNames():
                    cls.relevant_methods += [method.replace("__", f"__{char}", 1)]

    def addNewIMethods(self, content_pattern, methods_names, classes=None, arguments=None):
        self.__addNewCharMethod(content_pattern, methods_names, "i")
        self.iMethodsContentPatterns.append(IMethodContentPattern(content_pattern, methods_names, classes=classes, arguments=arguments))

    def addNewRMethods(self,content_pattern, methods_names, classes=None, arguments=None):
        self.__addNewCharMethod(content_pattern, methods_names, "r")
        self.rMethodsContentPatterns.append(RMethodContentPattern(content_pattern, methods_names, classes=classes, arguments=arguments))

    def __iter__(self):
        return iter(map(lambda item: item[-1], self.items()))


class ClassString(dict):

    SEPARATOR = "%LAHAV%"
    METHOD_SEPARATOR = "%SHANI%"

    def __init__(self, class_data: str, relevant_methods: list = None, only_magic_methods = False):
        super(ClassString, self).__init__()
        self.classData = class_data

        self.name = None
        self.originName = None
        self.parents = []
        self.methods = []
        self.methodsNames = []
        self.decorators = {}

        if relevant_methods is None:
            relevant_methods = []
        self.relevant_methods = relevant_methods

        self.headerPattern_1 = "class {name}:"
        self.headerPattern_2 = "class {name}({parents}):"
        self.headerPattern = self.headerPattern_2

        self.only_magic_methods = only_magic_methods

        self.sliceClass()

    def sliceClass(self):
        self.__updateName()
        self.__updateParents()
        self.__updateMethods()
        self.__updateMethodsNames()

        for method_name in self.getMethodsNames():
            self[method_name] = MethodString(self.getMethod(method_name))
            # self[method_name].setClassName(self.getName())

    def joinClass(self):
        class_data = ""
        for method in self:
            if method.getName() in self.relevant_methods:
                if method.getName() in self.decorators.keys():
                    decorator = "    @" + self.getDecorator(method.getName()) + "\n"
                else:
                    decorator = ""

                class_data += decorator + method.joinMethod() + "\n\n"

        if not class_data:
            class_data = self.getHeader() + "\n    pass"
        else:
            class_data = self.getHeader() + "\n\n" + class_data

        return class_data.strip()

    def __isMagicMethod(self, method: str):
        return method.startswith("__") and method.endswith("__")

    def __updateMethods(self) -> [str]:
        class_data = self.classData.replace("\n    def ", self.METHOD_SEPARATOR + "\n    def ").replace("\n    @", self.METHOD_SEPARATOR + "\n    @")
        methods: list = class_data.split(self.METHOD_SEPARATOR)[1::]
        methods[-1] = "\n" + "\n".join(list(filter(lambda method: method.startswith("    def ") or method.startswith("        "), methods[-1].split("\n"))))

        k = 0
        while k < len(methods):
            method = methods[k]
            if method.strip().startswith("@"):
                decorator = method.strip().split(" ", 1)[0].replace("@", "")
                if k+1 < len(methods):
                    method_name = methods[k+1].split("(", 1)[0].split("def ", 1)[-1]
                    self.addDecorator(method_name, decorator)

            k += 1

        if self.only_magic_methods:
            methods = list(filter(lambda method: self.__isMagicMethod(method.split("(", 1)[0].split("def ", 1)[-1]), methods))

        methods = list(map(lambda method: "    " + method.strip(), methods))
        self.methods = methods

    def __updateMethodsNames(self) -> [str]:
        self.methodsNames = list(map(lambda method: method.split("(", 1)[0].split("def ", 1)[-1], self.getMethods()))

    def getMethods(self):
        return self.methods

    def getMethodsNames(self):
        return self.methodsNames

    def getMethod(self, method_name) -> str:
        return self.getMethods()[self.getMethodsNames().index(method_name)]

    def __updateName(self):
        self.originName = self.classData.split("\n", 1)[0].split("(", 1)[0].split(":", 1)[0].split("class ", 1)[-1]
        self.name = self.originName

    def __updateParents(self):
        if "):" not in self.classData.split("\n", 1)[0]:
            self.headerPattern = self.headerPattern_1
            return []

        self.parents = list(map(lambda arg: arg.strip(), self.classData.split("\n", 1)[0].split("#", 1)[0].split("(", 1)[-1].split(")", 1)[0].split(",")))

    def getName(self):
        return self.name

    def getOriginName(self):
        return self.originName

    def getParents(self):
        return self.parents

    def getHeader(self):
        if self.parents:
            header = self.headerPattern.format(name=self.name, parents=str((self.parents)).replace("\'", "")[1:-1:])
        else:
            header = self.headerPattern.format(name=self.name)

        return header

    def replaceName(self, name):
        self.name = name

    def replaceParent(self, old_parent, new_parent):
        if old_parent in self.parents:
            self.parents[self.parents.index(old_parent)] = new_parent

    def addDecorator(self, method_name, decorator):
        self.decorators[method_name] = decorator

    def getDecorator(self, method_name):
        return self.decorators[method_name]

    def __iter__(self):
        return iter(self.values())

    # def __repr__(self):
    #     return self.classData


class MethodString(str):
    def __init__(self, method_data: str):
        super(MethodString, self).__init__()
        self.methodData = method_data
        self.className = None

        self.name = None
        self.arguments = []

        self.headerPattern_1 = "def {name}({arguments}):"
        self.headerPattern = self.headerPattern_1
        self.content = None

        self.setupMethod()

    def setupMethod(self):
        self.__updateName()
        self.__updateArguments()
        self.__updateContent()

    def joinMethod(self):
        method_data = self.getHeader() + "\n" + self.content

        return "    " + method_data.strip()

    def __updateName(self):
        self.name = self.split("(", 1)[0].split("def ", 1)[-1]

    def __updateArguments(self):
        self.arguments = list(map(lambda arg: arg.strip(), self.split("\n", 1)[0].split("#", 1)[0].split("(", 1)[-1].rsplit(")", 1)[0].replace("\'", "\"").split(",")))

    def __updateContent(self):
        self.content = self.methodData.split("\n", 1)[-1]

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getArguments(self):
        return self.arguments

    def setArguments(self, arguments):
        self.arguments = arguments

    def setContent(self, content: str):
        self.content = content

    def getContent(self):
        return self.content

    def isArgumentExist(self, arg_name):
        return arg_name in self.getArguments()

    def areArgumentsExist(self, *arg_names):
        return bool(set(self.getArguments()) & set(arg_names))

    def areAllArgumentsExist(self, *arg_names):
        return not bool(set(self.getArguments()) - set(arg_names))

    def getHeader(self):
        return self.headerPattern.format(name=self.name, arguments=str(self.arguments).replace("\'", "")[1:-1:])

    def setClassName(self, class_name):
        self.className = class_name

    def getClassName(self):
        return self.className

    # def __repr__(self):
    #     return self.methodData


class FileReader(object):
    def __init__(self, file_path: str, new_file_path: str, demo_file_path: str):
        self.filePath = file_path
        self.newFilePath = new_file_path
        self.demoFilePath = demo_file_path

        self.fileData = self.readFile(self.filePath)
        self.fileDataLines = self.readFileLines(self.filePath)
        self.newFile = ""
        self.newFileLines = []

    @staticmethod
    def readFile(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def readFileLines(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    @staticmethod
    def saveFile(file_path, data: str, demo_file_path: str = None, demo_tag: str = None):
        if demo_file_path and demo_tag:
            demo_file_data = FileReader.readFile(demo_file_path)
        else:
            demo_file_data = ""
            demo_tag = "."

        with open(file_path, 'w+') as file:
            file.write(demo_file_data.replace(demo_tag, data))
