"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : rbs_predictor.py
@Author : Zhiyue Chen
@Time : 2023/8/24 0:37
"""
# References
# 1. Liu, Y., Wu, Z., Wu, D., Gao, N., & Lin, J. (2023). Reconstitution of Multi-Protein Complexes through
# Ribozyme-Assisted Polycistronic Co-Expression. ACS Synthetic Biology, 12(1), 136–143.
# https://doi.org/10.1021/acssynbio.2c00416
# 2. Salis, H. (2023). Hsalis/Ribosome-Binding-Site-Calculator-v1.0 [Python].
# https://github.com/hsalis/Ribosome-Binding-Site-Calculator-v1.0 (Original work published 2009)
# 3. Salis, H. M. (2011). The ribosome binding site calculator. Methods in Enzymology, 498, 19–42.
# https://doi.org/10.1016/B978-0-12-385120-8.00002-4
# 4. Lorenz, R., Bernhart, S. H., Höner zu Siederdissen, C., Tafer, H., Flamm, C., Stadler, P. F., &
# Hofacker, I. L. (2011). ViennaRNA Package 2.0. Algorithms for Molecular Biology, 6(1), 26.
# https://doi.org/10.1186/1748-7188-6-26
import math
import sys
from copy import deepcopy

import RNA

from rapbuilder import constant

RNA.cvar.uniq_ML = 1


class CalcError(Exception):
    """
    A class contains all errors of RBSPredictor
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RBSPredictor:
    def __init__(self, mRNA: str, start_codon_range: list, temperature: float = 37.0, name: str = "Untitled"):
        """
        :param mRNA: the sequence of mRNA
        :param start_codon_range: the position range of the start codon
        :param temperature: the temperature of the environment
        :param name: the name of the task
        """
        self.dangles = 2
        RNA.cvar.uniq_ML = 1
        mRNA = mRNA.upper()
        allowed_chars = set("ACGUT")
        if set(mRNA) > allowed_chars:
            raise ValueError('Please input correct coding of mRNA!')
        start_codon_range[0] = max(start_codon_range[0], 0)
        start_codon_range[1] = min(start_codon_range[1], len(mRNA))
        self.name = name
        self.temperature = temperature
        self.md = RNA.md()
        self.md.temperature = self.temperature
        self.mRNA = mRNA
        self.dG_rRNA = self.calc_dG_rRNA
        self.start_codon_range = start_codon_range
        # Initialization of data structures
        self.mRNA_structure_list = []
        self.mRNA_rRNA_uncorrected_structure_list = []
        self.mRNA_rRNA_corrected_structure_list = []
        self.most_5p_mRNA_list = []
        self.dG_start_energy_list = []
        self.dG_mRNA_list = []
        self.dG_mRNA_rRNA_list = []
        self.dG_spacing_list = []
        self.dG_standby_site_list = []
        self.dG_total_list = []
        self.min_bp_prob_list = []
        self.kinetic_score_list = []
        self.three_state_indicator_list = []
        self.start_pos_list = []

    def calc_dG(self):
        """
        this function calculate the delta_G total
        """
        for start_pos, codon in self.find_start_codons(self.mRNA):
            if start_pos > constant.cutoff:
                self.dangles = 0
            else:
                self.dangles = 2
            self.md.dangles = self.dangles
            dG_start_codon = constant.start_codon_energies[codon]
            dG_mRNA, mRNA_structure = self.calc_dG_mRNA(start_pos)
            dG_mRNA_rRNA_withspacing, mRNA_rRNA_structure = self.calc_dG_mRNA_rRNA(start_pos)
            dG_mRNA_rRNA_nospacing = mRNA_rRNA_structure["dG_mRNA_rRNA"]
            dG_standby_site, corrected_structure = self.calc_dG_standby_site(mRNA_rRNA_structure)
            # dGmRNA:rRNA + dGstart - dGrRNA - dGmRNA - dGstandby_site
            dG_total = dG_mRNA_rRNA_withspacing + dG_start_codon - dG_mRNA - dG_standby_site
            kinetic_score, min_bp_prob = self.calc_kinetic_score(mRNA_structure)
            dG_SD_open = self.calc_dG_SDopen(mRNA_structure, mRNA_rRNA_structure)
            self.mRNA_structure_list.append(mRNA_structure)
            self.mRNA_rRNA_uncorrected_structure_list.append(mRNA_rRNA_structure)
            self.mRNA_rRNA_corrected_structure_list.append(corrected_structure)
            self.most_5p_mRNA_list.append(self.calc_most_5p_mRNA(mRNA_rRNA_structure))
            self.dG_start_energy_list.append(dG_start_codon)
            self.dG_mRNA_list.append(dG_mRNA)
            self.dG_mRNA_rRNA_list.append(dG_mRNA_rRNA_nospacing)
            self.dG_spacing_list.append(mRNA_rRNA_structure["dG_spacing"])
            self.dG_standby_site_list.append(dG_standby_site)
            self.dG_total_list.append(dG_total)
            self.min_bp_prob_list.append(min_bp_prob)
            self.kinetic_score_list.append(kinetic_score)
            self.three_state_indicator_list.append(dG_SD_open)
            self.start_pos_list.append(start_pos)

    def find_start_codons(self, sequence: str):
        """
        find the start codons of the RNA sequence
        :param sequence: RNA sequence
        :return: a generator that contains the index and position of all start codons
        """
        seq_len = len(sequence)
        end = min(self.start_codon_range[1], seq_len - 2)
        begin = min(self.start_codon_range[0], end)
        for i in range(begin, end + 1):
            codon = sequence[i:i + 3]
            if codon.upper() in constant.start_codons:
                yield i, codon
            else:
                pass

    def calc_dG_mRNA(self, start_pos: int) -> tuple:
        """
        calculate the delta_G of the mRNA
        :param start_pos: the position of the start codon
        :return: the tuple contains mfe value and the structure of the RNA fold compound
        """
        mRNA = self.mRNA[max(0, start_pos - constant.cutoff):min(len(self.mRNA), start_pos + constant.cutoff)]
        fc = RNA.fold_compound(mRNA, self.md)
        ss, mfe = fc.mfe()
        structure = {'mRNA': mRNA, 'mfe_res': fc.mfe()}
        return mfe, structure

    def calc_dG_rRNA(self) -> float:
        """
        calculate the delta_G of the rRNA
        :return: mfe value
        """
        fc = RNA.fold_compound(constant.rRNA, self.md)
        _, mfe = fc.mfe()
        return mfe

    def calc_dG_mRNA_rRNA(self, start_pos: int) -> tuple:
        """
        :param start_pos: the position of the start codon
        :return: a tuple contains delta_G withspacing of mRNA:rRNA and its RNA fold structure
        """
        begin = max(0, start_pos - constant.cutoff)
        mRNA_len = min(len(self.mRNA), start_pos + constant.cutoff)
        start_pos_in_subsequence = min(start_pos, constant.cutoff)
        startpos_to_end_len = mRNA_len - start_pos_in_subsequence - begin
        mRNA = self.mRNA[begin:start_pos]
        if len(mRNA) == 0:
            raise CalcError("There is a leaderless start codon, which is being ignored.")
        fc = RNA.fold_compound('&'.join([mRNA, constant.rRNA]), self.md)
        subopt_tuple = fc.subopt(constant.energy_cutoff)
        numbered_pairs = self.convert_subopt_bracket_to_numbered_pairs(subopt_tuple)
        if not numbered_pairs['bp_x']:
            raise CalcError('The 16S rRNA has no predicted binding site. Start codon is considered as leaderless and '
                            'ignored.')
        aligned_spacing = []
        for (bp_x, bp_y) in zip(numbered_pairs['bp_x'], numbered_pairs['bp_y']):
            aligned_spacing.append(self.calc_aligned_spacing(mRNA, start_pos_in_subsequence, bp_x, bp_y))
        dG_spacing_list = []
        dG_mRNA_rRNA = []
        dG_mRNA_rRNA_withspacing = []
        for i in range(len(numbered_pairs['bp_x'])):
            dG_mRNA_rRNA.append(numbered_pairs['energy'][i])
            dG_spacing = self.calc_dG_spacing(aligned_spacing[i])
            dG_spacing_list.append(dG_spacing)
            dG_mRNA_rRNA_withspacing.append(dG_spacing + numbered_pairs['energy'][i])
        min_index = dG_mRNA_rRNA_withspacing.index(min(dG_mRNA_rRNA_withspacing))
        dG_spacing_final = dG_spacing_list[min_index]
        most_5p_mRNA = sys.maxsize
        most_3p_mRNA = -sys.maxsize
        bp_x_target = []
        bp_y_target = []
        bp_x = numbered_pairs['bp_x'][min_index]
        bp_y = numbered_pairs['bp_y'][min_index]
        for (nt_x, nt_y) in zip(bp_x, bp_y):
            if nt_y > len(mRNA):  # nt is rRNA
                most_5p_mRNA = min(most_5p_mRNA, bp_x[bp_y.index(nt_y)])
                most_3p_mRNA = max(most_3p_mRNA, bp_x[bp_y.index(nt_y)])
                bp_x_target.append(nt_x)
                bp_y_target.append(nt_y)
        mRNA_pre = self.mRNA[begin:begin + most_5p_mRNA - 1]
        post_window_end = mRNA_len + 1
        post_window_begin = min(start_pos + constant.footprint, post_window_end)
        mRNA_post = self.mRNA[post_window_begin:post_window_end]
        total_bp_x = []
        total_bp_y = []
        if mRNA_pre:
            fc = RNA.fold_compound(mRNA_pre, self.md)
            fold_pre = self.convert_mfe_bracket_to_numbered_pairs(fc.mfe(), mRNA_pre)
            bp_x_pre = fold_pre['bp_x']
            bp_y_pre = fold_pre['bp_y']
        else:
            bp_x_pre = []
            bp_y_pre = []
        for nt_x, nt_y in zip(bp_x_pre, bp_y_pre):
            total_bp_x.append(nt_x)
            total_bp_y.append(nt_y)
        rRNA_offset = startpos_to_end_len
        for (nt_x, nt_y) in zip(bp_x_target, bp_y_target):
            total_bp_x.append(nt_x)
            total_bp_y.append(nt_y + rRNA_offset)
        if mRNA_post:
            fc = RNA.fold_compound(mRNA_post, self.md)
            fold_post = self.convert_mfe_bracket_to_numbered_pairs(fc.mfe(), mRNA_post)
            bp_x_post = fold_post['bp_x']
            bp_y_post = fold_post['bp_y']
        else:
            bp_x_post = []
            bp_y_post = []
        offset = post_window_begin - begin
        for (nt_x, nt_y) in zip(bp_x_post, bp_y_post):
            total_bp_x.append(nt_x + offset)
            total_bp_y.append(nt_y + offset)
        mRNA = self.mRNA[begin:mRNA_len]
        fc = RNA.fold_compound('&'.join([mRNA, constant.rRNA]), self.md)
        strands = [len(mRNA), len(constant.rRNA)]
        total_energy = fc.eval_structure(self.convert_numbered_pairs_to_bracket(strands, total_bp_x, total_bp_y))
        total_energy_withspacing = total_energy + dG_spacing_final
        structure = {'bp_x': total_bp_x, 'bp_y': total_bp_y, 'dG_mRNA_rRNA': total_energy,
                     'dG_spacing': dG_spacing_final, 'mRNA': mRNA}
        return total_energy_withspacing, structure

    @staticmethod
    def convert_subopt_bracket_to_numbered_pairs(subopt_tuple: tuple) -> dict:
        """
        convert subopt bracket to numbered pairs
        :param subopt_tuple: return of fc.subopt
        :return: the numbered pairs format of RNA fold structure
        """
        res = {'strands': [], 'bp_x': [], 'bp_y': [], 'energy': []}
        for subopt in subopt_tuple:
            bp_x = []
            strands = []
            bracket_string = subopt.structure
            bp_y = [[]] * bracket_string.count(")")
            last_nt_x_list = []
            counter = 0
            num_strands = 0
            for pos, letter in enumerate(bracket_string):
                if letter == ".":
                    counter += 1
                elif letter == "(":
                    bp_x.append(pos - num_strands)
                    last_nt_x_list.append(pos - num_strands)
                    counter += 1
                elif letter == ")":
                    nt_x = last_nt_x_list.pop()
                    nt_x_pos = bp_x.index(nt_x)
                    bp_y[nt_x_pos] = pos - num_strands
                    counter += 1
                elif letter == "&":
                    strands.append(counter)
                    counter = 0
                    num_strands += 1
                else:
                    raise CalcError('Invalid character in bracket notation.')
            if last_nt_x_list:
                raise CalcError('Leftover unpaired nucleotides when converting from bracket notation to numbered '
                                'base pairs.')
            strands.append(counter)
            bp_x = [pos + 1 for pos in bp_x[:]]
            bp_y = [pos + 1 for pos in bp_y[:]]
            res['strands'].append(strands)
            res['bp_x'].append(bp_x)
            res['bp_y'].append(bp_y)
            res['energy'].append(subopt.energy)
        return res

    @staticmethod
    def convert_mfe_bracket_to_numbered_pairs(mfe_res: list, sequence: str) -> dict:
        """
        convert mfe bracket to numbered_pairs
        :param mfe_res: return of fc.mfe
        :param sequence: the sequence of mRNA
        :return: numbered pairs format of RNA fold structure
        """
        res = {}
        bp_x = []
        strands = []
        if '&' in sequence:
            bracket_string = mfe_res[0][:sequence.index('&')] + '&' + mfe_res[0][sequence.index('&'):]
        else:
            bracket_string = mfe_res[0]
        bp_y = [[]] * bracket_string.count(")")
        last_nt_x_list = []
        counter = 0
        num_strands = 0
        for pos, letter in enumerate(bracket_string[:]):
            if letter == ".":
                counter += 1
            elif letter == "(":
                bp_x.append(pos - num_strands)
                last_nt_x_list.append(pos - num_strands)
                counter += 1
            elif letter == ")":
                nt_x = last_nt_x_list.pop()
                nt_x_pos = bp_x.index(nt_x)
                bp_y[nt_x_pos] = pos - num_strands
                counter += 1
            elif letter == "&":
                strands.append(counter)
                counter = 0
                num_strands += 1
            else:
                raise CalcError('Invalid character in bracket notation.')
        if last_nt_x_list:
            raise CalcError('Leftover unpaired nucleotides when converting from bracket notation to numbered base '
                            'pairs.')
        strands.append(counter)
        bp_x = [pos + 1 for pos in bp_x[:]]
        bp_y = [pos + 1 for pos in bp_y[:]]
        res['strands'] = strands
        res['bp_x'] = bp_x
        res['bp_y'] = bp_y
        res['energy'] = mfe_res[1]
        return res

    @staticmethod
    def convert_numbered_pairs_to_bracket(strands: list, bp_x: list, bp_y: list) -> str:
        """
        convert numbered pairs to bracket
        :param strands: the list contains strands information of RNA sequence
        :param bp_x: a list contains base pairing position x
        :param bp_y: a list contains base pairing position y
        :return: bracket format of RNA
        """
        bp_x = [pos - 1 for pos in bp_x]
        bp_y = [pos - 1 for pos in bp_y]
        bracket_notation = []
        counter = 0
        for strand_number, seq_len in enumerate(strands):
            # if strand_number > 0:
            # bracket_notation.append("&")
            for pos in range(counter, seq_len + counter):
                if pos in bp_x:
                    bracket_notation.append("(")
                elif pos in bp_y:
                    bracket_notation.append(")")
                else:
                    bracket_notation.append(".")
            counter += seq_len
        return ''.join(bracket_notation)

    @staticmethod
    def calc_aligned_spacing(mRNA: str, start_pos: int, bp_x: list, bp_y: list) -> int:
        """
        this function calculate aligned spacing of the mRNA
        :param mRNA: mRNA sequence
        :param start_pos: the position of the start codon
        :param bp_x: a list contains base pairing position x
        :param bp_y: a list contains base pairing position y
        :return: aligned spacing
        """
        flag = False
        seq_len = len(mRNA) + len(constant.rRNA)
        distance_to_start, farthest_3_prime_rRNA = 0, 0
        for rRNA_nt in range(seq_len, seq_len - len(constant.rRNA), -1):
            if rRNA_nt in bp_y:
                rRNA_pos = bp_y.index(rRNA_nt)
                if bp_x[rRNA_pos] < start_pos:
                    flag = True
                    farthest_3_prime_rRNA = rRNA_nt - len(mRNA)
                    mRNA_nt = bp_x[rRNA_pos]
                    distance_to_start = start_pos - mRNA_nt + 1
                    break
                else:
                    break
        if flag:
            aligned_spacing = distance_to_start - farthest_3_prime_rRNA
        else:
            aligned_spacing = sys.maxsize
        return aligned_spacing

    @staticmethod
    def calc_dG_spacing(aligned_spacing: int) -> float:
        """
        this function calculates the delta_G of spacing
        :param aligned_spacing: aligned spacing
        :return: delta_G of spacing
        """
        if aligned_spacing < constant.optimal_spacing:
            ds = aligned_spacing - constant.optimal_spacing
            dG_spacing_penalty = constant.dG_spacing_constant_push[0] / (1.0 + math.exp(
                constant.dG_spacing_constant_push[1] * (ds + constant.dG_spacing_constant_push[2]))) \
                                 ** constant.dG_spacing_constant_push[3]
        else:
            ds = aligned_spacing - constant.optimal_spacing
            dG_spacing_penalty = constant.dG_spacing_constant_pull[0] * ds * ds + constant.dG_spacing_constant_pull[
                1] * ds + constant.dG_spacing_constant_pull[2]
        return dG_spacing_penalty

    def calc_dG_standby_site(self, structure_old: dict) -> tuple:
        """
        this function calculate the delta_G of the standby site
        :param structure_old: the old RNA fold structure
        :return: a tuple contains delta_G of standby site and its RNA fold structure
        """
        structure = deepcopy(structure_old)
        mRNA = structure["mRNA"]
        bp_x = structure["bp_x"]
        bp_y = structure["bp_y"]
        energy_before = structure["dG_mRNA_rRNA"]
        most_5p_mRNA = 0
        for nt_x, nt_y in zip(bp_x, bp_y):
            if nt_x <= len(mRNA) < nt_y:
                most_5p_mRNA = nt_x
                break
        bp_x_3p = []
        bp_y_3p = []
        for (nt_x, nt_y) in zip(bp_x, bp_y):
            if nt_x >= most_5p_mRNA:
                bp_x_3p.append(nt_x)
                bp_y_3p.append(nt_y)
        mRNA_subsequence = mRNA[0:max(0, most_5p_mRNA - constant.standby_site_length - 1)]
        if mRNA_subsequence:
            fc = RNA.fold_compound(mRNA_subsequence, self.md)
            fold = self.convert_mfe_bracket_to_numbered_pairs(fc.mfe(), mRNA_subsequence)
            bp_x_5p = fold['bp_x']
            bp_y_5p = fold['bp_y']
        else:
            bp_x_5p = []
            bp_y_5p = []
        bp_x_after = []
        bp_y_after = []
        for (nt_x, nt_y) in zip(bp_x_5p, bp_y_5p):
            bp_x_after.append(nt_x)
            bp_y_after.append(nt_y)
        for (nt_x, nt_y) in zip(bp_x_3p, bp_y_3p):
            bp_x_after.append(nt_x)
            bp_y_after.append(nt_y)
        fc = RNA.fold_compound('&'.join([mRNA, constant.rRNA]), self.md)
        strands = [len(mRNA), len(constant.rRNA)]
        energy_after = fc.eval_structure(self.convert_numbered_pairs_to_bracket(strands, bp_x_after, bp_y_after))
        dG_standby_site = energy_before - energy_after
        dG_standby_site = min(dG_standby_site, 0)
        structure = {'bp_x': bp_x_after, 'bp_y': bp_y_after}
        return dG_standby_site, structure

    def calc_kinetic_score(self, structure: dict = None, mRNA_in: str = None, bp_x_in: list = None,
                           bp_y_in: list = None) -> tuple:
        '''
        this function claculates kinetic score and min base pairing probability. You can just input structure or input
        mRNA_in, bp_x_in and bp_y_in.
        :param structure: the structure of RNA fold
        :param mRNA_in: the inputted mRNA sequence
        :param bp_x_in: the inputed list contains base pairing position x
        :param bp_y_in: the inputed list contains base pairing position y
        :return: tuple contains kinetic score and min base pairing probability
        '''
        if structure:
            mRNA = structure["mRNA"]
            mfe_res = structure['mfe_res']
            fold = self.convert_mfe_bracket_to_numbered_pairs(mfe_res, mRNA)
            bp_x = fold['bp_x']
            bp_y = fold['bp_y']
        elif mRNA_in and bp_x_in and bp_y_in:
            mRNA = mRNA_in
            bp_x = bp_x_in
            bp_y = bp_y_in
        else:
            raise CalcError('No valid structure or basepair inputted.')
        largest_range_helix = 0
        for nt_x, nt_y in zip(bp_x, bp_y):
            if nt_x <= len(mRNA) and nt_y <= len(mRNA):
                val = nt_y - nt_x
                largest_range_helix = max(val, largest_range_helix)
        kinetic_score = float(largest_range_helix) / float(len(mRNA))
        if float(largest_range_helix) > 0:
            min_bp_prob = float(largest_range_helix) ** (-1.44)
        else:
            min_bp_prob = 1.0
        return kinetic_score, min_bp_prob

    def calc_dG_SDopen(self, mRNA_structure: dict, mRNA_rRNA_structure: dict) -> float:
        """
        this function calculates deltaG of opening SD sequence
        :param mRNA_structure: the RNA fold structure of mRNA
        :param mRNA_rRNA_structure: the RNA fold structure of mRNA:rRMA
        :return: deltaG of opening SD sequence
        """
        mRNA = mRNA_structure['mRNA']
        dG_mRNA = mRNA_structure['mfe_res'][1]
        bp_x_1 = mRNA_rRNA_structure['bp_x']
        bp_y_1 = mRNA_rRNA_structure['bp_y']
        most_5p_mRNA = sys.maxsize
        most_3p_mRNA = -sys.maxsize
        for nt_x, nt_y in zip(bp_x_1, bp_y_1):
            # nt_y is rRNA
            if nt_y > len(mRNA):
                most_5p_mRNA = min(most_5p_mRNA, bp_x_1[bp_y_1.index(nt_y)])
                most_3p_mRNA = max(most_3p_mRNA, bp_x_1[bp_y_1.index(nt_y)])
        pre_mRNA = mRNA[0:most_5p_mRNA]
        post_mRNA = mRNA[most_3p_mRNA + 1:len(mRNA) + 1]
        fc = RNA.fold_compound(pre_mRNA, self.md)
        _, dG_pre = fc.mfe()
        fc = RNA.fold_compound(post_mRNA, self.md)
        _, dG_post = fc.mfe()
        energy = dG_pre + dG_post
        ddG_mRNA = energy - dG_mRNA
        return ddG_mRNA

    @staticmethod
    def calc_most_5p_mRNA(structure_old: dict) -> int:
        """
        this function calculates the most 5-prime nucleotide of mRNA
        :param structure_old: the RNA fold structure
        :return: the position of the most 5-prime nucleotide of mRNA
        """
        structure = deepcopy(structure_old)
        mRNA = structure["mRNA"]
        bp_x = structure["bp_x"]
        bp_y = structure["bp_y"]
        for nt_x, nt_y in zip(bp_x, bp_y):
            # nt_x is mRNA, nt_y is rRNA, they are bound.
            if nt_x <= len(mRNA) < nt_y:
                return nt_x

    def calc_longest_loop_bulge(self, structure: dict, output_start_end: bool = False, in_rbs_only: bool = False,
                                rbs: str = None) -> tuple:
        """
        this function calclates longest loop bulge
        :param structure: RNA fold structure
        :param output_start_end: bool, if it is True, start and end of the loop bulge will be returned
        :param in_rbs_only: bool, if it is True, only considers RBS
        :param rbs: the sequence of RBS
        :return: a tuple contains results
        """
        mRNA = structure['mRNA']
        mfe_res = structure['mfe_res']
        fold = self.convert_mfe_bracket_to_numbered_pairs(mfe_res, mRNA)
        bp_x = fold["bp_x"]
        bp_y = fold["bp_y"]
        loop_length = 0
        begin_helix = 1
        end_helix = 1
        bulge_loop_list = []
        helical_loop_list = []
        if output_start_end:
            bulge_loop_start_end = []
            helical_loop_start_end = []
        if in_rbs_only and rbs:
            RBS_begin = mRNA.find(rbs)
            RBS_end = RBS_begin + len(rbs)
            nucleotide_range = range(RBS_begin, RBS_end + 1)
        else:
            nucleotide_range = range(1, len(mRNA) + 1)
        # find loops
        for n in nucleotide_range:
            if bp_x.count(n) == 0 and bp_y.count(n) == 0:
                # determine if nearest neighbor nucleotides are base-paired
                x1, x2, y1, y2 = (bp_x.count(n - 1), bp_x.count(n + 1), bp_y.count(n - 1), bp_y.count(n + 1))
                # middle unpaired nt
                if (x1, x2, y1, y2) == (0, 0, 0, 0):
                    loop_length += 1
                # single mismatch -- loop
                elif (x1, x2, y1, y2) == (1, 0, 0, 1) or (x1, x2, y1, y2) == (0, 1, 1, 0):
                    loop_length += 1
                    begin_helix = n - 1
                    end_helix = n + 1
                # single mismatch -- bulge
                elif (x1, x2, y1, y2) == (1, 1, 0, 0) or (x1, x2, y1, y2) == (0, 0, 1, 1):
                    loop_length += 1
                    begin_helix = n - 1
                    end_helix = n + 1
                # starting unpaired nt
                elif (x1, x2, y1, y2) == (1, 0, 0, 0) or (x1, x2, y1, y2) == (0, 0, 1, 0):
                    loop_length += 1
                    begin_helix = n - 1
                # ending unpaired nt
                elif (x1, x2, y1, y2) == (0, 1, 0, 0) or (x1, x2, y1, y2) == (0, 0, 0, 1):
                    loop_length += 1
                    end_helix = n + 1
            elif loop_length > 0:
                if bp_x.count(begin_helix) > 0 and bp_y.count(end_helix) > 0 and bp_x.index(begin_helix) == bp_y.index(
                        end_helix):
                    helical_loop_list.append(loop_length)
                    loop_length = 0
                    if output_start_end:
                        helical_loop_start_end.append((begin_helix, end_helix))
                else:
                    bp_end = 0
                    bp_begin = 0
                    if bp_x.count(end_helix) > 0: bp_begin = bp_y[bp_x.index(end_helix)]
                    if bp_y.count(end_helix) > 0: bp_end = bp_x[bp_y.index(end_helix)]
                    if bp_end > bp_begin:
                        bulge_loop_list.append(loop_length)
                        loop_length = 0
                        if output_start_end:
                            bulge_loop_start_end.append((begin_helix, end_helix))
                    else:
                        loop_length = 0
        if output_start_end:
            return helical_loop_list, bulge_loop_list, helical_loop_start_end, bulge_loop_start_end
        else:
            return helical_loop_list, bulge_loop_list
