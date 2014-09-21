import click
import tweepy
import json
import sqlite3
import os.path
from .TweetList import TweetList

def valid_tweet(message):
    return len(message) <= 140

@click.group()
@click.option('--dry-run', is_flag=True, default=False)
@click.option(
    '--config',
    envvar="TWEETQUEUE_CONFIG",
    type=click.File('rb')
)
@click.pass_context
def tweetqueue(ctx, dry_run, config):
    ctx.obj['DRYRUN'] = dry_run

    # If the config file wasn't provided, attempt to load the default one.
    if config is None:
        user_home = os.path.expanduser("~")
        default_config = os.path.join(user_home, ".tweetqueue")

        if not os.path.isfile(default_config):
            click.echo("Default configuration was not found and none was provided.")
            click.echo("Run 'tweetqueue config' to create one.")
            ctx.exit(1)

        config = open(default_config, 'rb')

    try:
        ctx.obj['config'] = json.load(config)
    except Exception as e:
        click.echo("Unable to read configuration file.")
        click.echo("Are you sure it is valid JSON")
        click.echo("JSON Error: " + e.message)
        ctx.exit(1)

    # Verify that the config file has all required options
    required_config = [
        'API_KEY',
        'API_SECRET',
        'ACCESS_TOKEN',
        'ACCESS_TOKEN_SECRET',
        'DATABASE_LOCATION'

    ]
    if not all(key in ctx.obj['config'] for key in required_config):
        click.echo("Missing required value in config file.")
        ctx.exit(1)

    # Make a tweepy api object for the context
    auth = tweepy.OAuthHandler(
        ctx.obj['config']['API_KEY'],
        ctx.obj['config']['API_SECRET']
    )
    auth.set_access_token(
        ctx.obj['config']['ACCESS_TOKEN'],
        ctx.obj['config']['ACCESS_TOKEN_SECRET']
    )
    ctx.obj['TWEEPY_API'] = tweepy.API(auth)


    ctx.obj['TWEETLIST'] = TweetList(ctx.obj['config']['DATABASE_LOCATION'])

@tweetqueue.command()
@click.argument('message')
@click.pass_context
def tweet(ctx, message):
    if not valid_tweet(message):
        click.echo("Message is too long for twitter.")
        click.echo("Message:" + message)
        ctx.exit(2)

    if not ctx.obj['DRYRUN']:
        ctx.obj['TWEEPY_API'].update_status(message)
    else:
        click.echo("Tweet not sent due to dry-run mode.")

@tweetqueue.command()
@click.argument('message')
@click.pass_context
def queue(ctx, message):
    if not valid_tweet(message):
        click.echo("Message is too long for twitter.")
        click.echo("Message: " + message)
        ctx.exit(2)

    if ctx.obj['DRYRUN']:
        click.echo("Message not queue due to dry-run mode.")
        ctx.exit(0)

    ctx.obj['TWEETLIST'].append(message)

@tweetqueue.command()
@click.pass_context
def dequeue(ctx):

    tweet =ctx.obj['TWEETLIST'].peek()

    if tweet is None:
        click.echo("Nothing to dequeue.")
        ctx.exit(1)

    if ctx.obj['DRYRUN']:
        click.echo(tweet)
    else:
        tweet = ctx.obj['TWEETLIST'].pop()
        ctx.obj['TWEEPY_API'].update_status(tweet)


if __name__ == '__main__':
    tweetqueue(obj={})
