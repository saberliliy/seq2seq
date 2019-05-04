#! /usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np

from quatrains import get_quatrains
from rhyme import RhymeEvaluator
from predict import Seq2SeqPredictor
from plan import Planner

from IPython import embed


def eval_poems(evaluator, poems):
    scores = []
    for poem in poems:
        score = evaluator.eval(poem)
        scores.append(score)

    mean_score = np.mean(scores)
    std_score = np.std(scores)

    print( "Mean score = {}, standard deviation = {}".format(mean_score, std_score))
    return scores, mean_score, std_score


def eval_train_data():
    evaluator = RhymeEvaluator()

    quatrains = get_quatrains()
    poems = list(map(lambda quatrain: quatrain['sentences'], quatrains)) # Strip out metadata information

    print( "Testing {} quatrains from the corpus.".format(len(poems)))
    eval_poems(evaluator, poems)
    

def eval_generated_data(num=100):
    evaluator = RhymeEvaluator()

    planner = Planner()
    predictor = Seq2SeqPredictor()

    poems = []
    for _ in range(num):        
        keywords = planner.plan(u'')
        assert 4 == len(keywords)

        sentences = predictor.predict(keywords)
        poems.append(sentences)

    print ("Testing {} quatrains generated by model.".format(num))
    eval_poems(evaluator, poems)


def main():
    # eval_train_data()
    eval_generated_data()
    

if __name__ == '__main__':
    main()