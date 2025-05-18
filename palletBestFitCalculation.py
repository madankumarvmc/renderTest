# palletBestFitCalculation.py

import pandas as pd
import io
import math

def pallet_capacity(file_stream):
    """Reads Pallet Size and Case Size sheets from an Excel file stream."""
    dfs = pd.read_excel(file_stream, sheet_name=None)

    print("DEBUG Sheet names found:", list(dfs.keys()))  # Add this

    pallet_df = dfs.get("Pallet Size")
    case_df = dfs.get("Case Size")

    if pallet_df is None or case_df is None:
        raise ValueError("Required sheet(s) missing: 'Pallet Size' or 'Case Size'")

    pallet_sku_capacity_df = capacity_calculation(pallet_df, case_df)

    return pallet_sku_capacity_df


def capacity_calculation(pallet_df, case_df):
    """
    Calculates how many cases of each SKU can fit on the given pallet (per layer),
    trying both orientations (lengthwise and breadthwise).
    """
    if pallet_df.empty:
        raise ValueError("Pallet DataFrame is empty")

    pallet_length = float(pallet_df.iloc[0]["Pallet Length (cm)"])
    pallet_breadth = float(pallet_df.iloc[0]["Pallet Breadth (cm)"])

    results = []

    for _, row in case_df.iterrows():
        sku = row["SKU Code"]

        max_stacking_layers = float(row["Stacking Layer (Max)"])
        
        case_length = float(row["Case Lenght (cm)"])
        case_breadth = float(row["Case Beradth (cm)"])

        if pd.isna(case_length) or pd.isna(case_breadth):
            raise ValueError(f"Missing length or breadth for SKU: {sku}")

        # Orientation-1
        fit_len_1 = math.floor(pallet_length / case_length)
        fit_brd_1 = math.floor(pallet_breadth / case_breadth)
        capacity_1 = fit_len_1 * fit_brd_1

        # Orientation-2
        fit_len_2 = math.floor(pallet_length / case_breadth)
        fit_brd_2 = math.floor(pallet_breadth / case_length)
        capacity_2 = fit_len_2 * fit_brd_2

        max_capacity = max(capacity_1, capacity_2)

        pallet_capacity = max_capacity * max_stacking_layers

        results.append({
            "SKU Code": sku,
            "Pallet Capacity": pallet_capacity
        })

    return pd.DataFrame(results)