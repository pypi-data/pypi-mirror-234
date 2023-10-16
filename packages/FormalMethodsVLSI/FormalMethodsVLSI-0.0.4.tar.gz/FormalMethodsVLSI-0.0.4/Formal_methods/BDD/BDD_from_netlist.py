from functools import cached_property,reduce,lru_cache
import networkx as nx
from .netlist import *
from dd import BDD
import operator as op
from tqdm import tqdm
from typing import Union,Optional
from multipledispatch import dispatch

__all__ = ["BDD_from_netlist"]

class BDD_from_netlist(Netlist):
    def __init__(self,file,input_probabilities=None):
        super().__init__(file)
        self._bdd = BDD()
        self.table = dict()  # to save all the computed nets
        if not input_probabilities:
            # PI - primary-input
            self.prob = {PI: 0.5 for PI in self.inputs}
        else:
            self.prob = input_probabilities

    def __str__(self):
        return f"BDD for {repr(self.dag)}"

    def __repr__(self):
        return f"BDD_from_netlist({self.file})"

    @lru_cache(maxsize = 2**14)
    def probability(self,u):
        if not u.low : return 1 # leaf node?
        low, high = u.low, u.high 
        p = self.prob[u.var]
        if low.negated: # if low edge is complemented
            return ((1-self.probability(low))*(1-p) +
                    self.probability(high)*p)
        return (self.probability(low)*(1-p) +
                self.probability(high)*p)

    def __len__(self):
        if len(self._bdd) == 1:
            raise AssertionError(
                    "No BDD is built,call "
                    "`bdd.build` first")
        return len(self._bdd)

    @cached_property
    def cutnodes(self):
        G = self.dag
        return G.all_cutnodes(self.outputs)

    def build(self,find_prob = False,use_cutnodes = False,
              ordering = None):
        G = self.dag
        nodes_list = G.nodes
        And,Or,Xor = op.and_,op.or_,op.xor
        table = self.table
        bdd = self._bdd
        bdd.declare(*self.inputs) # declare primary inputs as variables
        bdd.configure(max_growth = 1.05)
        cutnodes = set()
        if use_cutnodes:
            cutnodes = self.cutnodes
            bdd.declare(*cutnodes)
        if ordering:
            bdd.configure(reordering = False)
            bdd.reorder(var_order = ordering)
        table.update({primary_input : bdd.var(primary_input)
                      for primary_input in self.inputs})

        # progress_bar = tqdm(nx.topological_sort(G),total = len(nodes_list))
        progress_bar = nx.topological_sort(G)
        for node in progress_bar:
            gate_type = nodes_list[node].get("type")
            if gate_type:
                output = node
                inputs = [table[net] for net in G.pred[node]]
                N = len(inputs)
                # description = italic_text(f"Finding probability of {output}")
                # progress_bar.set_description(description)
                if gate_type == "nand":
                    expr = ~reduce(And,inputs)
                elif gate_type == "nor":
                    expr = ~reduce(Or,inputs)
                elif gate_type == "and":
                    expr = reduce(And,inputs)
                elif gate_type == "or":
                    expr = reduce(Or,inputs)
                elif gate_type == "inv":
                    expr = ~inputs[0]
                elif gate_type == "buf":
                    expr = inputs[0]
                elif gate_type == "xor":
                    expr = reduce(Xor,inputs)
                elif gate_type == "xnor":
                    expr = ~reduce(Xor,inputs) 
                else:
                    raise TypeError(f"Invalid gate_type {gate_type} in netlist") 
                u = table[output] = expr
                # for `cudd` garbage collection is automatic
                # bdd.collect_garbage()
                if output in cutnodes:
                    del u
                    table[output] = bdd.var(output)

                if find_prob:
                    po = self.probability(u)
                    self.prob[output] = (1-po) if u.negated else po
                """
                # for checking whether probabilities are calculated correctly
                n = len(u.support) 
                SATcount = u.count()
                assert isclose(self.prob[output], SATcount/2**n)
                """
            else:
                continue
        # print(green_text("done"))

    @property
    def ordering(self):
        return self._bdd.var_levels
