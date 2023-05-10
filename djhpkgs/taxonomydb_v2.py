import sys, os, re

class TaxTree(object):
    """构造taxonomy的分类树结构"""
    def __init__(self, taxid, level_rank, children=None, parent=None):
        self.taxid = taxid
        self.level_rank = level_rank
        self.children = []
        self.parent = parent
        if children is not None:
            for child in children:
                self.add_child(child)
    def add_child(self, node):
        assert isinstance(node, TaxTree)
        self.children.append(node)

def parser_nodes(nodes_dmp):
    """解析nodes.dmp"""
    with open(nodes_dmp, "r") as f:
        for line in f:
            pass
        
