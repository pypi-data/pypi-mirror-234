#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from abydos.distance._distance import _Distance

__all__ = ['AffineGapDistance', 'AffineGapSimilarity']

try:
    from abydos.distance.affinegap import affineGapDistance, normalizedAffineGapDistance
    from abydos.distance.cython_affine import affine, cython_sim_ident
except ImportError:
    import pyximport

    pyximport.install(inplace=True)
    from abydos.distance.affinegap import affineGapDistance, normalizedAffineGapDistance
    from abydos.distance.cython_affine import affine, cython_sim_ident


class AffineGapDistance(_Distance):

    def __init__(self,
                 matchWeight=1,
                 mismatchWeight=11,
                 gapWeight=10,
                 spaceWeight=7,
                 abbreviation_scale=.125):
        super().__init__()
        self.matchWeight = matchWeight
        self.mismatchWeight = mismatchWeight
        self.gapWeight = gapWeight
        self.spaceWeight = spaceWeight
        self.abbreviation_scale = abbreviation_scale

    def dist(self, src: str, tar: str) -> float:
        return affineGapDistance(src,
                                 tar,
                                 self.matchWeight,
                                 self.mismatchWeight,
                                 self.gapWeight,
                                 self.spaceWeight)

    def sim(self, src: str, tar: str) -> float:
        return self.sim_score(src, tar)

    def sim_score(self, src: str, tar: str) -> float:
        return normalizedAffineGapDistance(src,
                                           tar,
                                           self.matchWeight,
                                           self.mismatchWeight,
                                           self.gapWeight,
                                           self.spaceWeight)


class AffineGapSimilarity(_Distance):
    """Returns the affine gap score between two strings.

    The affine gap measure is an extension of the Needleman-Wunsch measure that handles the longer gaps more
    gracefully. For more information refer to the string matching chapter in the DI book ("Principles of Data Integration").

    Args:
        gap_start (float): Cost for the gap at the start (defaults to 1).
        gap_continuation (float): Cost for the gap continuation (defaults to 0.5).
        sim_func (function): Function computing similarity score between two characters, which are represented as strings (defaults
                             to an identity function, which returns 1 if the two characters are the same and returns 0 otherwise).

    Attributes:
        gap_start (float): An attribute to store the gap cost at the start.
        gap_continuation (float): An attribute to store the gap continuation cost.
        sim_func (function): An attribute to store the similarity function.
    """

    def __init__(self, gap_start=1, gap_continuation=0.5, sim_func=cython_sim_ident,
                 **kwargs: Any):
        super().__init__(**kwargs)
        self.gap_start = gap_start
        self.gap_continuation = gap_continuation
        self.sim_func = sim_func

    def dist(self, string1, string2):
        """Computes the affine gap score between two strings. This score can be outside the range [0,1].

        Args:
            string1,string2 (str) : Input strings.

        Returns:
            Affine gap score betwen the two input strings (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        # Examples:
        #     >>> aff = Affine()
        #     >>> aff.dist('dva', 'deeva')
        #     1.5
        #     >>> aff = Affine(gap_start=2, gap_continuation=0.5)
        #     >>> aff.dist('dva', 'deeve')
        #     -0.5
        #     >>> aff = Affine(gap_continuation=0.2, sim_func=lambda s1, s2: (int(1 if s1 == s2 else 0)))
        #     >>> aff.dist('AAAGAATTCA', 'AAATCA')
        #     4.4
        # """

        return affine(string1, string2, self.gap_start, self.gap_continuation,
                      self.sim_func)

    def sim_score(self, src: str, tar: str) -> float:
        normalizer = (self.dist(src, src) ** 0.5 * self.dist(tar, tar) ** 0.5)
        if normalizer == 0:
            return 0.0
        return min(max(0.0, self.dist(src, tar)) / normalizer, 1.0)

    def sim(self, src: str, tar: str) -> float:
        return self.sim_score(src, tar)

