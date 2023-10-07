import sys, os, pathlib, traceback, subprocess
import asyncio
import openiap
import zipfile, shutil, gzip, tarfile
from openiap.client import GracefulKiller

def getpackagepath(packagepath, first=True):
    if os.path.isfile( os.path.join(packagepath, "agent.py")): return packagepath
    if os.path.isfile( os.path.join(packagepath, "main.py")): return packagepath
    if os.path.isfile( os.path.join(packagepath, "index.py")): return packagepath
    if(not first): return ""
    if not os.path.exists(packagepath): return ""
    files = os.listdir(packagepath)
    for file in files:
        dir = os.path.join(packagepath, file)
        if not os.path.isfile(dir):
            result = getpackagepath(dir, False)
            if(result != ""): return result
    return ""
def getscriptpath(packagepath):
    if os.path.isfile( os.path.join(packagepath, "agent.py")): return os.path.join("agent.py")
    if os.path.isfile( os.path.join(packagepath, "main.py")): return os.path.join( "main.py")
    if os.path.isfile( os.path.join(packagepath, "index.py")): return os.path.join("index.py")
    return ""
def gitclone(url):
    directory = "package"
    if not os.path.exists(directory):
        print(f"Cloning {url}")
        subprocess.run(["git", "clone", "--recursive", url, directory])
    return directory
def pipinstall(packagepath):
    if os.path.isfile( os.path.join(packagepath, "requirements.txt")):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(packagepath, "requirements.txt")])
def runit(packagepath,command):
    os.chdir(packagepath)
    SKIP_XVFB = os.environ.get("SKIP_XVFB", "")
    try:
        if(SKIP_XVFB==""):
            #os.environ["DISPLAY"]=":99"
            commandarray = [
                "/usr/bin/xvfb-run",
                "-e", "/tmp/xvfb.log",
                f'--server-args=-screen 0 1920x1080x24 -ac',
                sys.executable, command
            ]
            command = " ".join(commandarray)
            print("Run " + command)
            subprocess.run(commandarray)
        else:
            print("Run " + command)
            subprocess.run([sys.executable, command])
    except Exception as e:
        if os.path.isfile( "/tmp/xvfb.log"):
            print("****************** xvfb.log")
            with open("/tmp/xvfb.log", "r") as file:
                content = file.read()
                print(content)
        print("***************************")
        print("runit EXCEPTION!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)
async def getpackage(fileid):
    directory = "package"
    c = openiap.Client()
    await c.Signin()
    result = await c.DownloadFile(Id=fileid)
    # c.Close()
    if(result.filename == ""):
        raise ValueError("Filename missing or not found")
    if(pathlib.Path(result.filename).suffix == ".zip"):
        with zipfile.ZipFile(result.filename, 'r') as zip_ref:
            zip_ref.extractall(directory)
        os.remove(result.filename)
    elif(pathlib.Path(result.filename).suffix == ".gz"):
        gunzip_shutil(result.filename, directory)
        os.remove(result.filename)
    elif(pathlib.Path(result.filename).suffix == ".tgz"):
        with tarfile.open(result.filename, "r:gz") as tar:
            tar.extractall(path=directory)
        os.remove(result.filename)
    else:
        shutil.copyfile(result.filename, os.path.join(directory, result.filename))
        os.remove(result.filename)
    return directory
async def getpackagefrom(packageid):
    directory = "package"
    c = openiap.Client()
    await c.Signin()
    pack = await c.Query("agents", {"_id": packageid, "_type": "package"})
    if(len(pack) == 0):
        raise ValueError("Package not found")
    fileid = pack[0]["fileid"]
    result = await c.DownloadFile(Id=fileid)
    # c.Close()
    if(result.filename == ""):
        raise ValueError("Filename missing or not found")
    if(pathlib.Path(result.filename).suffix == ".zip"):
        with zipfile.ZipFile(result.filename, 'r') as zip_ref:
            zip_ref.extractall(directory)
        os.remove(result.filename)
    elif(pathlib.Path(result.filename).suffix == ".gz"):
        gunzip_shutil(result.filename, directory)
        os.remove(result.filename)
    elif(pathlib.Path(result.filename).suffix == ".tgz"):
        with tarfile.open(result.filename, "r:gz") as tar:
            tar.extractall(path=directory)
        os.remove(result.filename)
    else:
        shutil.copyfile(result.filename, os.path.join(directory, result.filename))
        os.remove(result.filename)
    return directory
if __name__ == '__main__':
    print(f"Python version {sys.version} {sys.version_info}")
    killer = GracefulKiller()
    packagepath = os.environ.get("packagepath", "")
    fileid = os.environ.get("fileid", "")
    packageid = os.environ.get("packageid", "")
    gitrepo = os.environ.get("gitrepo", "")
    
    if(gitrepo != ""):
        packagepath = gitclone(gitrepo)
    if(packageid != ""):
        packagepath = asyncio.run(getpackagefrom(packageid))
    if(fileid != ""):
        packagepath = asyncio.run(getpackage(fileid))
    packagepath = getpackagepath(packagepath)
    if(packagepath == ""):
        sys.exit(f"packagepath not found, EXIT!")
    command = getscriptpath(packagepath)
    if command == "":
        sys.exit(f"Failed locating a command to run, EXIT!")
    pipinstall(packagepath)
    runit(packagepath, command)
