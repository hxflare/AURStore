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
                found={}
                for package in tar.getmembers():
                    if package.name.endswith("/desc"):
                        extracted=tar.extractfile(package)
                        if extracted:
                            content=extracted.read().decode("utf-8",errors="replace").splitlines()
                            pkgname=None
                            pkgdesc=None
                            for i, line in enumerate(content):
                                if line=="%NAME%":
                                    pkgname=content[i+1]
                                if line=="%DESC%":
                                    pkgdesc=content[i+1]
                            if query.lower() in pkgname.lower():
                                print(f"name: {pkgname}\n \ndescription: \n{pkgdesc}\n\n")
pac=PacmanHandler()
pac.search_db(input("you are searching for: "))