// indexes for blog posts

db.posts.ensureIndex({'date':-1}); 
db.posts.ensureIndex({'tags':1,'date'-1});
db.posts.ensureIndex({'permalink':1});


//show the indexes status for posts collection
db.posts.getIndexes()

