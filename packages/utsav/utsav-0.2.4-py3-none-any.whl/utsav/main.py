import pandas as pd
import matplotlib.pyplot as plt

def greet():
    print("My first python library, \nPlease bear with me while I construct an intuitive drag-and-drop interface for FASTQ. This tool will provide you with publishable results, all fine-tuned according to your specified parameters.")

def top_average(data, n=10):
    """
    Process a DataFrame or read an Excel file and return a dataframe with the top 'n' columns based on the highest averages.
    Also, plot a bar plot for the averages of the selected columns.

    Parameters:
    - data: DataFrame or filename of the Excel file.
    - n: The number of top columns to select based on average.

    Returns:
    - DataFrame with top 'n' columns based on average.
    """
    
    # Check if 'data' is a string (filename or filepath), then read the Excel file. 
    # Otherwise, use the DataFrame directly.
    if isinstance(data, str):
        try:
            df = pd.read_excel(data)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return
    else:
        df = data

    # Check if the dataframe contains only numeric data
    if not (df.dtypes == 'float64').all() and not (df.dtypes == 'int64').all():
        print("Data contains non-numeric values. Cannot calculate averages.")
        return

    # Compute the average of each column
    column_averages = df.mean()

    # Sort columns based on the average in descending order and select top 'n'
    top_n_averages = column_averages.nlargest(n)

    # Create a new dataframe containing only the top 'n' columns
    df_top_n = df[top_n_averages.index]

    # Plotting bar plot for the averages of top 'n' columns
    top_n_averages.plot(kind='bar', figsize=(10, 6), edgecolor='black', color='skyblue')
    plt.title(f'Top {n} Columns by Average')
    plt.ylabel('Average Value')
    plt.xlabel('Column Name')
    plt.tight_layout()
    plt.show()

    return df_top_n

