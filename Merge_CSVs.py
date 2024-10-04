import os
import pandas as pd
import uuid

# Quick GPT Generated code:

# Function to create UID
def create_uid(suffix):
    return f"{uuid.uuid4()}_{suffix}"

# Set the folder paths and the list of queries
downloads_folder = os.path.expanduser('./Downloads')
queries = ['Hate Crime'] # 'Bias Crime', 'BI']  # Example query list
output_folder = os.path.join(downloads_folder, "Merged_Files")
final_merged_file = os.path.join(output_folder, '_'.join(queries) + '_merged.csv')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize a dictionary to store merged DataFrames for each query
query_dfs = {}

# Loop through each query in the query list
for query in queries:
    query_output_file = os.path.join(output_folder, f"{query}_Merged.csv")
    
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through folders in Downloads
    for folder in os.listdir(downloads_folder):
        folder_path = os.path.join(downloads_folder, folder)
        
        # Check if folder name starts with the query and is a directory
        if folder.startswith(query) and os.path.isdir(folder_path):
            # Look for CSV files in the folder
            for file in os.listdir(folder_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(folder_path, file)
                    
                    # Read CSV file into a DataFrame
                    df = pd.read_csv(file_path)
                    
                    # Append DataFrame to the list
                    dataframes.append(df)
    
    # Merge all DataFrames for the current query
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Human code xd
        merged_df["query"] = query
        merged_df = merged_df.rename(columns={
            'Headline': 'Title',        # 'Headline' -> 'Title'
            'Article': 'Main_Text'      # 'Article' -> 'Main_Text'
        })
        # End human code xd
        
        # Save the merged DataFrame to a CSV file
        merged_df.to_csv(query_output_file, index=False)
        print(f"Merged file saved for query '{query}' to {query_output_file}")
        
        # Store the merged DataFrame for later final merging
        query_dfs[query] = merged_df
    else:
        print(f"No CSV files found in folders starting with '{query}'")

# If there are merged DataFrames from the queries, perform the final merge
if query_dfs:
    # Concatenate all the merged DataFrames
    final_merged_df = pd.concat(query_dfs.values(), axis=0, ignore_index=True)
    
    # Add 'UID' column based on the presence of unique identifiers
    final_merged_df['UID'] = final_merged_df.apply(
        lambda row: create_uid('webS') if pd.notnull(row.get('link')) else 
                    (create_uid('TDM') if pd.notnull(row.get('GOID')) else create_uid('Lexis')),
        axis=1
    )
    
    # Save the final merged DataFrame
    final_merged_df.to_csv(final_merged_file, index=False)
    print(f"Final merged file saved to {final_merged_file}")
else:
    print("No DataFrames were found for final merging.")
