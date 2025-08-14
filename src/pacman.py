import tarfile
from pathlib import Path
import subprocess

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
    def parse_output(self,output):
        packages=[]
        for line in output.splitlines():
            pkg={}
            if not line.strip():
                pkg={"NAME":pkgname,"VERSION":pkgversion,"DESCRIPTION":pkgdesc,"URL": pkgurl,}
                packages.append(pkg)
                continue
            key,sep,value=line.partition(":")
            key=key.strip()
            value=value.strip()
            if key=="Name":
                print(f"found pkg {value}")
                pkgname=value
            elif key=="Version":
                pkgversion=value
            elif key=="Description":
                pkgdesc=value
            elif key=="URL":
                pkgurl=value
        return packages
    def find_installed(self):
        aur=self.parse_output(subprocess.run(["pacman","-Qmi"],capture_output=True,text=True).stdout)
        pacman=self.parse_output(subprocess.run(["pacman","-Qei"],capture_output=True,text=True).stdout)
        merged=pacman+aur
        return merged
pac=PacmanHandler()

