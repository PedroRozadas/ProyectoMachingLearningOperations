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
# list_url = ["https://drive.google.com/uc?id=1ImYbz29myZKGDZCYY4r5yzXWcdPqp-DL",
#             "https://drive.google.com/uc?id=1rlpHWaxvo5kX5hyyOP7i5zpC5V9RfsaV",
#             "https://drive.google.com/uc?id=1CBZA4xkDhfa-CX8dr92rhjKR3HhgctzE",
#             "https://drive.google.com/uc?id=1CsaTyLVB-AZ78yJp9XeSw2qvTSNj9aYx",
#             "https://drive.google.com/uc?id=1QztUrbE6CEC57AgbNcR9XJf9WIvwUF3P",
#             "https://drive.google.com/uc?id=1y0TKNdKhSumjjaDSUGQTPIlMZuFqy1Zn",
#             "https://drive.google.com/uc?id=18WgvpsLVK_5uhCJm5HyZSytNreOIRiT1",
#             "https://drive.google.com/uc?id=1dwqAfTL7BXbOvJn_A3bwQkL9_gbIFoTz"]
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

df_names["rating"] = df_names["rating"].fillna("G")

df_names["date_added"] = df_names["date_added"].str.strip()
df_names["date_added"] = pd.to_datetime(df_names["date_added"], format="%B %d, %Y")

df_ratings["timestamp"] = pd.to_datetime(df_ratings["timestamp"], unit="s")

cols = ["type", "title", "director", "cast", "country", "listed_in", "description", "rating"]
df_names[cols] = df_names[cols].apply(lambda x: x.str.lower())

# split duration into two separate columns
df_duration = df_names["duration"].str.split(" ", n=1, expand=True)

# assign the resulting columns to duration_int and duration_type respectively
df_names["duration_int"] = df_duration[0].apply(lambda x: x if pd.notnull(x) else None)
df_names["duration_type"] = df_duration[1].apply(lambda x: x if pd.notnull(x) else None)

df_names["duration_int"] = df_names["duration_int"].astype(pd.UInt16Dtype())

df_names.to_csv("df_names.csv")

four = len(df_ratings) // 4
df1 = df_ratings.iloc[:four]
df2 = df_ratings.iloc[four:four + four]
df3 = df_ratings.iloc[four + four:four + four + four]
df4 = df_ratings.iloc[four + four + four:]
df1.to_csv("df1.csv")
df2.to_csv("df2.csv")
df3.to_csv("df3.csv")
df4.to_csv("df4.csv")