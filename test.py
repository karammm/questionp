import requests
import time
from datetime import datetime, timedelta

from flask_migrate import Migrate, MigrateCommand
from flask_rest_jsonapi import ResourceList
from flask import Flask
from flask_rest_jsonapi import Api
from flask_rest_jsonapi import ResourceDetail
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/apikaram'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate=Migrate(app, db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

class TopStories(ResourceList):
    def get(self):
        # Calculate the timestamp for 15 minutes ago
        timestamp = int((datetime.utcnow() - timedelta(minutes=15)).timestamp())

        # Fetch the top stories from the Hacker News API
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?orderBy="$key"&startAt={timestamp}.json')
        story_ids = response.json()[:10]

        # Fetch the details for each story
        stories = []
        for story_id in story_ids:
            story = requests.get('https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
            stories.append({
                'title': story['title'],
                'url': story['url'],
                'score': story['score'],
                'time': datetime.fromtimestamp(story['time']),
                'user': story['by']
            })

        return {'data': stories}

class PastStories(ResourceList):
    def get(self):
        # Fetch the cached stories from the previous request to /top-stories
        cached_data = current_app.config.get('cached_data', {})
        stories = cached_data.get('top_stories', [])

        return {'data': stories}

class Comments(ResourceList):
    def get(self, story_id):
        # Fetch the comments for the given story from the Hacker News API
        story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
        comment_ids = story['kids'][:10] if story.get('kids') else []

        # Fetch the details for each comment
        comments = []
        for comment_id in comment_ids:
            comment = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json').json()
            comments.append({
                'text': comment['text'],
                'user': comment['by']
            })

        # Sort the comments by the number of child comments
        sorted_comments = sorted(comments, key=lambda c: c.get('kids', 0), reverse=True)

        return {'data': sorted_comments}
api = Api(app)

api.route(TopStories, 'top-stories', '/top-stories')
api.route(PastStories, 'past-stories', '/past-stories')
api.route(Comments, 'comments', '/comments')

if __name__ == '__main__':
    manager.run()