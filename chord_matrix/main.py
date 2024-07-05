import pandas as pd
import numpy as np
import argparse
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process the data files for PCA analysis.", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # mandatory arguments
    parser.add_argument("--path", required=True, help="Path to the main data file in TSV format")
    parser.add_argument("--outputPath", required=True, help="Path to download the output matrix file.")

    return parser.parse_args()

def check_directories(target_dir, output_dir):
    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)


def make_matrix(target_dir, output_dir):
    # file_location = "C:\\Habib_wustl\\summer_2024\\Habib_updates\\20220918_ARCHb7_re_Tumor_only.tsv"
    # output_file_location = "C:\\Habib_wustl\\summer_2024\\Habib_updates\\chord_data.tsv"
    df = pd.read_csv(target_dir, sep='\t', low_memory=False)
    df = df[df['status'] == 'RMG_53']
    filtered_df = df[["UPN", "AF", "SYMBOL"]]
    filtered_df = filtered_df.drop_duplicates(subset=['UPN', 'SYMBOL'], keep='first')

    total_patients = filtered_df['UPN'].unique().size

    pivot_df = filtered_df.pivot(index='SYMBOL', columns='UPN', values='AF')

    pivot_df = (pivot_df > 0).astype(int)
    # pivot_df['count'] = (pivot_df>0).sum(axis=1)
    #print(pivot_df.head(5))
    #print(pivot_df['count'].describe())
    #print(pivot_df.transpose().head(5))

    transpose_df = pivot_df.transpose()
    transpose_df = (transpose_df>0).astype(int)
    #print(transpose_df)

    reverse_transposed_df = transpose_df.transpose()

    cooccurence_matrix = reverse_transposed_df.dot(transpose_df)
    print(cooccurence_matrix)

    single_gene_count = (transpose_df.sum(axis=1) == 1).astype(int)
    single_gene_df = transpose_df[single_gene_count == 1].sum(axis=0)
    print(single_gene_df)

    # for gene in single_gene_df.index:
    #     cooccurence_matrix.loc[gene, gene] = single_gene_df[gene]

    print(cooccurence_matrix)
    #cooccurence_matrix.to_csv(output_dir, sep='\t', index=False, header=True)
    details_df = getDetails(cooccurence_matrix, total_patients)

    with open(output_dir, 'w') as f:
        f.write('# Co-occurence matrix \n')
        cooccurence_matrix.to_csv(f, sep='\t', index=False, header=True)
        f.write('\n#Details \n')
        details_df.to_csv(f, sep='\t', index=False)


def getDetails(matrix, total_patients):
    details = []
    genes = matrix.index

    for i in range(genes.size):
        for j in range(genes.size):
            if (i != j):
                totalA = matrix.iloc[i, i]
                totalB = matrix.iloc[j, j]
                totalAB = matrix.iloc[i, j]

                AnotB = totalA - totalAB
                BnotA = totalB - totalAB
                neither = total_patients - totalAB - AnotB - BnotA

                oddsRatio = 1
                if (AnotB * BnotA != 0):
                    oddsRatio = (neither * totalAB) / (AnotB * BnotA)
                
                oddsRatio = np.log2(oddsRatio)


                tendency = "Mutual exclusivity"
                if (oddsRatio > 0):
                    tendency = "Co-occurence"

                details.append({
                    'geneA':  genes[i],
                    'geneB': genes[j],
                    'Both': totalAB, 
                    'A Not B': AnotB,
                    'B Not A': BnotA,
                    'Neither': neither,
                    'Log2 Odds Ratio': oddsRatio,
                    'Tendency': tendency
                })

    details_df = pd.DataFrame(details)
    return details_df

def main():
    args = parse_arguments()
    target_dir = Path(args.path)
    output_dir = Path(args.outputPath)
    check_directories(target_dir, output_dir)
    make_matrix(target_dir, output_dir)

if __name__ == "__main__":
    main()