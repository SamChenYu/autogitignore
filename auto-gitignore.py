import os
import sys
from pathlib import Path


args = sys.argv

cwd = os.getcwd()
script_dir = Path(__file__).resolve().parent


langs = ["c++", "java", "python", "javascript", "unity"]
lang_files = {}
for lang in langs:
    dir = os.path.join(script_dir, "templates/" + lang, ".gitignore")
    if(os.path.exists(dir) and os.path.isfile(dir)):
        lang_files[lang] = dir
    else:
        print("Error: " + lang + " .gitignore file not found in " + dir)
        exit()

if (len(args) < 2) or (args[1] == "-h") or (args[1] == "--help"):
    print("Usage:")
    print("  auto-gitignore.py <language>...")
    print("Available languages:")
    for lang in langs:
        print("  --" + lang)
    exit()

if(len(args) == 2):
    # just copy the file to the current directory
    requested_lang = args[1][2:]
    gitignore_dir = lang_files.get(requested_lang)
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
        requested_lang = args[i][2:]
        gitignore_dir = lang_files.get(requested_lang)
        if gitignore_dir is None:
            print("Error: Language " + requested_lang + " not supported.")
            exit()
        with open(gitignore_dir, "r") as f:
            content += f.read() + "\n"
    with open(os.path.join(cwd, ".gitignore"), "w") as f:
        f.write(content)
    print("Successfully created .gitignore for " + ", ".join([args[i][2:] for i in range(1, len(args))]))
