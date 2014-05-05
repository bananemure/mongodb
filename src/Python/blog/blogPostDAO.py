__author__ = 'smbatchou'


import sys
import re
import datetime



# The Blog Post Data Access Object handles interactions with the Posts collection
class BlogPostDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    # inserts the blog entry and returns a permalink for the entry
    def insert_entry(self, title, post, tags_array, author):
        print "inserting blog entry", title, post

        # fix up the permalink to not include whitespace

        exp = re.compile('\W') # match anything not alphanumeric
        whitespace = re.compile('\s')
        temp_title = whitespace.sub("_",title)
        permalink = exp.sub('', temp_title)

        # Build a new post
        post = {"title": title,
                "author": author,
                "body": post,
                "permalink":permalink,
                "tags": tags_array,
                "comments": [],
                "date": datetime.datetime.utcnow()}

        # now insert the post
        try:
            #  insert the post
            self.posts.save(post)

            print "Inserting the post"
        except:
            print "Error inserting post"
            print "Unexpected error:", sys.exc_info()[0]

        return permalink

    # returns an array of num_posts posts, reverse ordered
    def get_posts(self, num_posts):

        cursor = []         # Placeholder so blog compiles before you make your changes

        #  here to get the posts
        try:
            cursor = self.posts.find().limit(10).sort('_id',-1)
        except:
            print "Error retrieving reverse ordered post"
            print "Unexpected error:", sys.exc_info()[0]

        l = []

        for post in cursor:
            post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p") # fix up date
            if 'tags' not in post:
                post['tags'] = [] # fill it in if its not there already
            if 'comments' not in post:
                post['comments'] = []

            l.append({'title':post['title'], 'body':post['body'], 'post_date':post['date'],
                      'permalink':post['permalink'],
                      'tags':post['tags'],
                      'author':post['author'],
                      'comments':post['comments']})

        return l


    # find a post corresponding to a particular permalink
    def get_post_by_permalink(self, permalink):

        post = None
        # retrieve the specified post
        try:
            cursor= self.posts.find({"permalink": permalink})
        except:
            print "Error retrieving post by permalink"
            print "Unexpected error:", sys.exc_info()[0]

        if cursor.alive:
            post= cursor.next()
        else:
            post = None

        if post is not None:
            # fix up date
            post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

        return post

    # add a comment to a particular blog post
    def add_comment(self, permalink, name, email, body):

        comment = {'author': name, 'body': body}

        if (email != ""):
            comment['email'] = email

        try:
            #add the comment to the designated post

            last_error = self.posts.update({"permalink": permalink},{"$push": {"comments": comment}},safe=True)
            #last_error = self.db.command("getLastError",1)

            return last_error['n']         # return the number of documents updated

        except:
            print "Could not update the collection, error"
            print "Unexpected error:", sys.exc_info()[0]
            return 0






