# -*- coding: utf-8 -*-

import pytest
import pgf

@pytest.fixture
def multilexlang_2022_07():
    return {
        "grammar": "tests/MultiLexLang.pgf",
        "conc_name": "MultiLexLangZul",
        "exprs": [
            pgf.readExpr('PhrUtt NoPConj (UttS (UseCl TPresTemp PPos (PredVP (DetCN (DetNum NumSg) (UseN boy_N)) (UseV walk_V)))) NoVoc'),
            pgf.readExpr('PhrUtt NoPConj (UttS (UseCl TFutTemp PPos (PredVP (DetCN (DetNum NumSg) (PossNP (UseN aunt_paternal_N) (DetCN (DetNum NumSg) (UseN man_N)))) (ComplV2 want_V2 (DetCN (DetNum NumSg) (UseN cheese_N)))))) NoVoc')
        ],
        "children": [
            [pgf.readExpr('NoPConj'),pgf.readExpr('UttS (UseCl TPresTemp PPos (PredVP (DetCN (DetNum NumSg) (UseN boy_N)) (UseV walk_V)))'),pgf.readExpr('NoVoc')],
            [pgf.readExpr('NoPConj'),pgf.readExpr('UttS (UseCl TFutTemp PPos (PredVP (DetCN (DetNum NumSg) (PossNP (UseN aunt_paternal_N) (DetCN (DetNum NumSg) (UseN man_N)))) (ComplV2 want_V2 (DetCN (DetNum NumSg) (UseN cheese_N)))))'),pgf.readExpr('NoVoc')]
        ],
        "cn_subtrees": [
            [pgf.readExpr('UseN boy_N')],
            [pgf.readExpr('PossNP (UseN aunt_paternal_N) (DetCN (DetNum NumSg) (UseN man_N))'),pgf.readExpr('UseN aunt_paternal_N'),pgf.readExpr('UseN man_N'),pgf.readExpr('UseN cheese_N')]
        ],
        "cn_subtrees_nonoverlap": [
            [pgf.readExpr('UseN boy_N')],
            [pgf.readExpr('PossNP (UseN aunt_paternal_N) (DetCN (DetNum NumSg) (UseN man_N))'),pgf.readExpr('UseN cheese_N')]
        ],
        "usen_subtrees": [
            [pgf.readExpr('UseN boy_N')],
            [pgf.readExpr('UseN aunt_paternal_N'),pgf.readExpr('UseN man_N'),pgf.readExpr('UseN cheese_N')]
        ],
        "leaf_cats": {
            "NumSg": ['NumSg', 'NumPl'],
            "TPresTemp": ['TPresTemp', 'TFutTemp', 'TPastTemp', 'TRemFutTemp', 'TRemPastTemp']
        },
        "leaf_nodes_with_ids": [
            [(pgf.readExpr("NoPConj"), 0), (pgf.readExpr("TPresTemp"), 1), (pgf.readExpr("PPos"), 2), (pgf.readExpr("NumSg"), 3), (pgf.readExpr("boy_N"), 5), (pgf.readExpr("walk_V"), 8), (pgf.readExpr("NoVoc"), 13)],
            [(pgf.readExpr("NoPConj"), 0),
              (pgf.readExpr("TFutTemp"), 1),
              (pgf.readExpr("PPos"), 2),
              (pgf.readExpr("NumSg"), 3),
              (pgf.readExpr("aunt_paternal_N"), 5),
              (pgf.readExpr("NumSg"), 7),
              (pgf.readExpr("man_N"), 9),
              (pgf.readExpr("want_V2"), 14),
              (pgf.readExpr("NumSg"), 15),
              (pgf.readExpr("cheese_N"), 17),
              (pgf.readExpr("NoVoc"), 24)]
        ],
        "exprs_with_empty_nodes": [
            (pgf.readExpr('PhrUtt NoPConj (UttS (UseCl TPresTemp ? (PredVP (DetCN (DetNum NumSg) (UseN boy_N)) ?))) NoVoc'),(2,8)),
            (pgf.readExpr('PhrUtt NoPConj (UttS (UseCl TFutTemp PPos (PredVP (DetCN (DetNum NumSg) (PossNP (UseN aunt_paternal_N) ?)) (ComplV2 want_V2 (DetCN (DetNum NumSg) (UseN cheese_N)))))) ?'),(7,29))
        ],
        "substitute_nodes": [
            [pgf.readExpr("PNeg"),pgf.readExpr("(CopNPAssoc (PronPostdetNP it15_Pron (DemPostdet that_Quant)))")],
            [pgf.readExpr("(PostdetCN (PredetN (QuantPredet all_QuantStem) hand_N) (QuantDemPostdet all_QuantStem that_Quant) (DetNum NumSg))"),pgf.readExpr("NoVoc")]
        ],
        "reconstituted_tree_strs": [
            "PhrUtt NoPConj (UttS (UseCl TPresTemp PNeg (PredVP (DetCN (DetNum NumSg) (UseN boy_N)) (CopNPAssoc (PronPostdetNP it15_Pron (DemPostdet that_Quant)))))) NoVoc",
            "PhrUtt NoPConj (UttS (UseCl TFutTemp PPos (PredVP (DetCN (DetNum NumSg) (PossNP (UseN aunt_paternal_N) (PostdetCN (PredetN (QuantPredet all_QuantStem) hand_N) (QuantDemPostdet all_QuantStem that_Quant) (DetNum NumSg)))) (ComplV2 want_V2 (DetCN (DetNum NumSg) (UseN cheese_N)))))) NoVoc"
        ],
        "empty_leaves_tree_strs": [
            "PhrUtt ? (UttS (UseCl ? ? (PredVP (DetCN (DetNum ?) (UseN ?)) (CopNPAssoc (PronPostdetNP ? (DemPostdet ?)))))) ?",
            "PhrUtt ? (UttS (UseCl ? ? (PredVP (DetCN (DetNum ?) (PossNP (UseN ?) (PostdetCN (PredetN (QuantPredet ?) ?) (QuantDemPostdet ? ?) (DetNum ?)))) (ComplV2 ? (DetCN (DetNum ?) (UseN ?)))))) ?"
        ],
        "children_types": {
            "UseN": ["N"],
            "PhrUtt": ["PConj","Utt","Voc"],
            "TPresTemp": []
        },
        "random_cats": [
            'N', 'Temp','Utt','V','VP'
        ],
        "patterns": [
            ('Phr',"PhrUtt NoPConj (UttS (UseCl TPresTemp ? (PredVP (DetCN (DetNum NumSg) (UseN boy_N)) (CopNPAssoc (PronPostdetNP it15_Pron ?))))) NoVoc"),
            ('Phr',"PhrUtt NoPConj (UttS (UseCl TFutTemp PPos (PredVP (DetCN (DetNum NumSg) (PossNP (UseN aunt_paternal_N) (PostdetCN (PredetN (QuantPredet all_QuantStem) hand_N) ? (DetNum NumSg)))) (ComplV2 want_V2 ?)))) NoVoc"),
            ('CN','PossNP (UseN aunt_paternal_N) (DetCN (DetNum NumSg) (UseN man_N))')
        ],
        "tokens": [
            ['umfana', 'u', '&+', 'ya', '&+', 'hamb', '&+', 'a'],
            ['ubabekazi', 'we', '&+', 'ndoda', 'u', '&+', 'zo', '&+', 'fun', '&+', 'a', 'ushizi']
        ],
        "segments": [
            ['umfana', '_', 'u', 'ya', 'hamb', 'a'],
            ['ubabekazi', '_', 'we', 'ndoda', '_', 'u', 'zo', 'fun', 'a', '_', 'ushizi']
        ],
        "leaves_tagged": [
            [('umfana', 'boy_N', 5),
                ('u', None, -1),
                ('&+', None, -1),
                ('ya', None, -1),
                ('&+', None, -1),
                ('hamb&+a', 'walk_V', 8)
            ],
            [('ubabekazi', 'aunt_paternal_N', 5),
                ('we', None, -1),
                ('&+', None, -1),
                ('ndoda', 'man_N', 9),
                ('u', None, -1),
                ('&+', None, -1),
                ('zo', None, -1),
                ('&+', None, -1),
                ('fun&+a', 'want_V2', 14),
                ('ushizi', 'cheese_N', 17)]
        ],
        "lin_brackets": [
            [
                (10,'umfana u&+ya&+hamb&+a'),
                (8,'hamb&+a'),
                (7,'umfana'),
                (12,'umfana u&+ya&+hamb&+a')
            ],
            [
                (12,'ubabekazi we&+ndoda'),
                (20,'u&+zo&+fun&+a ushizi'),
                (5,'ubabekazi'),
                (9,'ndoda'),
                (14,'fun&+a'),
                (17,'ushizi')
            ]
        ]
    }
