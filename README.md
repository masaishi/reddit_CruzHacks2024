# reddit_CruzHacks2024

## Overview

reddit_Sitegeist is a Python-based data collection tool that extracts textual data from Reddit. It uses the Reddit API through PRAW (Python Reddit API Wrapper) to gather posts and comments from specified subreddits. This tool is particularly useful for projects involving Natural Language Processing (NLP), sentiment analysis, or any research requiring large datasets of conversational text.

## Features

- **Data Collection from Reddit**: Extracts both posts and comments from any subreddit.
- **Customizable Data Retrieval**: Supports collecting 'hot' or 'new' posts and comments, with adjustable limits and time frames.
- **Expandable Comment Threads**: Recursively fetches replies to comments, ensuring a comprehensive dataset.
- **Timestamps and Metadata**: Includes creation timestamps and relevant metadata for posts and comments.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PRAW (Python Reddit API Wrapper)
- pandas (for data manipulation and exporting to CSV)
- tqdm (for progress bar visualization)

### Installation

1. Ensure Python 3.8 or higher is installed on your system.
2. Install the required Python libraries:

   ```bash
   pip install praw pandas tqdm
   ```

### Configuration

1. Register your application on Reddit to obtain a `client_id` and `client_secret`.
2. Set environment variables for your Reddit credentials:

   ```bash
   export REDDIT_CLIENT_ID='your_client_id'
   export REDDIT_CLIENT_SECRET='your_client_secret'
   ```

### Usage

1. Import and initialize the `RedditDataCollector` class:

   ```python
   from RedditDataCollector import RedditDataCollector

   collector = RedditDataCollector(client_id='your_client_id', client_secret='your_client_secret', user_agent='your_user_agent', subreddit_name='your_subreddit')
   ```

2. Use the methods to collect data:

   ```python
   # Collect hot text data
   collector.collect_hot_text_data(limit=10, after='start_timestamp', before='end_timestamp')
   # Collect new text data
   collector.collect_text_data(limit=10)
   ```

3. Export the collected data to CSV:

   ```python
   post_df = pd.DataFrame(collector.post_data)
   post_df.to_csv('/data/hot_posts.csv', index=False)
   comment_df = pd.DataFrame(collector.comment_data)
   comment_df.to_csv('/data/hot_comments.csv', index=False)
   ```
