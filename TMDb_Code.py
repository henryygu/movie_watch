from dotenv import load_dotenv
from themoviedb import TMDb
import os
import pandas as pd

# Import environment variables from .env file
load_dotenv()
TMDB_Key = os.getenv("TMDB_Key")

tmdb = TMDb(key=TMDB_Key, language="en-GB", region="GB")

# Search for the movie "Fight Club"
movies = tmdb.search().movies("fight club")
if movies:
    movie_id = movies[0].id  # Get first result
    movie = tmdb.movie(movie_id).details(append_to_response="credits,external_ids,images,videos")
    # Get where to watch information
    providers = tmdb.movie(movie_id).watch_providers()
    # Extract information for the desired region (GB)
    if 'GB' in providers:
        gb_providers = providers['GB']
        print("Where to watch 'Fight Club' in GB:")
else:
    print("No movies found for the search term.")





def extract_provider_data(providers_list):
    return [
        {
            "Provider Name": provider.provider_name,
            "Display Priority": provider.display_priority,
           # "Logo Path": provider.logo_path,
            "Provider ID": provider.provider_id
        }
        for provider in providers_list
    ]

# Convert the provider lists to dataframes
if gb_providers.flatrate:
    flatrate_df = pd.DataFrame(extract_provider_data(gb_providers.flatrate))
    print("Flatrate Providers:")
    print(flatrate_df.to_string(index=False))
    print("\n")

if gb_providers.buy:
    buy_df = pd.DataFrame(extract_provider_data(gb_providers.buy))
    print("Buy Providers:")
    print(buy_df.to_string(index=False))
    print("\n")

if gb_providers.rent:
    rent_df = pd.DataFrame(extract_provider_data(gb_providers.rent))
    print("Rent Providers:")
    print(rent_df.to_string(index=False))
    print("\n")