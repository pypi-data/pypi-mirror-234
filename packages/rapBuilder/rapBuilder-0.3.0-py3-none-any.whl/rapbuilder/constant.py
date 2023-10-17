"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : constant.py
@Author : Zhiyue Chen
@Time : 2023/8/24 0:35
"""
# From experimental characterization from Salis, H. M., Mirsky, E. A., & Voigt, C. A. (2009). Automated design of
# synthetic ribosome binding sites to control protein expression. Nature Biotechnology, 27(10), Article 10.
RT_eff = 2.222
logK = 7.824
K = 2500.0

# dG ranges
dG_range_high = 25.0
dG_range_low = -18.0
# aligned spacing
optimal_spacing = 5
# number of nt before SD sequence that must be unpaired for ribosome binding
standby_site_length = 4

dG_spacing_constant_push = [12.2, 2.5, 2.0, 3.0]
dG_spacing_constant_pull = [0.048, 0.24, 0.0]

# number of nt +- start codon considering for folding
cutoff = 35
energy_cutoff = 300

# #Footprint of the 30S complex that prevents formation of secondary structures downstream of the start codon. Here,
# we assume that the entire post-start RNA sequence does not form secondary structures once the 30S complex has bound.
footprint = 1000


nucleotides = {'A', 'T', 'G', 'C'}
# SD sequence
SD = ["T", "A", "A", "G", "G", "A", "G", "G", "T"]
# last 9 nt (3' end) of the 16S rRNA in E. coli
rRNA = "ACCUCCUUA"
# substituted U for T in actual calGGcs. Ignores CTG/CUG
start_codons = ["ATG", "AUG", "GTG", "GUG", "TTG", "UUG"]
# hybridization to CAT
start_codon_energies = {"ATG": -1.194, "AUG": -1.194, "GTG": -0.0748, "GUG": -0.0748, "TTG": -0.0435, "UUG": -0.0435,
                        "CTG": -0.03406, "CUG": -0.03406}
# Stem loop sequence
pre_seq_stem_loop = 'AAACACCCACCACAATTTCCACCGTTT'
stem_loop = 'CCCGACGCTTCGGCGTCGGG'
cutoff_stem_loop = 30