# ProyectoMachingLearningOperations
import pandas as pd
def url_set(url: str):
    return 'https://drive.google.com/uc?id=' + url.split('/')[-2]
def generate_id(show_id, platform):
    return platform[0] + show_id
dic_url = {"amazon_prime": url_set("https://drive.google.com/file/d/1LJIYUiPnFbU0mOKQMW54QZPPq1bAd5Zc/view?usp=share_link"),
            "disney_plus": url_set("https://drive.google.com/file/d/1d8BTVBj3NmCxUMknTkVcuVRWwVhXthiP/view?usp=share_link"),
           "hulu": url_set("https://drive.google.com/file/d/1Sy7HMCQgVlT31CAD2ewXrN82jMlsK21s/view?usp=share_link"),
           "netflix": url_set("https://drive.google.com/file/d/1yQ44qjfACWsR66lb-D_tDCmmDxPnIXvm/view?usp=share_link")}
df_names = pd.DataFrame()
for key, value in dic_url.items():
    # Get CSV file from Google Drive without downloading it
    df = pd.read_csv(value)
    df["id"] = df["show_id"].apply(lambda x: generate_id(x, key))
    df_names = pd.concat([df_names, df])
df_names.reset_index(drop=True, inplace=True)
list_url = [url_set("https://drive.google.com/file/d/1ImYbz29myZKGDZCYY4r5yzXWcdPqp-DL/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1rlpHWaxvo5kX5hyyOP7i5zpC5V9RfsaV/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1CBZA4xkDhfa-CX8dr92rhjKR3HhgctzE/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1CsaTyLVB-AZ78yJp9XeSw2qvTSNj9aYx/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1QztUrbE6CEC57AgbNcR9XJf9WIvwUF3P/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1y0TKNdKhSumjjaDSUGQTPIlMZuFqy1Zn/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/18WgvpsLVK_5uhCJm5HyZSytNreOIRiT1/view?usp=share_link"),
        url_set("https://drive.google.com/file/d/1dwqAfTL7BXbOvJn_A3bwQkL9_gbIFoTz/view?usp=share_link")]
#Merging multiple csv files into a single dataframe
df_ratings = pd.concat(map(pd.read_csv, list_url))
df_ratings.reset_index(drop=True, inplace=True)
