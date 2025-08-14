import tarfile
from pathlib import Path

class PacmanHandler():
    def __init__(self):
        self.paths=[
            Path("/var/lib/pacman/sync/core.db"),
            Path("/var/lib/pacman/sync/extra.db")
        ]
    def search_db(self,query="ll"):
        for path in self.paths:
            with tarfile.open(path,"r:gz") as tar:
                found=[]
                for package in tar.getmembers():
                    if package.name.endswith("/desc"):
                        extracted=tar.extractfile(package)
                        if extracted:
                            content=extracted.read().decode("utf-8",errors="replace").splitlines()
                            pkgname=None
                            pkgdesc=None
                            pkgversion=None
                            pkgurl=None
                            for i, line in enumerate(content):
                                if line=="%NAME%":
                                    pkgname=content[i+1]
                                elif line=="%DESC%":
                                    pkgdesc=content[i+1]
                                elif line=="%VERSION%":
                                    pkgversion=content[i+1]
                                elif line=="%URL%":
                                    pkgurl=content[i+1]
                            if query.lower() in pkgname.lower():
                                found.append({"NAME":pkgname,"DESC":pkgdesc, "VERSION":pkgversion,"URL": pkgurl,"UNPARSED":content})
        return found
"""
pac=PacmanHandler()
result=pac.search_db(input("you are searching for: "))
print("\n\n")
for i in result:
    print(f"Name: {i["NAME"]}-{i["VERSION"]}\n\nDescription:\n{i["DESC"]}\n\nURL: {i["URL"]}\n\n")
"""