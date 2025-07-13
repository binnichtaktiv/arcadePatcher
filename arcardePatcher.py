import os, random, zipfile, shutil, plistlib, subprocess

count = 0

tweakFolder = ""
if tweakFolder == "":
    input("please enter the folder path for all the bypass tweaks:\n")
    # ignore this if you hard coded your folder path in the "" above

uinput = input("enter folder or iPA path:\n")
output = input("enter output path (leave it empty if you want it in the same path as input iPA/folder):\n")
if output == None:
    if uinput.endswith(".ipa"):
        output = os.path.dirname(uinput)
    else:
        output = uinput

if not uinput.endswith(".ipa"):
    iPA = [os.path.join(uinput, file) for file in os.listdir(uinput) if os.path.isfile(os.path.join(uinput, file)) and file.endswith(".ipa")]
    print("[*] folder with iPA(s) detected")
else:
    iPA = [uinput]
    print("[*] single iPA detected")

for entry in iPA:
    print("[*] extracting iPA")
    iPATmp = os.path.join(output, str(random.randint(100000, 999999)))
    os.mkdir(iPATmp)

    with zipfile.ZipFile(entry, "r") as zip:
        zip.extractall(iPATmp)

    Payload = os.path.join(iPATmp, "Payload")
    appDir = [os.path.join(Payload, f) for f in os.listdir(Payload) if f.endswith(".app") and os.path.isdir(os.path.join(Payload, f))]
    if not appDir:
        shutil.rmtree(iPATmp)
        raise Exception("[!] no .app folder found")

    print("[*] modifing Info.plist")

    plist = os.path.join(appDir[0], "Info.plist")
    if not plist:
        shutil.rmtree(iPATmp)
        raise Exception("[!] no Info.plist found")
    
    with open(plist, "rb") as fp:
        pl = plistlib.load(fp)

    pl["NSApplicationRequiresArcade"] = False

    with open(plist, "wb") as fp:
        plistlib.dump(pl, fp)

    print("[*] injecting tweaks")

    patchedOutput = os.path.join(output, "patched iPas")
    os.makedirs(patchedOutput, exist_ok=True)

    inject = ['"' + os.path.join(tweakFolder, file) + '"' for file in os.listdir(tweakFolder)]

    cyanCmd = f"cyan -o '{os.path.join(patchedOutput,os.path.basename(entry[:-4] + "_patched.ipa"))}' -i '{appDir[0]}' -f {' '.join(inject)} -c 9 -gqw"

    subprocess.call(cyanCmd, shell=True)

    shutil.rmtree(iPATmp)

    if len(iPA) > 1:
        count+=1
        print(f"[*] app {count} of {len(iPA)} done\n")
