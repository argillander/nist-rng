from subprocess import check_output, CalledProcessError
import argparse
import sys
import glob

class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


parser = argparse.ArgumentParser()
parser.add_argument("-if", "--folder",nargs='?',default=None, help="read all files in folder")
parser.add_argument("-nc", "--no-color",default=False, action="store_true", help="colorless output")
args, unknown = parser.parse_known_args()

delta_ent = 5

use_color = not args.no_color

#print("USE_COLOR: ", use_color)
def printgreen(s):
    if use_color:
        print(col.OKGREEN + s + col.ENDC)
    else:
        print(s)

def printOK(s):
    if use_color:
        print(col.OKGREEN + "PASS: " + col.ENDC + s )
    else:
        print("PASS: ", s)

def printFAIL(s):
    if use_color:
        print(col.FAIL + "FAIL: " + col.ENDC + s )
    else:
        print("FAIL: ", s)
    
def printWARN(s):
    if use_color:
        print(col.WARNING + "WARN: " + col.ENDC + s )
    else:
        print("WARN: ", s)
    
def in_delta_range(thresh, delta, val):
    return (val > thresh-delta) and (val < thresh+delta)


def run_entropy(filename):
    cmd = "ent -t {filename}".format(filename=filename)
    out = ""
    try:
        out = check_output(cmd.split(" ")).decode("utf8")
    except CalledProcessError:
        printWARN("File [" + filename +"] not available. Skipping file...")
        return None
        
    lines = out.split("\n")
    dline = lines[1].split(",")
    return {"entropy": float(dline[2]), "chi-square": float(dline[3]), "mean": float(dline[4]), "monte-carlo-pi": float(dline[5]), "serial-correlation": float(dline[6])}


def run_entropy_tests(files):
    print("============ Running preliminary RNG test ============")
    print("")
    numfail= 0
    numpass = 0
    for s in files:
        stat = run_entropy(s)
        if stat == None:
            continue
        mean = stat["mean"]
        if in_delta_range(127.5, 5, mean):
            printOK("Entropy test passed (" + str(mean) + ") within bound 127.5 +-5 for file: " + str(s))
            numpass +=1
        else:
            printFAIL("Entropy test failed (" + str(mean) + ") outside bound 127.5 +-5 for file: "+ str(s))
            numfail += 1

    print("\n{}/{} tests passed".format(numpass, numpass+numfail))
    print("============     All entropy tests run     ============")



if __name__ == "__main__":
    all_files =  unknown

    if args.folder:

        all_files = glob.glob(args.folder + "/*.rnd")
        #run_entropy_tests(["rand1", "rand2", "rand3", "rand4", "rand5"])
    run_entropy_tests(all_files)
