import pandas as pd
import numpy as np
from chord_matrix.utils import getDetails

def check_directories(target_dir, output_dir):
    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)

def make_matrix(target_dir, output_dir):
    df = pd.read_csv(target_dir, sep='\t', low_memory=False)
    df = df[df['status'] == 'RMG_53']
    filtered_df = df[["UPN", "AF", "SYMBOL"]]
    filtered_df = filtered_df.drop_duplicates(subset=['UPN', 'SYMBOL'], keep='first')
    total_patients = filtered_df['UPN'].unique().size

    pivot_df = filtered_df.pivot(index='SYMBOL', columns='UPN', values='AF')
    pivot_df = (pivot_df > 0).astype(int)
    transpose_df = pivot_df.transpose()
    transpose_df = (transpose_df > 0).astype(int)
    reverse_transposed_df = transpose_df.transpose()
    cooccurence_matrix = reverse_transposed_df.dot(transpose_df)

    single_gene_count = (transpose_df.sum(axis=1) == 1).astype(int)
    single_gene_df = transpose_df[single_gene_count == 1].sum(axis=0)

    details_df = getDetails(cooccurence_matrix, total_patients)

    with open(output_dir, 'w') as f:
        f.write('# Co-occurence matrix \n')
        cooccurence_matrix.to_csv(f, sep='\t', index=False, header=True)
        f.write('\n#Details \n')
        details_df.to_csv(f, sep='\t', index=False)

