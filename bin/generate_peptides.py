#!/usr/bin/env python3
####################################################################################################
#
# Author: Sabrina Krakau, Leon Kuchenbecker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

import sys
import gzip
import csv
import pandas as pd
#import tqdm
import io
import argparse
import time

from Bio import SeqIO
from pprint import pprint
from datetime import datetime
from collections import Counter

import sys


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--proteins", required=True, metavar='FILE', help="Compressed TSV file containing: protein_id, protein_sequence.")
    parser.add_argument('-min', "--min_len", required=True, metavar='N', type=int, help="Min. peptide length.")
    parser.add_argument('-max', "--max_len", required=True, metavar='N', type=int, help="Max. peptide length.")
    parser.add_argument('-p', '--peptides', required=True, metavar='FILE', help='Output file containing: peptide_id, peptide_sequence.') # use str type to allow compression of output
    parser.add_argument('-pp', '--proteins_peptides', required=True, metavar='FILE', type=argparse.FileType('w'), help='Output file containing: protein_id, peptide_id, count.')
    parser.add_argument('-l', '--proteins_lengths', required=True, metavar='FILE', type=argparse.FileType('w'), help='Output file containing: protein_id, protein_length.')
    return parser.parse_args(args)

def gen_peptides(prot_seq, k):
    return [ prot_seq[i:(i+k)] for i in range(len(prot_seq)-k+1) ]


def main(args=None):
    args = parse_args(args)

    protid_protseq_protlen = pd.read_csv(args.proteins, sep="\t")
    protid_protseq_protlen["protein_length"] = protid_protseq_protlen["protein_sequence"].apply(len)
    print("# proteins: ", len(protid_protseq_protlen))

    # write out protein lengths
    protid_protseq_protlen[['protein_id', 'protein_length']].to_csv(args.proteins_lengths, sep="\t", index=False)

    ####################
    # generate peptides

    with gzip.open(args.peptides, 'wt') as pep_handle:
        print('peptide_id', 'peptide_sequence', sep='\t', file=pep_handle, flush=True)
        print('protein_id', 'peptide_id', 'count', sep='\t', file=args.proteins_peptides, flush=True)
        id_counter = 0
        # for each k
        for k in range(args.min_len, args.max_len + 1):
            print("Generate peptides of length ", k, " ...", flush=True)
            # for each protein generate all peptides of length k

            results = pd.DataFrame(
                [ (str(it.protein_id), pep) for it in protid_protseq_protlen.itertuples() for pep in gen_peptides(it.protein_sequence, k) ],
                columns = ['protein_id','peptide_sequence']
                )

            # TODO handle this more memory efficiently
            print("format results ...", flush=True)
            # count occurences of one peptide in one protein
            results = results.groupby(['protein_id','peptide_sequence']).size().reset_index(name='count')

            unique_peptides = results[['peptide_sequence']].drop_duplicates()
            unique_peptides["peptide_id"] = range(id_counter, id_counter+len(unique_peptides))
            id_counter += len(unique_peptides)
            unique_peptides[['peptide_id', 'peptide_sequence']].to_csv(pep_handle, mode='a', sep="\t", index=False, header=False)

            results = results.merge(unique_peptides)
            results[['protein_id', 'peptide_id', 'count']].to_csv(args.proteins_peptides, mode='a', sep="\t", index=False, header=False)

            print("# peptides of length ", k, ", (non-unique across proteins): ", len(results))

    print("Done!", flush=True)


if __name__ == "__main__":
    sys.exit(main())
