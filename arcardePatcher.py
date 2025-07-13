import os, random, zipfile, shutil, plistlib, subprocess

tweakFolder = "/home/jonasb/Desktop/testtttt/tweaks"
if tweakFolder == "":
    input("please enter the folder path for all the bypass tweaks:\n")
    # ignore this if you hard coded your folder path in the "" above

input = input("enter folder or iPA path:\n")

if not input.endswith(".ipa"):
    iPA = [os.path.join(input, file) for file in os.listdir(input) if os.path.isfile(os.path.join(input, file)) and file.endswith(".ipa")]
    outputFolder = input
    print("[*] folder with iPA(s) detected")
else:
    iPA = input
    outputFolder = os.path.dirname(input)
    print("[*] single iPA detected")

print("[*] extracting iPA")
print(iPA)
iPATmp = os.mkdir(os.path.join(outputFolder, str(random.randint(100000, 999999))))
print(iPATmp)
with zipfile.ZipFile(iPA, "r") as zip:
    zip.extractall(iPATmp)

Payload = os.path.join(iPATmp, "Payload")

appDir = list(Payload.glob("*.app"))
if not appDir:
    shutil.rmtree(iPATmp)
    raise Exception("[!] no .app folder found")

print("[*] modifing Info.plist")

plist = os.path.join(appDir, "Info.plist")
if not plist:
    shutil.rmtree(iPATmp)
    raise Exception("[!] no Info.plist found")
   
with open(plist, "rb") as fp:
    pl = plistlib.load(fp)

pl["NSApplicationRequiresArcade"] = False

with open(plist, "wb") as fp:
    plistlib.dump(pl, fp)

print("[*] injecting tweaks")
patchedOutput = os.makedirs(os.path.join(outputFolder, "patched iPas"), exist_ok=True)
injectThis = [file for file in tweakFolder]
inject = ' '.join(['"' + item + '"' for item in injectThis])

cyanCmd = f"cyan -o {os.path.join(patchedOutput,os.path.basename(iPA))} -i {appDir} -f {inject} -c 9 -gqw"

subprocess.call(cyanCmd)

print("[*] deleting temp directory")
shutil.rmtree(iPATmp)
