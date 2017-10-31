#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import math
from random import randint
from Helper.DesignPattern import Singleton
from Helper.JaroWinklerDistance import JaroWinklerDistance

class Neri:
    __metaclass__ = Singleton

    def __init__(self):
        with open("./Data/NeriEng.json", "r") as data_file:
            self.__eng = json.load(data_file)

        with open("./Data/NeriVni.json", "r") as data_file:
            self.__vni = json.load(data_file)

        self.__cntQuestions = 0
        self.__numQuestions = len(self.__eng) + len(self.__vni)
        self.__questions = [""] * self.__numQuestions
        self.__mapping = dict()
        self.__build(self.__eng)
        self.__build(self.__vni)
        self.__indexing()

    def __build(self, dict):
        for key in dict.keys():
            self.__questions[self.__cntQuestions] = key
            for word in key.split(' '):
                map = self.__mapping.get(word, [])
                if len(map) == 0:
                    map = [0] * self.__numQuestions
                    self.__mapping[word] = map
                map[self.__cntQuestions] += 1
            self.__cntQuestions += 1

    def __indexing(self):
        for key in self.__mapping.keys():
            map = self.__mapping[key]
            maxFreq = max(map) * 1.0
            numContained = (len(map) - map.count(0)) * 1.0
            idf = math.log(self.__numQuestions / numContained, 2)
            idx = 0
            while idx < self.__numQuestions:
                if map[idx] > 0:
                    tf = map[idx] / maxFreq
                    map[idx] = tf * idf
                idx += 1

    def __analyze(self, question):
        keys = self.__mapping.keys()
        jaroWinklerDistance = JaroWinklerDistance()
        scoreTable = [0] * self.__numQuestions
        words = set(question.split(' '))
        print words
        for word in words:
            filtered = [w for w in keys if jaroWinklerDistance.get_jaro_distance(word, w) > 0.9]
            if len(filtered) > 0:
                for w in filtered:
                    weights = self.__mapping[w]
                    distance = jaroWinklerDistance.get_jaro_distance(word, w)
                    weights = [x * distance for x in weights]
                    weights = [scoreTable, weights]
                    scoreTable = [sum(x) for x in zip(*weights)]
        maxVal = max(scoreTable)
        if maxVal == 0: return question, 0
        res = [idx for idx in range(0, len(scoreTable)) if scoreTable[idx] == maxVal]
        for i in res:
            if self.__questions[i] == question: return question, 10
        idx = randint(0, len(res) - 1)
        return self.__questions[int(list(res)[idx])], maxVal

    def ask(self, question):
        question, score = self.__analyze([question.lower()][0])
        answers = self.__eng.get(question, []) # Sorry! I don't understand what you mean!
        if len(answers) == 0: answers = self.__vni.get(question, [u"Xin lỗi! Neri không thể hiểu ý bạn!"])
        idx = randint(0, len(answers) - 1)
        return question, answers[idx].encode('utf_8'), score
