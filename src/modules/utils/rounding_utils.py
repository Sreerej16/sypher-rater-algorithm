# utils/rounding_utils.py
from decimal import Decimal, ROUND_DOWN, ROUND_UP
import pandas as pd

def custom_round(series: pd.Series) -> pd.Series:
    def round_logic(val):
        d = Decimal(str(val))
        str_val = format(d, '.10f').rstrip('0').rstrip('.')
        parts = str_val.split('.')
        
        if len(parts) == 1 or len(parts[1]) <= 3:
            return float(d.quantize(Decimal('0.001')))
        
        fourth_digit = int(parts[1][3])
        
        if fourth_digit < 5:
            return float((d * 1000).to_integral_value(rounding=ROUND_DOWN) / 1000)
        else:
            return float((d * 1000).to_integral_value(rounding=ROUND_UP) / 1000)

    return series.apply(round_logic)
