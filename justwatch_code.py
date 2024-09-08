#search("Fight Club", "GB", "en", 5, True)
#details("tm42409", "GB", "en", False)

from simplejustwatchapi.justwatch import search, details
import pandas as pd
# Perform the search



results = search("Fight Club", "GB", "en", 5, True)

# Function to convert offers to a DataFrame
def offers_to_dataframe(media_entries):
    rows = []
    for entry in media_entries:
        title = entry.title  # Access title attribute
        for offer in entry.offers:  # Access offers attribute
            row = {
                'Title': title,
                'Platform': offer.package.name,
                'url': offer.url,
                'Monetization Type': offer.monetization_type,  
                'presentation_type': offer.presentation_type,  
                #'Price String': getattr(offer, 'price_string', 'N/A'),  # Use getattr for optional attributes
                #'Price Currency': getattr(offer, 'price_currency', 'N/A'),  # Use getattr for optional attributes
                'URL': offer.url  # Access url attribute
            }
            rows.append(row)
    return pd.DataFrame(rows)


# Convert offers to DataFrame
df = offers_to_dataframe(results)

# Print DataFrame
print(df.to_string(index=False))