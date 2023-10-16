from .cutnodes import DAG
from tqdm import tqdm
import time
import os
import re
import argparse
from pathlib import Path

__all__ = ["Netlist","green_text","italic_text"]

class Netlist:
    def __init__(self,file=None,parse=True):
        if file:
            self.file = file
            self.dag = DAG()
            self.inputs = set()
            self.outputs = set()
            if parse:
                self.parse()

    def __str__(self):
        if self.__dict__.get("file"):
            return f"Netlist for {repr(self.dag)}"
        return "Netlist()"

    def __repr__(self):
        if self.__dict__.get("file"):
            return f"Netlist({self.file})"
        return "Netlist()"

    def __call__(self,file):
        return self.__init__(file)

    def parse(self): 
        G = self.dag
        with open(self.file,'r') as f:
            text = f.readlines()

        for line in text:
            tokens = line.split()
            *input_nets,output = [token.split(":")[1].strip("'")
                                  for token in tokens[2:]]
            gate = tokens[0]
            gate_type = gate[:-1] if gate[-1].isdigit() else gate

            for input_net in input_nets:
                G.add_edge(input_net,output)
            G.nodes[output]["type"] = gate_type

        for net in G.nodes:
            # no incoming edges?
            if not G.in_degree(net):
                self.inputs.add(net)
            # no outgoing edges?
            elif not G.out_degree(net):
                self.outputs.add(net)
            else:
                continue

    @classmethod
    def from_directory(cls,directory):
        # find all the netlists in the directory
        files = Path(directory).glob('*tmp_mod')
        # a list of `Netlist` objects for all the files in the
        # directory
        return [cls(file) for file in files] 

GREEN = '\033[92;1m'
END = '\033[0m'
ITALIC = '\033[3m'

green_text = lambda text : GREEN + text + END
italic_text = lambda text : ITALIC + text + END

if __name__=="__main__": 
    parser = argparse.ArgumentParser(
                       prog = "netlist_cutnodes",
                       description = "Find cutnodes of a DAG")
    
    parser.add_argument('--filename',default=False,
           help="netlist file - if directory is not given\
                file is assumed to be in current directory")
    
    parser.add_argument('--directory',default=False,
           help="directory in which netlist(s) is(are) present")
    args = parser.parse_args()
    
    filename = args.filename
    directory = args.directory
    
    if filename:
        if directory:
            file = os.path.join(directory,filename)
        else:
            cwd = os.getcwd()
            file = os.path.join(cwd,filename)
        try:
            netlists = Netlist(file)
        except:
            raise FileNotFoundError("netlist file does not exist")
    else:
        if directory:
            netlists = Netlist.from_directory(directory)
            if len(netlists) == 0:
                raise ValueError("Directory has no netlists")
        else:
            raise ValueError("no netlist(s) given")
    
    pattern = re.compile(".*/(\w*\d*)\.v")
    progress_bar = tqdm(netlists) if isinstance(netlists,list) else tqdm([netlists])
    file = open("netlist_cutnodes.txt",'w')
    
    for netlist in progress_bar:
        print(netlist.file)
        netlist_str=re.match(pattern,str(netlist.file)).group(1)
        description = italic_text(f"Finding cutnodes for {netlist_str}")
        progress_bar.set_description(description)
        G = netlist.dag
        outputs = netlist.outputs
        start = time.time()
        cutnodes = G.all_cutnodes(outputs)
        stop = time.time()
        file.write(f"cutnodes of {netlist_str}\n")
        file.write(f"elapsed time - {stop-start} seconds\n")
        file.write(f"No.of cutnodes={len(cutnodes)}\n")
        file.write(f"_"*50+"\n")
    
    print(green_text("done"))
    
    file.close() 
