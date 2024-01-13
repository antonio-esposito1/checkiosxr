import shelve

db = shelve.open('devicedb')

for key in sorted(db):
    print(key, '\t=', db[key])
    
mivpe015 = db['v-mivpe015']
mivpe015.connectnetconf()
db.close()