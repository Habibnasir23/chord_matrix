import pandas as pd
import numpy as np

def getDetails(matrix, total_patients):
    details = []
    genes = matrix.index

    for i in range(genes.size):
        for j in range(genes.size):
            if i != j:
                totalA = matrix.iloc[i, i]
                totalB = matrix.iloc[j, j]
                totalAB = matrix.iloc[i, j]
                AnotB = totalA - totalAB
                BnotA = totalB - totalAB
                neither = total_patients - totalAB - AnotB - BnotA
                oddsRatio = 1
                if AnotB * BnotA != 0:
                    oddsRatio = (neither * totalAB) / (AnotB * BnotA)
                oddsRatio = np.log2(oddsRatio)
                tendency = "Mutual exclusivity"
                if oddsRatio > 0:
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
