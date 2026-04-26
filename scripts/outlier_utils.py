import pandas as pd

def count_outliers(zscore_df, cols, threshold=3):
    """
    Count number of outliers in each column based on z-score threshold.

    Parameters:
        zscore_df (DataFrame): dataframe containing absolute z-scores
        cols (list): columns to inspect
        threshold (int/float): z-score threshold

    Returns:
        dict: {column_name: outlier_count}
    """
    
    outlier_counts = {}

    for col in cols:
        col_outliers = (zscore_df[col] > threshold).sum()
        outlier_counts[col] = col_outliers

    return outlier_counts


def print_outliers(zscore_df, cols, threshold=3):
    """
    Print outlier counts nicely.
    """
    outlier_counts = count_outliers(zscore_df, cols, threshold)

    for col, count in outlier_counts.items():
        print(f"{col}: {count} outliers")