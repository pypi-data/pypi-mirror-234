"""
common parts of the test suite for rapidfuzz
"""
from math import isnan

import pytest

from rapidfuzz import process_cpp, process_py, utils


def is_none(s):
    if s is None:
        return True

    if isinstance(s, float) and isnan(s):
        return True

    return False


def scorer_tester(scorer, s1, s2, **kwargs):
    score1 = scorer(s1, s2, **kwargs)

    if "processor" not in kwargs:
        kwargs["processor"] = None
    elif kwargs["processor"] is True:
        kwargs["processor"] = utils.default_process
    elif kwargs["processor"] is False:
        kwargs["processor"] = None

    extractOne_res1 = process_cpp.extractOne(s1, [s2], scorer=scorer, **kwargs)
    extractOne_res2 = process_py.extractOne(s1, [s2], scorer=scorer, **kwargs)
    extract_res1 = process_cpp.extract(s1, [s2], scorer=scorer, **kwargs)
    extract_res2 = process_py.extract(s1, [s2], scorer=scorer, **kwargs)
    extract_iter_res1 = list(
        process_cpp.extract_iter(s1, [s2], scorer=scorer, **kwargs)
    )
    extract_iter_res2 = list(process_py.extract_iter(s1, [s2], scorer=scorer, **kwargs))

    if is_none(s1) or is_none(s2):
        assert extractOne_res1 is None
        assert extractOne_res2 is None
        assert extract_res1 == []
        assert extract_res2 == []
    # todo add testing with score_cutoff
    # this is a bit harder, since result elements are filtererd out
    # if they are worse than score_cutoff
    elif kwargs.get("score_cutoff") is not None:
        assert extractOne_res1 is None or pytest.approx(score1) == extractOne_res1[1]
        assert extractOne_res2 is None or pytest.approx(score1) == extractOne_res2[1]
        assert extract_res1 == [] or pytest.approx(score1) == extract_res1[0][1]
        assert extract_res2 == [] or pytest.approx(score1) == extract_res2[0][1]
        assert (
            extract_iter_res1 == [] or pytest.approx(score1) == extract_iter_res1[0][1]
        )
        assert (
            extract_iter_res2 == [] or pytest.approx(score1) == extract_iter_res2[0][1]
        )
    else:
        assert pytest.approx(score1) == extractOne_res1[1]
        assert pytest.approx(score1) == extractOne_res2[1]
        assert pytest.approx(score1) == extract_res1[0][1]
        assert pytest.approx(score1) == extract_res2[0][1]
        assert pytest.approx(score1) == extract_iter_res1[0][1]
        assert pytest.approx(score1) == extract_iter_res2[0][1]

    try:
        import numpy as np
    except Exception:
        np = None

    # todo this should be able to handle None similar to the original scorer
    if not is_none(s1) and not is_none(s2) and np is not None:
        score6 = process_cpp.cdist([s1], [s2], scorer=scorer, **kwargs)[0][0]
        score7 = process_py.cdist([s1], [s2], scorer=scorer, **kwargs)[0][0]
        assert pytest.approx(score1) == score6
        assert pytest.approx(score1) == score7

    return score1


def symmetric_scorer_tester(scorer, s1, s2, **kwargs):
    score1 = scorer_tester(scorer, s1, s2, **kwargs)
    score2 = scorer_tester(scorer, s2, s1, **kwargs)
    assert pytest.approx(score1) == score2
    return score1


class GenericScorer:
    def __init__(self, py_scorer, cpp_scorer, get_scorer_flags):
        self.py_scorer = py_scorer
        self.cpp_scorer = cpp_scorer
        self.get_scorer_flags = get_scorer_flags

    def _distance(self, s1, s2, **kwargs):
        symmetric = self.get_scorer_flags(s1, s2, **kwargs)["symmetric"]
        tester = symmetric_scorer_tester if symmetric is True else scorer_tester

        assert hasattr(self.cpp_scorer.distance, "_RF_ScorerPy")
        assert hasattr(self.cpp_scorer.distance, "_RF_Scorer")
        assert hasattr(self.py_scorer.distance, "_RF_ScorerPy")
        score1 = tester(self.cpp_scorer.distance, s1, s2, **kwargs)
        score2 = tester(self.py_scorer.distance, s1, s2, **kwargs)
        assert pytest.approx(score1) == score2
        return score1

    def _similarity(self, s1, s2, **kwargs):
        symmetric = self.get_scorer_flags(s1, s2, **kwargs)["symmetric"]
        tester = symmetric_scorer_tester if symmetric is True else scorer_tester

        assert hasattr(self.cpp_scorer.similarity, "_RF_ScorerPy")
        assert hasattr(self.cpp_scorer.similarity, "_RF_Scorer")
        assert hasattr(self.py_scorer.similarity, "_RF_ScorerPy")
        score1 = tester(self.cpp_scorer.similarity, s1, s2, **kwargs)
        score2 = tester(self.py_scorer.similarity, s1, s2, **kwargs)
        assert pytest.approx(score1) == score2
        return score1

    def _normalized_distance(self, s1, s2, **kwargs):
        symmetric = self.get_scorer_flags(s1, s2, **kwargs)["symmetric"]
        tester = symmetric_scorer_tester if symmetric is True else scorer_tester

        assert hasattr(self.cpp_scorer.normalized_distance, "_RF_ScorerPy")
        assert hasattr(self.cpp_scorer.normalized_distance, "_RF_Scorer")
        assert hasattr(self.py_scorer.normalized_distance, "_RF_ScorerPy")
        score1 = tester(self.cpp_scorer.normalized_distance, s1, s2, **kwargs)
        score2 = tester(self.py_scorer.normalized_distance, s1, s2, **kwargs)
        assert pytest.approx(score1) == score2
        return score1

    def _normalized_similarity(self, s1, s2, **kwargs):
        symmetric = self.get_scorer_flags(s1, s2, **kwargs)["symmetric"]
        tester = symmetric_scorer_tester if symmetric is True else scorer_tester

        assert hasattr(self.cpp_scorer.normalized_similarity, "_RF_ScorerPy")
        assert hasattr(self.cpp_scorer.normalized_similarity, "_RF_Scorer")
        assert hasattr(self.py_scorer.normalized_similarity, "_RF_ScorerPy")
        score1 = tester(self.cpp_scorer.normalized_similarity, s1, s2, **kwargs)
        score2 = tester(self.py_scorer.normalized_similarity, s1, s2, **kwargs)
        assert pytest.approx(score1) == score2
        return score1

    def _validate(self, s1, s2, **kwargs):
        # todo requires more complex test handling
        # score_cutoff = kwargs.get("score_cutoff")
        kwargs = {k: v for k, v in kwargs.items() if k != "score_cutoff"}

        maximum = self.get_scorer_flags(s1, s2, **kwargs)["maximum"]
        dist = self._distance(s1, s2, **kwargs)
        sim = self._similarity(s1, s2, **kwargs)
        norm_dist = self._normalized_distance(s1, s2, **kwargs)
        norm_sim = self._normalized_similarity(s1, s2, **kwargs)
        assert pytest.approx(dist) == maximum - sim
        if maximum != 0:
            assert pytest.approx(dist / maximum) == norm_dist
            assert pytest.approx(sim / maximum) == norm_sim
        else:
            assert pytest.approx(0.0) == norm_dist
            assert pytest.approx(1.0) == norm_sim

    def distance(self, s1, s2, **kwargs):
        self._validate(s1, s2, **kwargs)
        return self._distance(s1, s2, **kwargs)

    def similarity(self, s1, s2, **kwargs):
        self._validate(s1, s2, **kwargs)
        return self._similarity(s1, s2, **kwargs)

    def normalized_distance(self, s1, s2, **kwargs):
        if not is_none(s1) and not is_none(s2):
            self._validate(s1, s2, **kwargs)
        return self._normalized_distance(s1, s2, **kwargs)

    def normalized_similarity(self, s1, s2, **kwargs):
        if not is_none(s1) and not is_none(s2):
            self._validate(s1, s2, **kwargs)
        return self._normalized_similarity(s1, s2, **kwargs)
