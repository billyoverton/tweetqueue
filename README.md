tweetqueue
==========
A command line tool for time-delaying your tweets.

Installation
------------

```bash
$ pip install tweetqueue
```

Configuration
-------------
`tweetqueue` requires a JSON configuration file with the following entries

```json
{
    "API_KEY": "YourAPIKey",
    "API_SECRET": "YourAPISecret",
    "ACCESS_TOKEN": "yourAccessToken",
    "ACCESS_TOEKN_SECRET": "yourAccessTokenSecret",
    "DATABASE_LOCATION": "/a/file/path"
}
```

You can get the Twitter api values by creating an application at [Twitter Apps](https://apps.twitter.com/). To make creating the configuration file easier, you can use the config command.

```bash
$ tweetqueue config
```

By default, tweetqueue looks for a configuration file called `.tweetqueue` in your user's home directory. You can change the location of your configuration file by either setting the environment variable `TWEETQUEUE_CONFIG` or supplying the path on the command line.

```bash
$ tweetqueue --config /path/to/your/config COMMAND
```


Use
---
To add a message to your queue, use the queue command `tweetqueue queue "Hello, Twitter!"`. Messages added to your queue are not sent to Twitter until the dequeue command is called. `tweetqueue dequeue` will take the first message in the queue and post it to your Twitter timeline. Messages are dequeued in the order they are added, in a first in first out order.

If you want to bypass the queue, you can use `tweetqueue tweet "Hello, Twitter!"` This will immediately post `Hello, Twitter!` to your timeline.

Managing Your Queue
-------------------
You can show your current queue with `tweetqueue show`. This will print out a list of the tweets and an associated id. You can remove a tweet from your queue using this id with `tweetqueue delete ID`.