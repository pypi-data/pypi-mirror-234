# -*- coding: utf-8 -*-

import pytest
import pgf
import pgfaux.analyze as an

def test_node_is_empty(multilexlang_2022_07):
    data = multilexlang_2022_07
    for e in data['exprs']:
        assert an.node_is_empty(e) == False
    expr = pgf.readExpr('?')
    assert an.node_is_empty(expr) == True

def test_is_equal(multilexlang_2022_07):
    data = multilexlang_2022_07
    assert an.is_equal(data['exprs'][0],data['exprs'][0]) == True
    assert an.is_equal(data['exprs'][0],data['exprs'][1]) == False

def test_depth(multilexlang_2022_07):
    data = multilexlang_2022_07
    assert an.depth(data['exprs'][0]) == 6
    assert an.depth(data['exprs'][1]) == 8
    assert an.depth(pgf.readExpr('?')) == 0
    assert an.depth(pgf.readExpr('RootFun')) == 0

def test_root_str(multilexlang_2022_07):
    data = multilexlang_2022_07
    assert an.root_str(data['exprs'][0]) == 'PhrUtt'
    assert an.root_str(pgf.readExpr('?')) == None
    assert an.root_str(pgf.readExpr('"symbol"')) == '"symbol"'

def test_root_cat(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for e in data['exprs']:
        assert an.root_cat(e,grammar) == 'Phr'
    assert an.root_cat(pgf.readExpr('"symbol"'),grammar) == an.SYMB

def test_children_trees(multilexlang_2022_07):
    data = multilexlang_2022_07
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        cs = tuple([str(c) for c in data['children'][i]])
        cs_ = tuple([str(c) for c in an.children_trees(e)])
        assert cs == cs_
    assert an.children_trees(pgf.readExpr('?')) == []
    assert an.children_trees(pgf.readExpr('"symbol"')) == []
    assert an.children_trees(pgf.readExpr('RootFun')) == []

def test_subtrees_of_cat(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        ss = tuple([str(s) for s in data['cn_subtrees'][i]])
        ss_ = tuple([str(s) for s in an.subtrees_of_cat(e,'CN',grammar,overlap=True)])
        assert ss == ss_
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        ss = tuple([str(s) for s in data['cn_subtrees_nonoverlap'][i]])
        ss_ = tuple([str(s) for s in an.subtrees_of_cat(e,'CN',grammar,overlap=False)])
        assert ss == ss_

def test_subtrees_of_fun(multilexlang_2022_07):
    data = multilexlang_2022_07
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        ss = tuple([str(s) for s in data['usen_subtrees'][i]])
        ss_ = tuple([str(s) for s in an.subtrees_of_fun(e,'UseN')])
        assert ss == ss_

def test_alternative_leaf_function_names(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    for l in data["leaf_cats"].keys():
        e = pgf.readExpr(l)
        ls = an.alternative_leaf_function_names(e,grammar,data["conc_name"])
        assert ls == data["leaf_cats"][l]

def test_leaf_nodes_with_ids(multilexlang_2022_07):
    data = multilexlang_2022_07
    for i in range(len(data["exprs"])):
        e = data["exprs"][i]
        ls = an.leaf_nodes_with_ids(e)
        assert ls == data["leaf_nodes_with_ids"][i]

def empty_nodes_with_ids(multilexlang_2022_07):
    data = multilexlang_2022_07
    for e,ids in data["exprs"]:
        assert tuple(an.empty_node_ids(e)) == ids
