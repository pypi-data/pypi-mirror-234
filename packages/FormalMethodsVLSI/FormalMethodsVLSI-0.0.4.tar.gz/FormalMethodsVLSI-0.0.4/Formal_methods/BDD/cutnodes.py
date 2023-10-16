import networkx as nx
from collections import deque

__all__ = ["DAG"]

class DAG(nx.DiGraph):
    """ `nx.DiGraph` class is parent class of `DAG`
    class.It inherits the attributes and methods of
    `nx.DiGraph` class. Usage of `DAG` is similar  
    to that of `nx.DiGraph` """
    def __init__(self,nodes=None):
        super().__init__(nodes)

    def __repr__(self):
        return f"DAG with {len(self.nodes)} nodes"\
               f" and {len(self.edges)} edges"

    def add_edge(self,u,v,**attr):
        super().add_edge(u,v,**attr)

    def add_edges_from(self,edges, **attr):
        super().add_edges_from(edges, **attr)

    def all_cutnodes(self,outputs):
        """To get all the cutnodes for all the subgraphs formed by
        ancestors of outputs. All such subgraphs of outputs together 
        give the original DAG"""
        cutnodes = set()
        for output in outputs:
            ancestors = nx.ancestors(self,output)|{output}
            subgraph = self.subgraph(ancestors)
            cutnodes.update(subgraph.Cutnodes(output))
        return cutnodes

    # cutnodes of the graph using the dominance algorithm
    def Cutnodes(self,output=None):
      cutnodes = set()
      flow_graph = nx.DiGraph()
      queue = deque()
      flow_graph.add_edges_from(self.edges)
      queue.append(output)
      # flow_graph.remove_node(output)
      #Make all edges of the flow graph bi-directional
      for u,v in flow_graph.edges:
        flow_graph.add_edge(v,u)
      """except for  the edges incident on the output 
      gate, reverse the direction of edges incident on 
      output gate
      """
      nets = [net for net in flow_graph.pred[output]]
      for net in nets:
          flow_graph.remove_edge(net,output)
      # find `immediate dominators` of each node for 
      # the `flow graph`
      idom = nx.immediate_dominators(flow_graph,output)
      # remove output as it its immediate dominator is itself
      del idom[output]
      """each node is a child of `immediate dominator`
      in the `dominator tree`"""
      dominator_tree = DAG()
      """ each  node in the `dominator tree` is a child 
      of `immediate dominator` """
      for u,v in idom.items():
        dominator_tree.add_edge(v,u)
      # assert nx.is_tree(dominator_tree) 
      """node with 2 or more successors in the `dominator
      tree` and single successor of the node in the `original 
      DAG` are `cutnodes` """ 
      while queue:
        u = queue.popleft()
        for v in dominator_tree.successors(u):
          if len(dominator_tree.succ[v])>=2:
            cutnodes.add(v)
          queue.append(v)
      return cutnodes #,dominator_tree
