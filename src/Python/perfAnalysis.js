//analysis the queries profiles of students collection in db school2 
//=> return the latency of the slowest query
db.profile.find({ns:'school2.students'}).sort({millis:-1}).pretty().limit(1).next().['millis']
