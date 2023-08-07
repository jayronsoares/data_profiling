import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

def check_missing_values_lazy(series):
    """
    Check for missing values in the pandas Series using lazy evaluation.
    """
    return series.isnull().sum()

def check_duplicates_lazy(series):
    """
    Check for duplicates in the pandas Series using lazy evaluation.
    """
    return series.duplicated().sum()

def check_cardinality_lazy(series):
    """
    Check if a column has high or low cardinality using lazy evaluation.
    """
    cardinality = series.nunique()
    high_cardinality = cardinality > len(series) / 2
    low_cardinality = cardinality < 0.01 * len(series)
    return high_cardinality, low_cardinality

def check_consistency_lazy(group_data):
    """
    Check for consistency in the dataset using lazy evaluation.
    """
    inconsistent_rows = [len(set(row)) > 1 for row in group_data]
    return sum(inconsistent_rows)

def check_accuracy_validity_lazy(series):
    """
    Check for accuracy and validity in the pandas Series using lazy evaluation.
    """
    notna_mask = pd.notna(series)
    min_value, max_value = series[notna_mask].min(), series[notna_mask].max()
    valid_values = series[notna_mask].unique()

    accuracy_count = np.logical_and(series >= min_value, series <= max_value).sum()
    accuracy_percent = accuracy_count / notna_mask.sum() * 100

    validity_count = series.isin(valid_values).sum()
    validity_percent = validity_count / notna_mask.sum() * 100

    return accuracy_count, accuracy_percent, validity_count, validity_percent

def data_quality_checks_lazy(df):
    """
    Perform data quality checks using lazy evaluation on the DataFrame.
    """
    results = {}
    for column in df.columns:
        series = df[column]

        results[column] = {
            "Missing Values": check_missing_values_lazy(series),
            "Duplicates": check_duplicates_lazy(series),
            "High Cardinality": check_cardinality_lazy(series)[0],
            "Low Cardinality": check_cardinality_lazy(series)[1],
            "Consistency Issues": check_consistency_lazy(df.groupby(list(df.drop(column, axis=1).columns[:2]))[column].apply(list)),
        }

        # Get accuracy and validity results
        accuracy_count, accuracy_percent, validity_count, validity_percent = check_accuracy_validity_lazy(series)
        results[column]["Accuracy Count"] = accuracy_count
        results[column]["Accuracy Percentage"] = accuracy_percent
        results[column]["Validity Count"] = validity_count
        results[column]["Validity Percentage"] = validity_percent

    return results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        try:
            df = pd.read_csv(file, nrows=5)  # Load only the first 5 rows for column information
            columns = df.columns.tolist()
            return render_template('upload.html', columns=columns)  # Pass columns variable to the template
        except Exception as e:
            return f"Error: {e}"
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    df = pd.read_csv(file)

    # Perform data quality checks using lazy evaluation
    results = data_quality_checks_lazy(df)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
