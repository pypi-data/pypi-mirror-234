#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tempfile

from constants import Flavour
from mosaic_utils.ai.file_utils import extract_tar
from mosaic_utils.ai.flavours import (
    keras,
    pytorch,
    sklearn,
    tensorflow,
    pyspark,
    spacy,
    pmml,
    xgboost,
)


def download_model(model_tar_path):
    """download model artifacts from object storage server"""
    # download model from object storage server
    # model_data = get_model_data(model_tar_path)
    # write model to tar file
    temp_dir = tempfile.mkdtemp()

    tar_path = os.path.join(model_tar_path, "ml_model.tar.gz")
    # model_data.save(tar_path)
    # extract model file
    extract_tar(tar_path, temp_dir)

    # Getting the list of directories
    dir = os.listdir(temp_dir)
    # Checking if the list is empty or not
    if len(dir) != 0:
        return temp_dir


def get_loader(flavour):
    if flavour == Flavour.keras:
        return keras.load_model
    if flavour == Flavour.sklearn:
        return sklearn.load_model
    if flavour == Flavour.pytorch:
        return pytorch.load_model
    if flavour == Flavour.tensorflow:
        return tensorflow.load_model
    if flavour == Flavour.pyspark:
        return pyspark.load_model
    if flavour == Flavour.spacy:
        return spacy.load_model
    if flavour == Flavour.r:
        # R import specifically moved below as it will give error of rpy2 while deploying otherwise
        from mosaic_utils.ai.flavours import r

        return r.load_model
    if flavour == Flavour.pmml:
        return pmml.load_model
    if flavour == Flavour.xgboost:
        return xgboost.load_model
