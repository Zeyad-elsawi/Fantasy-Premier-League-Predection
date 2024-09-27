import csv
import sys
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

TEST_SIZE = 0.5

def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python Fantazy.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels, identity = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    # Convert predictions to discrete labels by rounding
    predicted_labels = predictions.round().astype(int)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predicted_labels)
    cm = confusion_matrix(y_test, predicted_labels)
    sensitivity = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if (cm[1, 1] + cm[1, 0]) > 0 else 0
    specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1]) if (cm[0, 0] + cm[0, 1]) > 0 else 0

    # Print results
    print(f"Correct: {(y_test == predicted_labels).sum()}")
    print(f"Incorrect: {(y_test != predicted_labels).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

def load_data(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Create a dictionary to store player identity numbers
    player_ids = {}
    next_id = 0

    # Initialize a list for the identity numbers to be added to the DataFrame
    identity_numbers = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Create a unique key for each player using name, position, and team
        player_key = (row['name'], row['position'], row['team'])

        # If the player is already in the dictionary, use their existing ID
        if player_key in player_ids:
            identity_no = player_ids[player_key]
        else:
            # If the player is not in the dictionary, assign a new unique ID
            identity_no = next_id
            player_ids[player_key] = identity_no
            next_id += 1

        # Append the identity number to the list
        identity_numbers.append(identity_no)

    # Add the identity numbers as a new column in the DataFrame
    df['identity_no'] = identity_numbers

    # Define columns for the player information (identity)
    columns_to_include = ['name', 'position', 'team']
    identity_df = df[columns_to_include]

    # Define evidence columns by dropping unnecessary columns
    evidence_df = df.drop(columns=['name', 'position', 'team', 'total_points'])

    # Convert data to lists
    evidence = evidence_df.values.tolist()
    labels = df['identity_no'].tolist()
    identity = identity_df.values.tolist()

    return evidence, labels, identity

def train_model(evidence, labels):
    # Train a linear regression model
    model = LinearRegression()
    model.fit(evidence, labels)
    return model

if __name__ == "__main__":
    main()
