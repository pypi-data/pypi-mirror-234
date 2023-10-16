from BDD import BDD_from_netlist
from multiprocessing import Process
from pathlib import Path
from random import shuffle

p = Path("./tmpFiles.maxfo20/withGateSplit/")
files = list(p.iterdir())
shuffle(files)

print("Timed-out")

for file in files:
    bdd = BDD_from_netlist(file)
    try:
        process = Process(target = bdd.build)
        process.start()
    except Exception:
        # for now only show timed-out files
        continue
        print(str(file).split("/")[-1])
    finally:
        # set 1hr as timed out for BDDs
        process.join(3600)
    if process.is_alive():
        print(str(file).split("/")[-1])
        process.terminate()
        process.join()

