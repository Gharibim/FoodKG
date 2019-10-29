'''
Load the embedding model using TF and then load the STM model
'''

import os
import tensorflow as tf
import numpy as np
import pickle
from Prediction.helpers import data_shaper
from Prediction.embeddings import text_embeddings
from Prediction.models import wordpair_classifier


source = 'Prediction/AGROVEC/AGROVEC.txt'

# Get the vectors for the data and return the feed dictionary
def build_feed_dict_func(model, data, config = None, predict = False):
    x_pairs, y = zip(*data)
    x1s = [x[0] for x in x_pairs]
    x2s = [x[1] for x in x_pairs]
    drp = 0.5
    fd = model.get_feed_dict(x1s, x2s, None if predict else y, 1.0 if predict else drp, not predict)
    return fd, y



t_embeddings = None
model = None
session = None
dist_labels = None

# Start loading the models here (limit is 1000000 words)
def prepare_Models():
    global t_embeddings
    global model
    global session
    global dist_labels
    print("Loading word embeddings...")
    t_embeddings = text_embeddings.Embeddings()
    t_embeddings.load_embeddings(source, 1000000, language='default', print_loading=True, skip_first_line=True)
    vocabulary_size = len(t_embeddings.lang_vocabularies["default"])
    embeddings = t_embeddings.lang_embeddings["default"].astype(np.float64)
    embedding_size = t_embeddings.emb_sizes["default"]
    t_embeddings.inverse_vocabularies()

    print("Loading model...")
    # print(os.getcwd())
    hyperparams, vars = pickle.load(open("Prediction/relations_prediction/args.output", "rb"))

    same_mlp = hyperparams[0]
    bilinear_softmax = hyperparams[1]
    mlp_hidden_layer_sizes = hyperparams[2]
    num_mlps = hyperparams[3]
    embedding_size = hyperparams[5]
    dist_labels = hyperparams[6]
    act = tf.nn.tanh
    noise = 0

    tf.reset_default_graph()
    model = wordpair_classifier.WordPairClassifier(embeddings, embedding_size, mlp_hidden_layer_sizes, same_mlp=same_mlp, bilinear_softmax=bilinear_softmax, num_mappings=num_mlps, activation=act, num_classes=len(dist_labels), noise_std=noise)

    print("Initializing tensorflow session...")
    session = tf.InteractiveSession()
    session.run(tf.global_variables_initializer())

    model.set_variable_values(session, vars)


# Return the semantic similarity for subject and object (pass the actual words)
def get_Similarity(subject, object):
    return t_embeddings.word_similarity(subject, object, "default", "default")


# predict the relation between subject and object (pass the actual words)
def predict_Relationship(subject, object):
    print("Preparing prediction examples...")
    predict_wordpairs = [(subject, object)]
    predict_pairs = data_shaper.prep_word_tuples(predict_wordpairs, t_embeddings, "default", labels=None)
    predict_data = list(zip(predict_pairs, [None] * len(predict_pairs)))

    print("Computing predictions...")
    preds = model.preds_raw.eval(session=session,
                                 feed_dict=build_feed_dict_func(model, predict_data, predict=True)[0])
    pred_labels = [dist_labels[np.argmax(p)] for p in preds]

    prdes = "Prediction/data/predict.data"
    # if prdes is not None and not os.path.isdir(os.path.dirname(prdes)) and not os.path.dirname(prdes) == "":
    print("Writing predictions to file...")
    to_write = list(zip([t_embeddings.get_word_from_index(x[0], lang="default") for x in predict_pairs],
                        [t_embeddings.get_word_from_index(x[1], lang="default") for x in predict_pairs],
                        pred_labels))
    # print("To WriteLOOOOOOOL", to_write)
    return to_write[0][2]
