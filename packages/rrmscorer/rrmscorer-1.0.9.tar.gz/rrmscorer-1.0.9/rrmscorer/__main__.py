# Python wrapper to have available all the scoring classes in one place and
# merge the results​
import os
import sys
import csv
import json
import argparse

from .rrm_rna_functions import RNAScoring, HMMScanner, LogoGenerator

__version__ = "1.0.9"

def main():
    print("Executing rrmscorer version %s." % __version__)

    usr_input_handler = UserInputHandler()
    usr_input = usr_input_handler.parse_args()

    Manager(usr_input).input_handler()

class Manager():
    STANDARD_AMINO_ACIDS = {
            "A", "C", "D", "E", "F", "G", "H", "I", "K",
            "L", "M", "N", "P", "Q", "R", "S", "T", "V",
            "W", "Y"}
    STANDARD_RNA_NUCLEOTIDES = {"A", "C", "G", "U"}
    N_MERS = [10, 50, 100, 250]

    # This is the general input manager of the scoring framework
    def __init__(self, usr_input):
        self.usr_input = usr_input
        self._rna_scoring = None
        self._hmm_scan = None
        self._logo_gen = None

    @property
    def rna_scoring(self):
        if not self._rna_scoring:
            self._rna_scoring = RNAScoring()

        return self._rna_scoring

    @property
    def hmm_scan(self):
        if not self._hmm_scan:
            self._hmm_scan = HMMScanner()

        return self._hmm_scan

    @property
    def logo_gen(self):
        if not self._logo_gen:
            self._logo_gen = LogoGenerator()

        return self._logo_gen

    def input_handler(self):
        if self.usr_input.fasta_file:
            seqs_dict = self.hmm_scan.hmmalign_RRMs(
                fasta_file=self.usr_input.fasta_file)

        elif self.usr_input.UP_id:
            seqs_dict = self.hmm_scan.get_UP_seq(
                UP_id=self.usr_input.UP_id)

        for seq_id, seq in seqs_dict.items():
            self.handle_sequence(seq_id, seq)
            if self.usr_input.aligned:
                with open(
                        self.usr_input.aligned + "/" + seq_id.replace(
                            "/", "_").replace("|", "_") + "_aligned" + ".fasta", "w") as aln_out:
                    aln_out.write(">{}\n{}\n".format(seq_id, seq))


    def handle_sequence(self, seq_id, seq):
        set_seq = set(seq.upper())
        set_seq.remove("-")
        if set_seq.issubset(Manager.STANDARD_AMINO_ACIDS):
            pass
        else:
            print("\033[91m[ERROR] The protein sequence contains"
                      " non-standard amino acids.\033[0m")
            sys.exit()
        seq_id = seq_id.replace("/", "_").replace("|", "_")
        print("\nRunning predictions for {}...".format(seq_id))
        if self.usr_input.top:
            top_scores = self.rna_scoring.find_best_rna(rrm_seq=seq)

            if self.usr_input.json:
                json_path = os.path.join(os.path.abspath(self.usr_input.json), f"{seq_id}_top_scorers.json")
                with open(json_path, "w") as fp:
                    json.dump(top_scores, fp, indent=2)
                    print("Json file successfully saved in {}".format(
                            json_path))

            if self.usr_input.plot:
                for n_mers in Manager.N_MERS: # Right line
                    plot_path = os.path.join(os.path.abspath(self.usr_input.plot), f"{seq_id}_top_{n_mers}_logo.png")
                    self.logo_gen.generate_logo_to_file(plot_path, top_scores, n_mers, self.usr_input.window_size)
                    print("Plot successfully saved in {}".format(plot_path))

        elif self.usr_input.rna_seq:
            if not set(self.usr_input.rna_seq).issubset(Manager.STANDARD_RNA_NUCLEOTIDES):
                print("\033[91m[ERROR] The RNA sequence contains"
                          " non-standard RNA nucleotides.\033[0m")
                sys.exit("Invalid input parameters")

            self.rna_scoring.score_out_seq(
                    rrm_seq=seq, rna_seq=self.usr_input.rna_seq,
                    rna_pos_range=self.usr_input.rna_pos_range)

            for key, score in self.rna_scoring.scores_dict.items():
                print(key, score)

            if self.usr_input.json:
                json_path = os.path.join(os.path.abspath(self.usr_input.json), f"{seq_id}.json")
                with open(json_path, "w") as fp:
                    json.dump(self.rna_scoring.scores_dict, fp, indent=2)
                    print("Json file successfully saved in {}".format(json_path))

            if self.usr_input.csv:
                csv_path = os.path.join(os.path.abspath(self.usr_input.csv), f"{seq_id}.csv")
                with open(csv_path, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in self.rna_scoring.scores_dict.items():
                        writer.writerow([key, value])
                    print("CSV file successfully saved in {}".format(csv_path))

            if self.usr_input.plot:
                plot_path = os.path.join(os.path.abspath(self.usr_input.plot), f"{seq_id}.png")
                self.rna_scoring.plot_rna_kde_to_file(self.usr_input.rna_seq, self.usr_input.window_size, plot_path)
                print("Plot successfully saved in {}".format(plot_path))

class UserInputHandler():
    def __init__(self):
        self.parser = self._build_parser()

    def _build_parser(self):
        parser = argparse.ArgumentParser(description=f'RRM-RNA scoring version {__version__}')

        input_arg = parser.add_mutually_exclusive_group(required=True)
        input_arg.add_argument('-u', '--uniprot', help='UniProt identifier',
                               metavar='UNIPROT_ID')
        input_arg.add_argument('-f', '--fasta', help='Fasta file path',
                               metavar='/path/to/input.fasta')

        feat_arg = parser.add_mutually_exclusive_group(required=True)
        feat_arg.add_argument('-r', '--rna', help='RNA sequence',
                              metavar='RNA_SEQUENCE')
        feat_arg.add_argument('-t', '--top', action="store_true",
                              help='To find the top scoring RNA fragments')

        parser.add_argument('-w', '--window_size', required=False,
                            help='The window size to test', metavar='N')
        parser.add_argument('-j', '--json',
                            help='Store the results in a json file in the declared directory path',
                            metavar='/path/to/output')
        parser.add_argument('-c', '--csv',
                            help='Store the results in a CSV file in the declared directory path',
                            metavar='/path/to/output')
        parser.add_argument('-p', '--plot',
                            help='Store the plots in the declared directory path',
                            metavar='/path/to/output')
        parser.add_argument('-a', '--aligned',
                            help='Store the aligned sequences in the declared directory path',
                            metavar='/path/to/output')
        parser.add_argument('-v', '--version', action='version',
                            help='show RRM-RNA scoring version number and exit',
            version=f'RRM-RNA scoring {__version__}')

        return parser

    def parse_args(self):
        usr_input = UserInput()

        input_files = self.parser.parse_args()

        usr_input.fasta_file = input_files.fasta
        usr_input.UP_id = input_files.uniprot

        usr_input.rna_seq = input_files.rna
        usr_input.top = input_files.top

        # User defined outputs
        usr_input.json = input_files.json
        usr_input.csv = input_files.csv
        usr_input.plot = input_files.plot
        usr_input.aligned = input_files.aligned

        # Default window size
        if input_files.window_size:
            usr_input.window_size = int(input_files.window_size)

            if usr_input.window_size == 3:
                usr_input.rna_pos_range = (3, 6)

            elif usr_input.window_size == 5:
                usr_input.rna_pos_range = (2, 7)

            else:
                sys.exit('Only 3 and 5 nucleotide windows are accepted')
        else:  # Default ws=5 if not in input
            usr_input.window_size = 5
            usr_input.rna_pos_range = (2, 7)

        return usr_input

class UserInput():
    def __init__(self):
        self.fasta_file = None
        self.UP_id = None
        self.rna_seq = None
        self.top = None
        self.json = None
        self.csv = None
        self.plot = None
        self.window_size = None
        self.rna_pos_range = None

if __name__ == '__main__':
    main()