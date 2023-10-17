"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : stem_loop_predictor.py
@Author : Zhiyue Chen
@Time : 2023/9/19 23:19
"""
import RNA
from rapbuilder import constant


class CalcError(Exception):
    """
    A class contains all errors of RBSPredictor
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StemLoopPredictor:
    def __init__(self, stem_loop:str, temperature: float = 37.0, name: str = "Untitled"):
        """
        :param stem_loop: sequence of stem loop
        :param temperature: the temperature of the environment
        :param name: the name of the task
        """
        self.dG_stem_loop = None
        allowed_chars = set("ACGUT")
        stem_loop = stem_loop.upper()
        if set(stem_loop) > allowed_chars:
            raise ValueError('Please input correct coding of stem loop!')
        self.name = name
        self.temperature = temperature
        self.md = RNA.md()
        self.md.temperature = self.temperature
        self.stem_loop = stem_loop

    def calc_dG(self) -> None:
        """
        this function calculate the delta_G
        """
        self.dG_stem_loop = self.calc_dG_stem_loop()

    def calc_dG_stem_loop(self) -> float:
        """
        :return: the mfe of stem loop
        """
        stem_loop = constant.pre_seq_stem_loop + self.stem_loop
        fc = RNA.fold_compound(stem_loop, self.md)
        ss, mfe = fc.mfe()
        return mfe



