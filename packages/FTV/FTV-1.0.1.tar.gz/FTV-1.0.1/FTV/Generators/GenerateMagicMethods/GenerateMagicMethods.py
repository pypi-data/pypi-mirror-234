import os

from FTV.Generators import FileString, FileReader


builtins_file_name = "source/Builtins_3_7.py"
new_file_name = "result/MagicMethodsInterfaces.py"
demo_file_name = "source/MagicMethodsInterfacesDemo.py"

current_dir = os.getcwd().replace("\\", "/") + "/"

builtins_file_path = current_dir + builtins_file_name
new_file_path = current_dir + new_file_name
demo_file_path = current_dir + demo_file_name

# Create the file reader
fileReader = FileReader(builtins_file_path, new_file_name, demo_file_name)

# Create variables
builtin_objects = {
    "object":"DyObject",
    "int":"DyInt",
    "float":"DyFloat",
    "bool":"DyBool",
    "str":"DyStr",
    "list":"DyList",
    "set":"DySet",
    "dict":"DyDict",
    "tuple":"DyTuple",
    "complex":"DyComplex",
    "bytes":"DyBytes",
    "bytearray":"DyByteArray"
}

for key in builtin_objects.keys():
    builtin_objects[key] += "MagicMethods"

numeric_objects = [
    "int",
    "float",
    "bool"
]

string_objects = [
    "str"
]

iterator_objects = [
    "list",
    "set",
    "dict",
    "tuple",
    "bytearray"
]

other_objects = [
    "complex",
    "bytes",
    "object"
]

compare_methods = [
    "__eq__",
    "__ne__",
    "__ge__",
    "__le__",
    "__gt__",
    "__lt__",
    "__contains__"
]

single_math_methods = [
    "__neg__",  # ???
    "__pos__",  # ???
    "__trunc__",
    "__round__",
    "__ceil__",
    "__floor__",
    "__abs__"
]

dual_math_methods = [
    "__add__",
    "__sub__",
    "__mul__",
    "__floordiv__",
    "__truediv__",
    "__divmod__",
    "__pow__",
    "__mod__",
    "__lshift__",
    "__rshift__",
    "__and__",
    "__or__",
    "__xor__"
]

r_dual_math_methods = dual_math_methods

i_dual_math_methods = dual_math_methods.copy()
i_dual_math_methods.remove("__divmod__")

string_methods = [
    "__repr__",
    "__str__",
    "__format__"
]

type_methods = [
    "__bool__",
    "__int__",
    "__float__"
]

iterator_methods = [
    "__index__",
    "__invert__",
    "__reversed__",
    "__iter__",
    "__len__"
]

# Create the file reader (include filtering)
fileString = FileString(fileReader.fileData, list(builtin_objects), only_magic_methods=True)

# Replace objects' names
fileString.replaceClassesNames(builtin_objects)
fileString.replaceClassParentsNames(builtin_objects)

for obj in iterator_objects + other_objects:
    fileString.addMethodsContent(
        f"if isinstance(args[0], DyObject):\n"
        f"    return {'{'}cls{'}'}.{'{'}method{'}'}(self.get(), args[0].get(), **kwargs)\n"
        f"else:\n"
        f"    return {'{'}cls{'}'}.{'{'}method{'}'}(self.get(), *args, **kwargs)",
        dual_math_methods + compare_methods, classes=[obj]
    )
    fileString.addNewIMethods(
        f"if isinstance(args[0], DyObject):\n"
        f"    self.set({'{'}cls{'}'}.{'{'}method{'}'}(self.get(), args[0].get(), **kwargs))\n"
        f"else:\n"
        f"    self.set({'{'}cls{'}'}.{'{'}method{'}'}(self.get(), *args, **kwargs))\n"
        f"return self",
        i_dual_math_methods, classes=[obj]
    )
    fileString.addNewRMethods(
        f"return int(*args, **kwargs)",
        r_dual_math_methods, classes=[obj]
    )

for obj in numeric_objects + string_objects:
    fileString.addMethodsContent(
        f"return {'{'}cls{'}'}.{'{'}method{'}'}(self.get(), args[0].__{obj}__(), **kwargs)",
        dual_math_methods + compare_methods, classes=[obj]
    )
    fileString.addNewIMethods(
        f"self.set({'{'}cls{'}'}.{'{'}method{'}'}(self.get(), args[0].__{obj}__(), **kwargs))\n"
        "return self",
        i_dual_math_methods, classes=[obj]
    )
    fileString.addNewRMethods(
        f"return args[0].__{obj}__()",
        r_dual_math_methods, classes=[obj]
    )

fileString.addMethodsContent(
    "return {cls}.{method}(self.get(), *args, **kwargs)",
    string_methods + type_methods + iterator_methods + single_math_methods
)

### Exceptions

fileString.addMethodsContent(
    "return {cls}.{method}(self.get(), *args, **kwargs)",
    ["__format__"], classes=["complex"], arguments=["self", "*args", "**kwargs"]
)

fileString.addMethodsContent(
    f"if isinstance(y, DyObject):\n"
    f"    return {'{'}cls{'}'}.{'{'}method{'}'}(self.get(), y.get())\n"
    f"else:\n"
    f"    return {'{'}cls{'}'}.{'{'}method{'}'}(self.get(), y)",
    ["__contains__"], classes=["set"], arguments=["self", "y"]
)

fileData = fileString.newFileString.joinFile()
fileReader.saveFile(new_file_name, fileData, demo_file_path, "### CONTENT")
print(fileData)
