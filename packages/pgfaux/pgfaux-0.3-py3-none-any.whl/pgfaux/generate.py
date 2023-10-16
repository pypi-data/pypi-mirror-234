# -*- coding: utf-8 -*-

import pgf
import pgfaux.analyze as analyze
from pgfaux.exceptions import *

import random
import itertools

MAX_GR_ATTEMPTS = 100
MAX_GR_DEPTH = 10

def replace_empty_nodes(tree,nodes):
    tree = pgf.readExpr(str(tree))
    if analyze.depth(tree) == 0 and str(tree) == '?':
        if len(nodes) > 1:
            return pgf.readExpr(str(nodes[0])),nodes[1:]
        elif len(nodes) > 0:
            return pgf.readExpr(str(nodes[0])),[]
        else:
            return tree,[]
    children = analyze.children_trees(tree)
    new_children = []
    for c in children:
        new_c,nodes = replace_empty_nodes(c,nodes)
        new_children.append(new_c)
    return pgf.Expr(analyze.root_str(tree),new_children),nodes

def make_leaves_empty(tree,grammar,concrete):
    tree = pgf.readExpr(str(tree))
    depth = analyze.depth(tree)
    root_fun_name = analyze.root_str(tree)
    if depth == 0:
        if str(tree) == '?':
            return tree
        else:
            return pgf.readExpr('?')
    children = analyze.children_trees(tree)
    new_children = []
    for c in children:
        new_c = make_leaves_empty(c,grammar,concrete)
        new_children.append(new_c)
    return pgf.Expr(root_fun_name,new_children)

def children_types(grammar,fun_str):
    funtype = grammar.functionType(fun_str)
    if len(funtype.hypos) == 0:
        return []
    return [str(funtype.hypos[i][2]) for i in range(len(funtype.hypos))]

def generate_random_fun(grammar,cat_str):
    funs = grammar.functionsByCat(cat_str)
    print(cat_str,funs)
    index = random.randint(0,max(len(funs)-1,0))
    if index >= len(funs):
        return None
    return funs[index]

def _generate_random_tree_by_cat(grammar,cat_str,depth):
    fun_str = generate_random_fun(grammar,cat_str)
    if not fun_str:
        return None
    children = children_types(grammar,fun_str)
    if len(children) == 0:
        return pgf.readExpr(fun_str)
    elif depth == 0:
        return None
    else:
        children_trees = []
        for c in children:
            ct = _generate_random_tree_by_cat(grammar,c,depth-1)
            if not ct:
                return None
            children_trees.append(ct)
        return pgf.Expr(fun_str,children_trees)

def generate_random_tree_by_cat(grammar,cat_str,depth=MAX_GR_DEPTH):
    for i in range(MAX_GR_ATTEMPTS):
        tree = _generate_random_tree_by_cat(grammar,cat_str,depth)
        if tree:
            return tree

def generate_random_tree_by_pattern(grammar,pattern,depth=MAX_GR_DEPTH):
    pattern = pgf.readExpr(str(pattern))
    if analyze.node_is_empty(pattern):
        return generate_random_tree_by_cat(grammar,str(grammar.startCat),depth)
    else:
        fun,children = pattern.unpack()
        c_types = children_types(grammar,fun)
        if len(c_types) != len(children):
            raise InvalidPattern(pattern)
        new_children = []
        if len(children) > 0:
            for i in range(len(children)):
                if analyze.node_is_empty(children[i]):
                    new_children.append(generate_random_tree_by_cat(grammar,c_types[i],depth-1))
                else:
                    new_children.append(generate_random_tree_by_pattern(grammar,children[i],depth-1))
            return pgf.Expr(fun,new_children)
        else:
            return pgf.readExpr(fun)

def _replace_at_id(tree,subtree,id,prev_id=-1):
    tree = pgf.readExpr(str(tree))
    children = analyze.children_trees(tree)
    if len(children) == 0: # tree is a leaf
        cur_id = prev_id + 1
        if cur_id == id:
            return subtree,cur_id
        else:
            return tree,cur_id
    new_children = []
    for c in children:
        new_c,prev_id = _replace_at_id(c,subtree,id,prev_id)
        new_children.append(new_c)
        cur_id = prev_id + 1
    if cur_id == id:
        return subtree,cur_id
    return pgf.Expr(analyze.root_str(tree),new_children),cur_id

def replace_at_id(tree,subtree,id):
    new_tree,root_id = _replace_at_id(tree,subtree,id)
    return new_tree
