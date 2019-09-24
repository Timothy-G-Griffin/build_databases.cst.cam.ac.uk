import urllib3
import os

http = urllib3.PoolManager()

url_base = 'https://datasets.imdbws.com/'
target_dir = 'IMDb_raw/'


def fetchit (str):
    print ('Fetching ' + str + ' ...')
    r = http.request('GET', url_base + str)
    with open(target_dir + str, 'wb') as f:
        f.write(r.data)

fetchit('name.basics.tsv.gz')
#fetchit('title.akas.tsv.gz')
fetchit('title.basics.tsv.gz')
#fetchit('title.crew.tsv.gz') 
#fetchit('title.episode.tsv.gz')
fetchit('title.principals.tsv.gz')
fetchit('title.ratings.tsv.gz')

os.system('gunzip ' + target_dir + '*.gz')         
