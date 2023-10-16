# -*- coding: utf-8 -*-

import pgf

BIND = '&+'
WORD_BOUNDARY = '_'

def concat_bind(bracket_elements,bind=BIND):
    c_str = ""
    for e in bracket_elements:
        if isinstance(e,type(pgf.BIND)):
            c_str += bind
        else:
            c_str += str(e)
    return c_str

def is_leaf_bracket(bracket):
    for c in bracket.children:
        if isinstance(c,pgf.Bracket):
            return False
    return True

def tokens_from_bracket(bracket,bind=BIND):
    toks = []
    for b in bracket.children:
        if isinstance(b,str):
            toks.append(b)
        elif isinstance(b,type(pgf.BIND)):
            toks.append(bind)
        else:
            c_toks = tokens_from_bracket(b,bind)
            toks += c_toks
    return toks

def segments_from_bracket(bracket,wb=WORD_BOUNDARY):
    toks = tokens_from_bracket(bracket,BIND)
    segs = []
    for i in range(len(toks)-1):
        if toks[i] == BIND:
            continue
        elif toks[i+1] == BIND:
            segs.append(toks[i])
        else:
            segs += [toks[i],wb]
    segs.append(toks[-1])
    return segs

def tokens_from_expr(expr,conc,bind=BIND):
    expr = pgf.readExpr(str(expr))
    bl = conc.bracketedLinearize(expr)
    root_bracket = bl[0]
    return tokens_from_bracket(root_bracket,bind)

def segments_from_expr(expr,conc,wb=WORD_BOUNDARY):
    expr = pgf.readExpr(str(expr))
    bl = conc.bracketedLinearize(expr)
    try:
        root_bracket = bl[0]
    except IndexError:
        return []
    return segments_from_bracket(root_bracket,wb)

def leaf_tagged_linearize_bracket(bracket,bind=BIND):
    lin_pieces = []
    if isinstance(bracket,str):
        return [(bracket,None,-1)]
    if isinstance(bracket,type(pgf.BIND)):
    # if str(bracket) == BIND:
        bracket = (bind,None,-1)
        return [bracket]
    if is_leaf_bracket(bracket):
        lin_pieces.append((concat_bind(bracket.children,bind),bracket.fun,bracket.fid))
    else:
        for c in bracket.children:
            c_pieces = leaf_tagged_linearize_bracket(c,bind)
            lin_pieces += c_pieces
    return lin_pieces

def leaf_tagged_linearize(tree,concrete,bind=BIND):
    tree = pgf.readExpr(str(tree))
    [root_bracket] = concrete.bracketedLinearize(tree)
    return leaf_tagged_linearize_bracket(root_bracket,bind)

def concat_tokens(tokens,bind=BIND):
    pairs = [(None,tokens[0])] + [(tokens[i-1],tokens[i]) for i in range(1,len(tokens))]
    lin = ''
    for (prev,cur) in pairs:
        if prev and not prev == bind and not cur == bind:
            lin += ' '
        lin += cur
    return lin

def lin_at_fid_bracket(bracket,id,bind=BIND):
    if not isinstance(bracket,pgf.Bracket):
        return None
    bracket_children = [b for b in bracket.children if isinstance(b,pgf.Bracket)]
    if len(bracket_children) == 0 and bracket.fid != id:
        return None

    if bracket.fid == id:
        b_lins = []
        for b in bracket.children:
            if isinstance(b,str):
                b_lins.append(b)
            elif isinstance(b,type(pgf.BIND)):
                b_lins.append(bind)
            elif isinstance(b,pgf.Bracket):
                b_lins.append(lin_at_fid_bracket(b,b.fid,bind))
        return concat_tokens(b_lins,bind)
    else:
        for b in bracket.children:
            b_lin = lin_at_fid_bracket(b,id,bind)
            if b_lin:
                return b_lin
    return None

def lin_at_fid(tree,concrete,id,bind=BIND,prev_id=-1):
    tree = pgf.readExpr(str(tree))
    [b] = concrete.bracketedLinearize(tree)
    return lin_at_fid_bracket(b,id,bind)
