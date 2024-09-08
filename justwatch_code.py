from simplejustwatchapi.justwatch import search, details
import pandas as pd

# Function to convert offers to a DataFrame
def offers_to_dataframe(media_entries):
    rows = []
    for entry in media_entries:
        title = entry.title  # Access title attribute
        for offer in entry.offers:  # Access offers attribute
            row = {
                'Title': title,
                'Platform': offer.package.name,
                'URL': offer.url,
                'Monetization Type': offer.monetization_type,  
                'Presentation Type': offer.presentation_type,  
            }
            rows.append(row)
    return pd.DataFrame(rows)

# Read the Excel file with titles
df_titles = pd.read_excel('test.xlsx')  # Replace 'titles.xlsx' with your file name

# Initialize an empty DataFrame to store all results
all_results = pd.DataFrame()

# Iterate over each title in the "Titles" column and perform the search
for title in df_titles['Title']:  # Replace 'Titles' with the exact column name in your Excel file
    results = search(title, "GB", "en", 5, True)
    df = offers_to_dataframe(results)
    all_results = pd.concat([all_results, df], ignore_index=True)

# Save the combined results to a new Excel file
all_results.to_excel('offers_results.xlsx', index=False)  # Replace 'offers_results.xlsx' with your desired output file name

# Optional: print the results to check
print(all_results.to_string(index=False))
