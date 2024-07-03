import argparse
from pathlib import Path
from chord_matrix.matrix import make_matrix, check_directories

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process the data files for PCA analysis.", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--path", required=True, help="Path to the main data file in TSV format")
    parser.add_argument("--outputPath", required=True, help="Path to download the output matrix file.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    target_dir = Path(args.path)
    output_dir = Path(args.outputPath)
    check_directories(target_dir, output_dir)
    make_matrix(target_dir, output_dir)

if __name__ == "__main__":
    main()
