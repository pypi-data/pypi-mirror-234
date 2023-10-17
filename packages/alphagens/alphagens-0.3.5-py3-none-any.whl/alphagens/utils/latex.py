import pandas as pd

def df_to_latex(df: pd.DataFrame, file, caption=None, label=None):
    result = df.style.to_latex(
        hrules=True,
        position="htbp",
        position_float="centering",
        caption=caption, 
        label=label
    )
    with open(file, "w+") as f:
        f.write(result)
