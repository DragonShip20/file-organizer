import os, shutil

GROUPS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".odt", ".rtf"},
    "Archives": {".zip", ".tar", ".gz", ".tgz", ".rar", ".7z"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".wmv"},
    "Code": {".py", ".js", ".java", ".c", ".cpp", ".cs", ".rb", ".go", ".rs"},
}

def match_ext(ext: str) -> str:
    ext = ext.lower()
    for group, exts in GROUPS.items():
        if ext in exts:
            return group
    return ext.lstrip('.') or "NoExt"

def sortfiles(folder: str) -> None:
    for name in os.listdir(folder):
        src = os.path.join(folder, name)
        if not os.path.isfile(src):
            continue
        ext = os.path.splitext(name)[1]
        group = match_ext(ext)
        dest = os.path.join(folder, group)
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
        path = os.path.join(dest, name)
        print(f"{name} -> {os.path.relpath(path, folder)}")
        shutil.copy2(src, path)

if __name__ == "__main__":
    filepath = input("Input folder path: ")
    sortfiles(filepath)