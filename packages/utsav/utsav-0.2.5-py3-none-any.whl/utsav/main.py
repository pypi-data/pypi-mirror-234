import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, classification_report, roc_auc_score, accuracy_score

def greet():
    print("My first python library, \nPlease bear with me while I construct an intuitive interface for FASTQ. This tool will provide you with publishable results, all fine-tuned according to your specified parameters.")

def top_average(data, n=10):
    if isinstance(data, str):
        try:
            df = pd.read_excel(data)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return
    else:
        df = data

    if not (df.dtypes == 'float64').all() and not (df.dtypes == 'int64').all():
        print("Data contains non-numeric values. Cannot calculate averages.")
        return

    column_averages = df.mean()
    top_n_averages = column_averages.nlargest(n)
    df_top_n = df[top_n_averages.index]

    top_n_averages.plot(kind='bar', figsize=(10, 6), edgecolor='black', color='skyblue')
    plt.title(f'Top {n} Columns by Average')
    plt.ylabel('Average Value')
    plt.xlabel('Column Name')
    plt.tight_layout()
    plt.show()

    return df_top_n

def ml(input_df, algorithm='rf', train_method='split', test_size=None, folds=None, seed=123, file_path=None):
    if input_df is None:
        if file_path is None:
            raise ValueError("Either a file_path or a DataFrame (input_df) must be provided.")
        else:
            ext = file_path.split('.')[-1]
            if ext == "csv":
                input_df = pd.read_csv(file_path)
            elif ext == "xlsx":
                input_df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
    
    y = input_df.iloc[:, 0]
    X = input_df.iloc[:, 1:]

    if algorithm == "rf":
        if y.dtype == 'O':
            model = RandomForestClassifier(random_state=seed)
        else:
            model = RandomForestRegressor(random_state=seed)
    elif algorithm == "svm":
        if y.dtype == 'O':
            model = SVC(kernel='rbf', probability=True, random_state=seed)
        else:
            model = SVR(kernel='rbf')
    else:
        raise ValueError("Unsupported algorithm choice")
    
    results = {}
    
    if train_method == "cv" and folds is None:
        raise ValueError("For K-Fold Cross-Validation, 'folds' must be specified.")
    
    if train_method == "split":
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
    
    elif train_method == "cv":
        cv = KFold(n_splits=folds, shuffle=True, random_state=seed)
        metrics_results = {
            "Accuracy": [],
            "Precision": [],
            "Recall": [],
            "Sensitivity": [],
            "F1 Score": [],
            "AUC-ROC": []
        }
        
        for train_idx, test_idx in cv.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            metrics_results["Accuracy"].append(accuracy_score(y_test, preds))
            report = classification_report(y_test, preds, output_dict=True, zero_division=0)
            metrics_results["Precision"].append(report["macro avg"]["precision"])
            metrics_results["Recall"].append(report["macro avg"]["recall"])
            metrics_results["Sensitivity"].append(report["macro avg"]["recall"])
            metrics_results["F1 Score"].append(report["macro avg"]["f1-score"])
            
            if len(y.unique()) == 2:  # Binary classification
                preds_proba = model.predict_proba(X_test)[:, 1]
                metrics_results["AUC-ROC"].append(roc_auc_score(y_test, preds_proba))
            else:
                metrics_results["AUC-ROC"].append("Only available for binary tasks")
        
        for metric, values in metrics_results.items():
            if isinstance(values[0], str): 
                results[metric + " (CV)"] = values[0]
            else:
                results[metric + " (CV)"] = sum(values) / len(values)
    
    if train_method == "split":
        if y.dtype == 'O':
            preds_proba = model.predict_proba(X_test)
            report = classification_report(y_test, preds, output_dict=True)
            results = {
                "Accuracy": accuracy_score(y_test, preds),
                "Precision": report["macro avg"]["precision"],
                "Recall": report["macro avg"]["recall"],
                "Sensitivity": report["macro avg"]["recall"],
                "F1 Score": report["macro avg"]["f1-score"],
                "AUC-ROC": roc_auc_score(y_test, preds_proba[:, 1]) if len(y.unique()) == 2 else "Only available for binary tasks",
                "Confusion Matrix": confusion_matrix(y_test, preds).tolist()
            }
        else:
            results = {
                "Mean Absolute Error": mean_absolute_error(y_test, preds),
                "Mean Squared Error": mean_squared_error(y_test, preds),
                "RMSE": mean_squared_error(y_test, preds, squared=False),
                "R2": r2_score(y_test, preds)
            }
    
    return pd.DataFrame([results])
