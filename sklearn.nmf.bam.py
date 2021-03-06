#!/bin/python

import argparse

parser = argparse.ArgumentParser(description='filter bam based on QNAMES')
parser.add_argument('--bam', type=str, dest="bam", help='bam file')
parser.add_argument('--statH', type=str, dest="statH", help='input statH matrix')
parser.add_argument('-o', '--outPrefix', type=str, dest="outPrefix", help='output prefix')

args = parser.parse_args()

import numpy as np
import pysam
from time import perf_counter as pc

def run():
	""" Run standard NMF on rank """
	start_time = pc()
	""" init input files """
	bamf = args.bam
	statHf = args.statH
	outPrefix = args.outPrefix
	print("filter out bam files")
	generate_bam(bamf, statHf, outPrefix)
	end_time = pc()
	print('Used (secs): ', end_time - start_time)

def generate_bam(bamf, statHf, prefix):
	o_stat_H = np.genfromtxt(statHf, dtype=None, names=True)
	rank = np.max(o_stat_H['class0']).astype(int) + 1
	for r in range(rank):
		bamF = pysam.AlignmentFile(bamf)
		qnames = list(o_stat_H[np.where(o_stat_H['class0']==r)]['xgi'].astype(str))
		qnames_set = set(qnames)
		n = r + 1
		bam_fname = prefix + "." + "metacell_" + str(n) + "." + "bam"
		print("For metaCell =", n, "The filtered bam is writing to:", bam_fname)
		obam = pysam.AlignmentFile(bam_fname, "wb", template=bamF)
		for b in bamF.fetch(until_eof=True):
			if b.query_name.split(':')[0] in qnames_set:
				obam.write(b)
		obam.close()
		bamF.close()

if __name__ == "__main__":
	"""filter bam based on QNAMES"""
	run()
