### News Sentiment Analysis with AWS Comprehend and NewsAPI
This Python script performs sentiment analysis on news articles related to prominent tech figures (Mark Zuckerberg, Jeff Bezos, Elon Musk, Bill Gates) using the NewsAPI and AWS Comprehend. The sentiment analysis is visualized through summary tables and charts.

#### Prerequisites
- Python 3.x
- requests, pandas, boto3, matplotlib, and seaborn libraries. You can install them using:
`pip install requests pandas boto3 matplotlib seaborn`

#### Setup
- Get your API key from NewsAPI and replace "your_NewsAPI_key" with your actual API key.
- Configure your AWS credentials for the AWS Comprehend service.

#### Usage
- Run the script in your Python environment.
- The script will fetch news articles from NewsAPI based on predefined queries for each tech figure.
- Perform sentiment analysis on the content of each article using AWS Comprehend.
- Display a summary table of the sentiment distribution for each tech figure.
- Generate visualizations:
  - Total number of articles for each query.
  - Distribution of sentiments for each query in a stacked bar chart.
  - Average negative sentiment scores for each tech figure in a horizontal bar chart.

#### Output
- The script will output a DataFrame containing information about each article, sentiment analysis results, and summary tables and visualizations.
#### Notes
- Make sure to handle your API keys securely.
- Adjust the AWS region ("eu-west-1") based on your AWS setup.
- Fine-tune queries or add more queries based on your interests.
- Feel free to modify the script according to your needs and explore additional functionalities or customizations.
