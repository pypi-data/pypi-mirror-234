

from constants import Flavour

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
