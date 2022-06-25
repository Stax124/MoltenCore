import imp
import os

# Find all files ending with .py in folder models recursively
model_files: list[str] = []
for root, dirs, files in os.walk("models"):
    for file in files:
        if file.endswith(".py"):
            model_files.append(os.path.join(root, file))

print(model_files)

for i in model_files:
    print(i.replace("/", ".").replace("\\", ".").replace(".py", ""))
    imp.load_source(i.replace("/", ".").replace("\\", ".").replace(".py", ""), i)
