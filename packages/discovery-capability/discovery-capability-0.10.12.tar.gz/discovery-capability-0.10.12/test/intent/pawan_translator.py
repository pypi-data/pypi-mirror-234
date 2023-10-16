import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


class AutoPreprocessor:
    def __init__(self):
        self.datetime_columns = []  # Initialize datetime_columns as an empty list

    # Function to clean column names
    def clean_column_names(self, data):
        data.columns = data.columns.str.replace(' ', '_')  # Replace spaces with underscores
        data.columns = data.columns.str.strip()
        # Convert to lowercase
        data.columns = data.columns.str.lower()  # Remove leading and trailing whitespace, including newline characters
        data.columns = data.columns.str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
        return data

    def handle_missing_values(self, data, numerical_impute_method, categorical_impute_method):
        # Check for and drop columns exceeding the missing value threshold
        threshold = 0.7  # Set the threshold for missing values (70% or more)
        threshold_count = len(data) * threshold
        columns_to_drop = [col for col in data.columns if data[col].isna().sum() >= threshold_count]
        data = data.drop(columns=columns_to_drop)

        if not data.empty:
            numerical_data = data.select_dtypes(include=np.number)
            categorical_data = data.select_dtypes(include='object')

            if not numerical_data.empty:
                data = self._impute_numerical(data, numerical_impute_method)

            if not categorical_data.empty:
                data = self._impute_categorical(data, categorical_impute_method)

        return data

    def _impute_categorical(self, data, categorical_impute_method):
        categorical_columns = data.select_dtypes(include='object').columns

        for col in categorical_columns:
            if data[col].isna().sum() > 0:
                if col not in self.datetime_columns:  # Skip datetime columns
                    if categorical_impute_method == 'mode':
                        mode = data[col].mode().iloc[0]
                        data[col].fillna(mode, inplace=True)
                    elif categorical_impute_method == 'knn':
                        # Check if the column is numeric (can be converted to int)
                        if pd.api.types.is_numeric_dtype(data[col]):
                            imputer = KNNImputer(n_neighbors=5)
                            data[col] = imputer.fit_transform(data[col].values.reshape(-1, 1))
                            data[col] = data[col].astype(int)  # Convert back to integer after KNN imputation

        return data

    def _impute_numerical(self, data, numerical_impute_method):
        numerical_columns = data.select_dtypes(include=np.number).columns

        for col in numerical_columns:
            if data[col].isna().sum() > 0:
                if col not in self.datetime_columns:  # Skip datetime columns
                    if numerical_impute_method == 'auto':
                        # Choose imputation method automatically based on data characteristics
                        if len(data[col].unique()) > 10:
                            # Use K-NN for columns with many unique values
                            imputer = KNNImputer(n_neighbors=5)
                        else:
                            # Use Linear Regression for columns with fewer unique values
                            imputer = Pipeline([
                                ('scaler', StandardScaler()),
                                ('regressor', LinearRegression())
                            ])

                    elif numerical_impute_method == 'knn':
                        imputer = KNNImputer(n_neighbors=5)

                    elif numerical_impute_method in ['mean', 'median']:
                        imputer = SimpleImputer(strategy=numerical_impute_method)

                    data[col] = imputer.fit_transform(data[col].values.reshape(-1, 1))

        return data

    def preprocess(self, data, datetime_columns=None, numerical_impute_method='auto', categorical_impute_method='mode',
                   categorical_encoding_method='one-hot'):
        data = self.clean_column_names(data)  # Clean column names first

        # Set the datetime_columns attribute
        if datetime_columns:
            self.datetime_columns = datetime_columns

        data = self.handle_missing_values(data, numerical_impute_method, categorical_impute_method)

        if categorical_encoding_method == 'label':
            data = self.encode_categorical_label(data)
        elif categorical_encoding_method == 'one-hot':
            data = self.encode_categorical_one_hot(data)
        elif categorical_encoding_method == 'pd-dummies':
            data = self.encode_categorical_pd_dummies(data)

        data = self.scale_numerical(data)

        if datetime_columns:
            data = self.convert_datetime_columns(data, datetime_columns)

        return data

    def encode_categorical_label(self, data):
        # Encode categorical columns using LabelEncoder
        categorical_columns = data.select_dtypes(include='object').columns
        label_encoder = LabelEncoder()
        for col in categorical_columns:
            data[col] = label_encoder.fit_transform(data[col])
        return data

    def encode_categorical_one_hot(self, data):
        # Encode categorical columns using OneHotEncoder
        categorical_columns = data.select_dtypes(include='object').columns
        encoder = OneHotEncoder(drop='first', sparse=False)
        encoded_data = encoder.fit_transform(data[categorical_columns])
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names(categorical_columns))
        data = pd.concat([data.drop(columns=categorical_columns), encoded_df], axis=1)
        return data

    def encode_categorical_pd_dummies(self, data):
        # Encode categorical columns using pd.get_dummies
        categorical_columns = data.select_dtypes(include='object').columns
        data = pd.get_dummies(data, columns=categorical_columns, prefix=categorical_columns, drop_first=True)
        return data

    def scale_numerical(self, data):
        # Scale numerical columns using StandardScaler
        numerical_columns = data.select_dtypes(include=np.number).columns
        scaler = StandardScaler()
        data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
        return data

    def convert_datetime_columns(self, data, datetime_columns):
        # Convert datetime columns to datetime objects
        for col in datetime_columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')
        return data


# Example usage:
if __name__ == "__main__":
    auto_preprocessor = AutoPreprocessor()  # No need to set imputation methods during initialization
    raw_data = pd.read_csv("puntonet_englist_org.csv")

    # Define a list of columns that contain datetime strings
    datetime_columns = ['date_for_last_update', 'completion_date',
                        'creation_date']  # Replace with your actual column names

    # Choose different imputation methods, categorical encoding methods, and encoding methods based on your dataset
    numerical_impute_method = 'mean'
    categorical_impute_method = 'knn'
    categorical_encoding_method = 'label'  # Choose 'label', 'one-hot', or 'pd-dummies'

    preprocessed_data = auto_preprocessor.preprocess(raw_data, datetime_columns=datetime_columns,
                                                     numerical_impute_method=numerical_impute_method,
                                                     categorical_impute_method=categorical_impute_method,
                                                     categorical_encoding_method=categorical_encoding_method)

    print(preprocessed_data.head())
