# chord-matrix

## Overview
`chord-matrix` is a Python package designed to process gene expression data and generate a co-occurrence matrix. This matrix can then be utilized to create chord diagrams, providing a visual representation of the co-occurrences between different gene mutations.

## Features
- **Data Processing**: Reads gene expression data from a TSV file and filters it based on specific criteria.
- **Co-occurrence Matrix**: Creates a matrix showing the co-occurrence of gene mutations across samples.
- **Details Calculation**: Computes various statistics, including odds ratios and tendencies for mutual exclusivity or co-occurrence.
- **Output**: Generates a detailed output file including the co-occurrence matrix and the computed statistics.

## Installation

### Prerequisites
Ensure you have Python 3.6 or higher installed on your system.

### Using pip
You can install `chord-matrix` using pip:

```bash
pip install chord-matrix
```

## The logic behind

### Data Reading and Filtering
The input data file is read and filtered based on a specific status (RMG_53). Only the necessary columns (UPN, AF, and SYMBOL) are retained, and duplicates are removed. 
Customize the filtering according to your requirements.

### Matrix Creation
The filtered data is used to create a pivot table where rows represent gene symbols and columns represent patient id(UPN). The presence of a mutation is indicated by 1, and the absence by 0.

### Why use the dot product?
To generate the co-occurrence matrix, we use matrix multiplication (dot product) of the gene-patient matrix with its transpose. This process is fundamental in identifying how many times pairs of genes co-occur across all patients.

The dot product of two binary vectors (gene presence/absence vectors) results in a scalar value representing the number of times both genes are mutated in the same patient. By performing this operation for each pair of genes, we can construct a full co-occurrence matrix that quantifies the co-occurrences of all gene pairs across the dataset.

### Details Calculation
The package calculates several statistics for each pair of genes, including:

* Both: Number of samples with both genes mutated.
* A Not B: Number of samples with only gene A mutated.
* B Not A: Number of samples with only gene B mutated.
* Neither: Number of samples with neither gene mutated.
* Log2 Odds Ratio: Log2 of the odds ratio indicating the tendency for co-occurrence or mutual exclusivity.