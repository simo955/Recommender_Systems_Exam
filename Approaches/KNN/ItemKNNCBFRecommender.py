#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 23/10/17


"""

from Base.Recommender import Recommender
from Base.Recommender_utils import check_matrix
from Base.SimilarityMatrixRecommender import SimilarityMatrixRecommender
from Base.IR_feature_weighting import okapi_BM_25, TF_IDF

import numpy as np

from Base.Similarity.Compute_Similarity import Compute_Similarity


class ItemKNNCBFRecommender(SimilarityMatrixRecommender, Recommender):
    """ ItemKNN recommender"""

    RECOMMENDER_NAME = "ItemKNNCBFRecommender"

    FEATURE_WEIGHTING_VALUES = ["BM25", "TF-IDF", "none"]

    def __init__(self, ICM, URM_train, sparse_weights=True):
        super(ItemKNNCBFRecommender, self).__init__()

        self.ICM = ICM.copy()

        # CSR is faster during evaluation
        self.URM_train = check_matrix(URM_train.copy(), 'csr')

        self.sparse_weights = sparse_weights


    def fit(self, topK=10, shrink=50, similarity='cosine', normalize=True, feature_weighting = "BM25", **similarity_args):

        self.topK = topK
        self.shrink = shrink

        if feature_weighting not in self.FEATURE_WEIGHTING_VALUES:
            raise ValueError("Value for 'feature_weighting' not recognized. Acceptable values are {}, provided was '{}'".format(self.FEATURE_WEIGHTING_VALUES, feature_weighting))


        if feature_weighting == "BM25":
            self.ICM = self.ICM.astype(np.float32)
            self.ICM = okapi_BM_25(self.ICM)

        elif feature_weighting == "TF-IDF":
            self.ICM = self.ICM.astype(np.float32)
            self.ICM = TF_IDF(self.ICM)


        similarity = Compute_Similarity(self.ICM.T, shrink=shrink, topK=topK, normalize=normalize, similarity = similarity, **similarity_args)


        if self.sparse_weights:
            self.W_sparse = similarity.compute_similarity()
        else:
            self.W = similarity.compute_similarity()
            self.W = self.W.toarray()

