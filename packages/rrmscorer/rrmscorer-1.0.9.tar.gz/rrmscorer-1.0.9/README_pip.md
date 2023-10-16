# RRMScorer documentation
RRMScorer allows the user to easily predict how likely a single RRM is to bind ssRNA using a carefully generated alignment for the RRM structures in complex with RNA, from which we analyzed the interaction patterns and derived the scores (Please address to the publication for more details on the method REF)

**🔗 RRMScorer is also available online now! (https://bio2byte.be/rrmscorer/)**

### Pip package installation
> pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

**🔗 Related link:** [Pip official documentation](https://pypi.org/).

```console
$ pip install rrmscorer
```

**⚠️ Important note:**
Apple silicon users may need to install the package in a Rosetta environment, using conda for isntance, bacause some packages are not available for the silicon architecture yet.
```console
$ CONDA_SUBDIR=osx-64 conda create -n rosetta_environment
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
$ python -m rrmscorer -u P19339 -r UAUAUUAGUAGUA -w 5 -j output/ -c output/ -p output/
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
$ python -m rrmscorer -f input_files/rrm_seq.fasta -r UAUAUUAGUAGUA -c output/
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
$ python -m rrmscorer -f input_files/rrm_seq.fasta -w 5 -top -j output/
```

## 📖 How to cite
If you use this package or data in this package, please cite:

| Predictor | Cite                                                                                                                                                         | Link                                      |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| RRMScorer | Roca-Martínez J, Dhondge H, Sattler M, Vranken WF. Deciphering the RRM-RNA recognition code: A computational analysis. PLoS Comput Biol. 2023 Jan 23;19(1)   | https://pubmed.ncbi.nlm.nih.gov/36689472/ |

