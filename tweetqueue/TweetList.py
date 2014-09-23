import sqlite3
import os

class TweetList(object):
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.connection = sqlite3.Connection(self.path)

        self.__init_db()

    def __init_db(self):

        c = self.connection.cursor()

        c.execute(
            '''CREATE TABLE IF NOT EXISTS tweets (
            id integer primary key autoincrement,
            message text not null,
            previous_tweet integer,
            next_tweet integer,
            FOREIGN KEY(previous_tweet) REFERENCES tweets(id),
            FOREIGN KEY(next_tweet) REFERENCES tweets(id)
            )'''
        )

        c.execute(
            '''CREATE TABLE IF NOT EXISTS tweetlist (
            label text primary key,
            tweet integer,
            FOREIGN KEY(tweet) REFERENCES tweets(id)
            )'''
        )

        # Check for the first_tweet and last_tweet references, set to
        # NULL if they do not  exist.

        try:
            c.execute("SELECT tweet from tweetlist where label='last_tweet'").next()
        except StopIteration:
            c.execute("INSERT INTO tweetlist VALUES ('last_tweet', NULL)")

        try:
            c.execute("SELECT tweet from tweetlist where label='first_tweet'").next()
        except StopIteration:
            c.execute("INSERT INTO tweetlist VALUES ('first_tweet', NULL)")

        self.connection.commit()
        c.close()


    def __len__(self):
        c = self.connection.cursor()
        count = conn.execute("SELECT COUNT(*) FROM tweets").next()[0]
        c.close()
        return count

    def append(self, tweet):
        """Add a tweet to the end of the list."""
        c = self.connection.cursor()

        last_tweet = c.execute("SELECT tweet from tweetlist where label='last_tweet'").next()[0]

        c.execute("INSERT INTO tweets(message,  previous_tweet, next_tweet) VALUES (?,?,NULL)", (tweet, last_tweet))
        tweet_id = c.lastrowid

        # Set the current tweet as the last tweet
        c.execute("UPDATE tweetlist SET tweet=? WHERE label='last_tweet'", (tweet_id,))

        # If there was no last_tweet, there was no first_tweet
        # so make this the first tweet
        if last_tweet is None:
            c.execute("UPDATE tweetlist SET tweet=? WHERE label='first_tweet'", (tweet_id,))
        else:
            # Update the last tweets reference to this one
            c.execute("UPDATE tweets SET next_tweet = ? WHERE id= ? ", (tweet_id, last_tweet))

        self.connection.commit()
        c.close()


    def pop(self):
        """Return first tweet in the list."""
        c = self.connection.cursor()

        first_tweet_id = c.execute("SELECT tweet from tweetlist where label='first_tweet'").next()[0]

        if first_tweet_id is None:
            # No tweets are in the list, so return None
            return None

        tweet = c.execute("SELECT id, message, previous_tweet, next_tweet from tweets WHERE id=?", (first_tweet_id,)).next()

        # Update the first tweet reference
        c.execute("UPDATE tweetlist SET tweet=? WHERE label='first_tweet'", (tweet[3],))

        # Update the "next tweet" if it exists
        if tweet[3] is not None:
            c.execute("UPDATE tweets SET previous_tweet=NULL WHERE id=?", (tweet[3],))
        else:
            #This was the last tweet so NULL the last tweet reference.
            c.execute("UPDATE tweetlist SET tweet=NULL WHERE label=?", ('last_tweet',))
        # Now remove the tweet from the list
        c.execute("DELETE FROM tweets WHERE id=?", (first_tweet_id,))

        self.connection.commit()
        c.close()

        return tweet[1]

    def peek(self):
        """Peeks at the first of the list without removing it."""
        c = self.connection.cursor()
        first_tweet_id = c.execute("SELECT tweet from tweetlist where label='first_tweet'").next()[0]
        if first_tweet_id is None:
            # No tweets are in the list, so return None
            return None

        tweet = c.execute("SELECT message from tweets WHERE id=?", (first_tweet_id,)).next()[0]

        c.close()
        return tweet

    def __iter__(self):
        c = self.connection.cursor()

        for tweet_id, tweet in c.execute("SELECT id, message from tweets"):
            yield (tweet_id, tweet)

        c.close()
    def delete(self, tweet_id):
        """Deletes a tweet from the list with the given id"""
        c = self.connection.cursor()

        try:
            tweet = c.execute("SELECT id, message, previous_tweet, next_tweet from tweets WHERE id=?", (tweet_id,)).next()
        except StopIteration:
            raise ValueError("No tweets were found with that ID")

        # Update linked list references
        c.execute("UPDATE tweets set next_tweet=? WHERE id=?", (tweet[3], tweet[2]))
        c.execute("UPDATE tweets set previous_tweet=? WHERE id=?", (tweet[2], tweet[3]))

        if tweet[3] is None:
            c.execute("UPDATE tweetlist SET tweet=? WHERE label='last_tweet'", (tweet[2],))

        if tweet[2] is None:
            c.execute("UPDATE tweetlist SET tweet=? WHERE label='first_tweet'", (tweet[3],))


        c.execute("DELETE from tweets WHERE id=?", (tweet_id,))
        self.connection.commit()
        c.close()

