# -*- coding: utf-8 -*-

import pytest
import pgf
import pgfaux.generate as gen

def test_replace_empty_nodes(multilexlang_2022_07):
    data = multilexlang_2022_07
    for i in range(len(data["exprs_with_empty_nodes"])):
        tree = data["exprs_with_empty_nodes"][i][0]
        nodes = data["substitute_nodes"][i]
        assert str(gen.replace_empty_nodes(tree,nodes)[0]) == data["reconstituted_tree_strs"][i]

def test_make_leaves_empty(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data["reconstituted_tree_strs"])):
        full_tree = data["reconstituted_tree_strs"][i]
        empty_leaves_tree = data["empty_leaves_tree_strs"][i]
        emptied_tree = gen.make_leaves_empty(full_tree,grammar,concrete)
        assert str(emptied_tree) == empty_leaves_tree

def test_children_types(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for fun in data['children_types'].keys():
        assert tuple(gen.children_types(grammar,fun)) == tuple(data['children_types'][fun])

def test_generate_random_tree_by_cat(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for cat in multilexlang_2022_07['random_cats']:
        tree = gen.generate_random_tree_by_cat(grammar,cat)
        assert grammar.checkExpr(tree,pgf.readType(cat))

def test_generate_random_tree_by_pattern(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for cat,pattern in multilexlang_2022_07['patterns']:
        tree = gen.generate_random_tree_by_pattern(grammar,pattern)
        assert grammar.checkExpr(tree,pgf.readType(cat))

def test_replace_at_id(multilexlang_2022_07):
    data = multilexlang_2022_07
    for i in range(len(data["exprs_with_empty_nodes"])):
        expr,ids = data["exprs_with_empty_nodes"][i]
        sub_nodes = data["substitute_nodes"][i]
        for j in range(len(ids)):
            expr = gen.replace_at_id(expr,sub_nodes[j],ids[j])
        assert str(expr) == data["reconstituted_tree_strs"][i]
