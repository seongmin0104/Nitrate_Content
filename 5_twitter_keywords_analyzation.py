# Import package
import json
# String of path to file: tweets_data_path
tweets_data_path = 'C:/Users/Always9/PycharmProjects/Pycharm Projects/daily/tweet_sad_happy.txt'
# Initialize empty list to store tweets: tweets_data
tweets_data = []
# Open connection to file
tweets_file = open(tweets_data_path, "r")
# Read in tweets and store in list: tweets_data
for line in tweets_file:
    tweet = json.loads(line)
    tweets_data.append(tweet)
# Close connection to file
tweets_file.close()
# Import package
import pandas as pd
# Build DataFrame of tweet texts and languages
df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
import re
def word_in_text(word, tweet):
    word = word.lower()
    text = tweet.lower()
    match = re.search(word, text)
    if match:
        return True
    return False
# Initialize list to store tweet counts
[sad, happy] = [0, 0]

# Iterate through df, counting the number of tweets in which
# each candidate is mentioned
for index, row in df.iterrows():
    sad += word_in_text('sad', row['text'])
    happy += word_in_text('happy', row['text'])
# Import packages
import seaborn as sns
import matplotlib.pyplot as plt
# Set seaborn style
sns.set(color_codes=True)
# Create a list of labels:cd
cd = ['sad', 'happy']
# Plot histogram
ax = sns.barplot(cd, [sad, happy])
ax.set(ylabel="count")
plt.show()
