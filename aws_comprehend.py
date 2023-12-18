import requests
import pandas as pd
import boto3

# Make API request
api_url = "https://newsapi.org/v2/everything"

# Construct the query parameter with logical operators
queries = ["Mark%AND%Zuckerberg", "Jeff%AND%Bezos", "Elon%AND%Musk", "Bill%AND%Gates"]

# Initialize AWS Comprehend client
comprehend = boto3.client(service_name="comprehend", region_name="eu-west-1")

# Initialize lists to store data
all_data = []

# Process each query
for query in queries:
    # Include the encoded query in API request
    params = {
        "q": query,
        "sortBy": "popularity",
        "language": "en",
        "searchIn": "title",
        "apiKey": "your_NewsAPI_key",
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    # Initialize lists for each query
    titles = []
    sources = []
    published_dates = []
    sentiments = []
    sentiment_scores = []

    # Process each article in the API response
    for article in data['articles']:
        # Extract relevant information
        title = article['title']
        source = article['source']['name']
        published_date = article['publishedAt']
        content = article['content']

        # Perform sentiment analysis with AWS Comprehend
        sentiment_response = comprehend.detect_sentiment(Text=content, LanguageCode='en')
        sentiment = sentiment_response['Sentiment']
        sentiment_score = sentiment_response['SentimentScore']

        # Append data to lists
        titles.append(title)
        sources.append(source)
        published_dates.append(published_date)
        sentiments.append(sentiment)
        sentiment_scores.append(sentiment_score)

    # Create a DataFrame for each query
    query_display = query.replace("%AND%", " ").replace("%", "") ## Clean up the query for display
    query_df = pd.DataFrame({
        'Title': titles,
        'Source': sources,
        'PublishedAt': published_dates,
        'Sentiment': sentiments,
        'SentimentScore': sentiment_scores,
        'Query': [query_display] * len(titles)  # Add a column for the related query
    })

    # Append the DataFrame to the list
    all_data.append(query_df)

# Concatenate all DataFrames into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Print the final DataFrame
pd.set_option('display.max_rows', None)
print(final_df)

# Group by "Query" and "Sentiment" columns and count the number of articles
summary_table = final_df.groupby(['Query', 'Sentiment']).size().unstack(fill_value=0)

# Reorder columns for better readability
summary_table = summary_table[['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED']]

# Add a column for total number of articles
summary_table['Total'] = summary_table.sum(axis=1)

# Print the summary table
print(summary_table)

import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plots 
sns.set(style="whitegrid")

# Create a bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Query', y='Total', data=summary_table.reset_index(), palette='viridis')
plt.title('Total Number of Articles for Each Query')
plt.ylabel('Number of Articles')
# Remove x-axis labels
ax.set(xlabel=None)

plt.show()


# Create a stacked bar chart
plt.figure(figsize=(12, 8))
sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED']
colors = ['green', 'red', 'yellow','orange']

# Iterate over sentiments and plot stacked bars
for i, sentiment in enumerate(sentiments):
    plt.bar(summary_table.index, summary_table[sentiment], bottom=summary_table[sentiments[:i]].sum(axis=1), label=sentiment, color=colors[i])

plt.title('Distribution of Sentiments for Each Query')
plt.ylabel('Number of Articles')
plt.legend(title='Sentiment')
plt.show()

# Create a horizontal bar chart
# Extract the negative sentiment score from the dictionary
final_df['Negative_Score'] = final_df['SentimentScore'].apply(lambda x: x['Negative'])

# Set the style for the plots
sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))

# Calculate the average negative sentiment scores for each tech titan
average_negative_scores = final_df.groupby('Query')['Negative_Score'].mean().sort_values(ascending=False)

# Map sentiment scores to colors
score_colors = sns.color_palette('viridis', len(average_negative_scores))

# Create the horizontal bar chart
plt.barh(average_negative_scores.index, average_negative_scores, color=score_colors)

plt.title('Average Negative Sentiment Scores for Each Tech Titan')
plt.xlabel('Average Negative Sentiment Score')
plt.show()