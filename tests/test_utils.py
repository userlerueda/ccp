"""Test utilty module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from unittest import TestCase

import pytest

from ccp.util import to_ccp_score, where

PLAYER_COLLECTION = [
    {"tsw": {"names": ["Luis Rueda"]}},
    {"tsw": {"names": ["Ana Rico"]}},
]


class TestUtilities:
    @pytest.mark.parametrize(
        "collection, left_side, operator, right_side, filtered_collection",
        [
            (
                PLAYER_COLLECTION,
                "tsw.names",
                "array-contains",
                "Luis Rueda",
                [{"tsw": {"names": ["Luis Rueda"]}}],
            ),
        ],
    )
    def test_where(
        self,
        collection,
        left_side,
        operator,
        right_side,
        filtered_collection,
    ):
        """
        Test where
        """

        assert filtered_collection == where(
            collection, left_side, operator, right_side
        )

    @pytest.mark.parametrize(
        "score_array, score",
        [
            ([[7, 6, 4], [6, 3]], "76 (4) 63"),
        ],
    )
    def test_to_ccp_score(self, score_array, score):
        """
        Test to_ccp_score
        """

        assert score == to_ccp_score(score_array)
