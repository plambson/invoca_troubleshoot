import pandas as pd

# explore duplicates, there are 35 duplicated entires
data = pd.read_json('revision140.json')
unique_count = data.groupby(['url', 'destination', 'utm_campaign', 'utm_source', 'utm_medium']).count()['forward']
unique_count = unique_count.reset_index().sort_values('forward', ascending=False)
unique_count.rename(columns={'forward': 'count'}, inplace=True)
unique_count.reset_index(inplace=True, drop=True)
multiple_entries = unique_count[unique_count['count'] > 1]
single_entries = unique_count[unique_count['count'] == 1]
all_dupes = pd.merge(data,
                     multiple_entries,
                     how='inner',
                     on=['url', 'destination', 'utm_campaign', 'utm_source', 'utm_medium'])

all_dupes.to_csv('all_dupes.csv')
dupes_unique = all_dupes.groupby(['url', 'destination', 'utm_campaign', 'utm_source', 'utm_medium']).nunique()[
    'forward']
dupes_unique = dupes_unique.reset_index().sort_values('forward', ascending=False)
