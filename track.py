import xml.etree.ElementTree as ET
import sqlite3
    
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()
    
    # Make some fresh tables using executescript()\n",
cur.executescript('''\n",
DROP TABLE IF EXISTS Artist;\n",
DROP TABLE IF EXISTS Album;\n",
DROP TABLE IF EXISTS Track;\n",
    \n",
    CREATE TABLE Artist (\n",
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n",
        name    TEXT UNIQUE\n",
   );\n",
    \n",
    CREATE TABLE Genre (\n",
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n",
        name    TEXT UNIQUE\n",
    );\n",
    \n",
    CREATE TABLE Album (\n",
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n",
        artist_id  INTEGER,\n",
        title   TEXT UNIQUE\n",
    );\n",
    \n",
    CREATE TABLE Track (\n",
        id  INTEGER NOT NULL PRIMARY KEY \n",
            AUTOINCREMENT UNIQUE,\n",
        title TEXT  UNIQUE,\n",
        album_id  INTEGER,\n",
        genre_id  INTEGER,\n",
        len INTEGER, rating INTEGER, count INTEGER\n",
    );''')
    
    
fname =' Library.xml'
if ( len(fname) < 1 ) : fname = 'Library.xml'
    
    # <key>Track ID</key><integer>369</integer>\n",
    # <key>Name</key><string>Another One Bites The Dust</string>\n",
    # <key>Artist</key><string>Queen</string>\n",
def lookup(d, key):
        found = False
        for child in d:
            if found : return child.text
            if child.tag == 'key' and child.text == key :
                found = True
        return None
    
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue
    
name = lookup(entry, 'Name')
artist = lookup(entry, 'Artist')
album = lookup(entry, 'Album')
genre=lookup(entry,'Genre')
count = lookup(entry, 'Play Count')
rating = lookup(entry, 'Rating')
length = lookup(entry, 'Total Time')
    
if name is None or artist is None or album is None or genre is None: 
   continue
    
print(name, artist, album,genre, count, rating, length)
    
cur.execute('''INSERT OR IGNORE INTO Artist (name) 
    VALUES ( ? )''', ( artist,  ))
cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
artist_id = cur.fetchone()[0]
        
cur.execute('''INSERT OR IGNORE INTO Genre (name) \n",
        VALUES ( ? )''', ( genre, ) )
cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
genre_id = cur.fetchone()[0]
        
cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) \n",
           VALUES ( ?, ? )''', ( album, artist_id ) )
cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
album_id = cur.fetchone()[0]
    
cur.execute('''INSERT OR REPLACE INTO Track\n",
            (title, album_id,genre_id, len, rating, count) \n",
            VALUES ( ?, ?,?, ?, ?, ? )''', 
            ( name, album_id,genre_id, length, rating, count ) )\
    
conn.commit()
sqlstr='SELECT Track.title, Artist.name, Album.title,Genre.name FROM Track JOIN Genre JOIN Album JOIN Artist ON Track.genre_id=Genre.ID and Track.album_id=Album.id AND Album.artist_id=Artist.id ORDER BY Artist.name LIMIT 3'
    
for row in cur.execute(sqlstr):
        print(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
cur.close()