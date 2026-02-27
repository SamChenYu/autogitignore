import os
import sys
from pathlib import Path

args = sys.argv

cwd = os.getcwd()
script_dir = Path(__file__).resolve().parent

langs = ["c++", "java", "python", "javascript", "unity"]
langs_extensions = {
    "c++": [".cpp", ".h", ".hpp", ".c"],
    "java": [".java"],
    "python": [".py"],
    "javascript": [".js", ".jsx", ".ts", ".tsx"],
    "unity": [".cs", ".unity", ".prefab"]
}
ignore_templates = {}
for lang in langs:
    # init the ignore_templates dictionary with the path to the .gitignore template for each language
    dir = os.path.join(script_dir, "templates/" + lang, ".gitignore")
    if(os.path.exists(dir) and os.path.isfile(dir)):
        ignore_templates[lang] = dir
    else:
        print("Error: " + lang + " .gitignore file not found in " + dir)
        exit()
# abbreviations
ignore_templates["js"] = ignore_templates["javascript"]
ignore_templates["typescript"] = ignore_templates["javascript"]
ignore_templates["ts"] = ignore_templates["javascript"]

if(len(args) == 1):
    # auto detect the language by looking for files in the current directory
    content = ""
    found_langs = set()
    # find all files in the current directory and its subdirectories
    for root, dirs, files in os.walk(cwd):
        # Remove directories that should be ignored
        dirs[:] = [d for d in dirs if d not in ("node_modules", "vendor", "bin", "obj")]
        for file in files:
            file_ext = os.path.splitext(file)[1]
            for lang, extensions in langs_extensions.items():
                if file_ext in extensions:
                    gitignore_dir = ignore_templates.get(lang)
                    if gitignore_dir is not None:
                        with open(gitignore_dir, "r") as f:
                            content += f.read() + "\n"
                    found_langs.add(lang)    
                    break
    if content == "":
        print("No supported language files found in the current directory.")
        exit()
    with open(os.path.join(cwd, ".gitignore"), "w") as f:
        f.write(content)
    print("Successfully created .gitignore for the detected languages: " + ", ".join(found_langs))
    exit()  

if (args[1] == "-h") or (args[1] == "--help"):
    print("=== Auto Gitignore ===\n")
    print("Auto detect languages and create .gitignore:")
    print("  auto-gitignore.py\n")
    print("Specifed languages syntax:")
    print("  auto-gitignore.py <language>...\n")
    print("Available languages:")
    for lang in langs:
        print(" " + lang)
    exit()

if(len(args) == 2):
    # only one language, just write the content of the template to .gitignore
    requested_lang = args[1].lower()
    gitignore_dir = ignore_templates.get(requested_lang)
    if gitignore_dir is None:
        print("Error: Language " + requested_lang + " not supported.")
        exit()
    with open(gitignore_dir, "r") as f:
        content = f.read()
    with open(os.path.join(cwd, ".gitignore"), "w") as f:
        f.write(content)
    print("Successfully created .gitignore for " + requested_lang)


# multiple languages, just concatenate the files and write to .gitignore
else:
    content = ""
    for i in range(1, len(args)):
        requested_lang = args[i].lower()
        gitignore_dir = ignore_templates.get(requested_lang)
        if gitignore_dir is None:
            print("Error: Language " + requested_lang + " not supported.")
            exit()
        with open(gitignore_dir, "r") as f:
            content += f.read() + "\n"
    with open(os.path.join(cwd, ".gitignore"), "w") as f:
        f.write(content)
    print("Successfully created .gitignore for " + ", ".join([args[i][2:] for i in range(1, len(args))]))
