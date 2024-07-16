import pandas as pd

url = 'https://archive.ics.uci.edu/static/public/222/data.csv'
df = pd.read_csv(url)

seasons = {
    'fall': ['sep', 'oct', 'nov'],
    'winter': ['dec', 'jan', 'feb'],
    'spring': ['mar', 'apr', 'may'],
    'summer': ['jun', 'jul', 'aug']
}

def filter_by_season(df, months):
    return df[df['month'].isin(months)]

fall_df = filter_by_season(df, seasons['fall'])
winter_df = filter_by_season(df, seasons['winter'])
spring_df = filter_by_season(df, seasons['spring'])
summer_df = filter_by_season(df, seasons['summer'])

pd.concat([winter_df, spring_df]).to_csv('data/test/dataset_1.csv', index=False)
summer_df.to_csv('data/new/dataset_2.csv', index=False)
fall_df.to_csv('data/new/dataset_3.csv', index=False)
