# -*- coding: utf-8 -*-

import pytest
import pgf
import pgfaux.linearize as lin

def test_tokens_from_bracket(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        [b] = concrete.bracketedLinearize(data['exprs'][i])
        assert tuple(lin.tokens_from_bracket(b)) == tuple(data['tokens'][i])

def test_segments_from_bracket(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        [b] = concrete.bracketedLinearize(data['exprs'][i])
        assert tuple(lin.segments_from_bracket(b)) == tuple(data['segments'][i])

def test_tokens_from_expr(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        assert tuple(lin.tokens_from_expr(data['exprs'][i],concrete)) == tuple(data['tokens'][i])

def test_segments_from_expr(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        assert tuple(lin.segments_from_expr(data['exprs'][i],concrete)) == tuple(data['segments'][i])

def test_leaf_tagged_linearize_bracket(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        [b] = concrete.bracketedLinearize(data['exprs'][i])
        assert tuple(lin.leaf_tagged_linearize_bracket(b)) == tuple(data['leaves_tagged'][i])

def test_leaf_tagged_linearize(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        assert tuple(lin.leaf_tagged_linearize(data['exprs'][i],concrete)) == tuple(data['leaves_tagged'][i])

def test_lin_at_fid_bracket(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        [b] = concrete.bracketedLinearize(e)
        for (fid,l) in data['lin_brackets'][i]:
            assert lin.lin_at_fid_bracket(b,fid) == l

def test_lin_at_fid(multilexlang_2022_07):
    data = multilexlang_2022_07
    grammar = pgf.readPGF(data['grammar'])
    concrete = grammar.languages[data['conc_name']]
    for i in range(len(data['exprs'])):
        e = data['exprs'][i]
        for (fid,l) in data['lin_brackets'][i]:
            assert lin.lin_at_fid(e,concrete,fid) == l
