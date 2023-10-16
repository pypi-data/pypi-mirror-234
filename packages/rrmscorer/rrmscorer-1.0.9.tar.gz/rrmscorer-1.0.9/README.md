# RRMScorer documentation
RRMScorer allows the user to easily predict how likely a single RRM is to bind ssRNA using a carefully generated alignment for the RRM structures in complex with RNA, from which we analyzed the interaction patterns and derived the scores (Please address to the publication for more details on the method REF)

---

## Installation

#### Clone this repository to your working environment:
```console
$ git clone git@bitbucket.org:bio2byte/rrmscorer.git && cd rrmscorer
```

#### The following packages are required:

```python
python==3.10.4
numpy==1.22.3
pandas==1.4.2
biopython==1.79
matplotlib==3.5.2
scikit-learn==1.1.1
hmmer==3.3.2
logomaker==0.8
```
#### Via [Conda](https://docs.conda.io/en/latest/):

```console
$ conda create --yes --name rrmscorer python==3.10.4
$ conda activate rrmscorer
$ conda install --yes --file requirements.txt
```

#### Via [Virtual Environment](https://docs.python.org/3/tutorial/venv.html):

```console
$ python3 -m venv rrmscorer-venv
$ source ./rrmscorer-venv/bin/activate
$ python -m pip install numpy==1.21.5 pandas==1.4.2 biopython==1.79 matplotlib==3.5.2 scikit-learn==1.1.1 logomaker==0.8 hmmer
```

## How to run it:
Either you are using Conda or Virtual Environments for your installation, before executing this software features, you need to setup the Python environment.
Using Conda:

```console
$ conda activate rrmscorer
```
Using Virtual Environment:

```console
$ source ./rrmscorer-venv/bin/activate
```

Continue reading the next section to find further details about the available features.
In case you need to deactivate this Python environment:

Using Conda:

```console
$ conda deactivate
```

Using Virtual Environment:

```console
$ deactivate
```

## Features
RRMScorer has several features to either calculate the binding score for a specific RRM and RNA sequences, for a set of RRM sequences in a fasta file, or to explore which are the best RNA binders according to our scoring method.

### i) UniProt id (with 1 or more RRMs) vs RNA
To use this feature the user needs to input:

1. `-u` The UniProt identifier 
2. `-r` The RNA sequence to score
3. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM


```console
$ python rrm_rna_wrapper.py -u P19339 -r UAUAUUAGUAGUA -w 5 -j output/ -c output/ -p output/
```

Example output:
```console
UAUAU -1.08
AUAUU -0.99
UAUUA -1.33
AUUAG -0.90
UUAGU -1.07
```

### ii) Fasta file with RRM sequences vs RNA
To use this feature the user needs to input:

1. `-f` Fasta file with 1 or more RRM sequences. The sequences are aligned to the master alignment HMM.
1. `-r` The RNA sequence to test
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM

```console
$ python rrm_rna_wrapper.py -f input_files/rrm_seq.fasta -r UAUAUUAGUAGUA -c output/
```


### iii) Fasta file / UniProt id to find top-scoring RNAs
To use this feature the user needs to input:

1. `-f` Fasta file or UniProt Id is as described in the previous cases.
1. `-w` [default=5] The window size to test (**Only 3 and 5 nucleotide windows are accepted**)
1. `-t` To find the top-scoring RNA for the specified RRM/s
4. `-j` [Optional] To store the results in a json file per RRM found in the declared directory path
5. `-c` [Optional] To store the results in a csv file per RRM found in the declared directory path
6. `-p` [Optional] To generate score plots for all the RNA possible windows per RRM found in the declared directory path
7. `-a` [Optional] To generate a fasta file with each input sequence aligned to the HMM

```console
$ python rrm_rna_wrapper.py -f input_files/rrm_seq.fasta -ws 5 -top -j output/
```



