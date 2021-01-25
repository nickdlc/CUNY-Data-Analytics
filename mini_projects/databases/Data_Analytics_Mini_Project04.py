import csv
import sqlite3

def create_connection():
    '''
    Creates a YouTube database (if it doesn't exist), and connects to it.

    post: Returns a sqlite3 connection to the YouTube database.
    '''
    try:
        conn = sqlite3.connect('YouTube.db')
        print('Connection successful')
        return conn
    except:
        print('Error connecting to database')

def create_table(conn, stmt):
    '''
    pre: conn is a sqlite3 connection, stmt is a SQL statement
    post: creates a table in the database from conn
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(stmt)
        conn.commit()
        print('Table created')
    except:
        print('Unable to create table')

def populate_table(conn, stmt, entry):
    '''
    pre: conn is a sqlite3 connection, stmt is a SQL statement, entry is a list of values
    corresponding to the table denoted in stmt
    post: inserts the data in entry to the corresponding table denoted in stmt
    '''
    try:
        cursor = conn.cursor()
        cursor.executemany(stmt, entry)
        conn.commit()
        print('Insertion successful')
    except:
        print('Unable to insert into table')

def select_all(conn, stmt):
    '''
    pre: conn is a sqlite3 connection, stmt is a SQL statement
    post: prints each row in the table denoted in stmt
    '''
    cursor = conn.cursor()
    cursor.execute(stmt)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

conn = create_connection()

create_videos = '''CREATE TABLE videos(video_id INTEGER PRIMARY KEY NOT NULL,
                                       title VARCHAR(255) NOT NULL,
                                       length VARCHAR(10) NOT NULL,
                                       url VARCHAR(500) NOT NULL);'''

create_reviewers = '''CREATE TABLE reviewers(review_id INTEGER PRIMARY KEY NOT NULL,
                                             video_id INTEGER NOT NULL,
                                             username VARCHAR(50) NOT NULL,
                                             rating INTEGER,
                                             review VARCHAR(255),
                                             FOREIGN KEY (video_id)
                                                REFERENCES videos(video_id));'''

create_table(conn, create_videos)
create_table(conn, create_reviewers)

add_video = input('Would you like to add videos [Y/N]? ')

if add_video.upper() == 'Y':
    more = True
    while more:
        title = input('Enter the video title: ')
        length = input('Enter the video length [HH:MM:SS]: ')
        url = input('Enter the video url: ')

        videos_values = [(title, length, url)]
        insert_video = '''INSERT INTO videos(title, length, url) VALUES(?,?,?);'''
        populate_table(conn, insert_video, videos_values)

        if input('Would you like to add another video [Y/N]? ').upper() != 'Y':
            more = False

add_review = input('Would you like to add reviews [Y/N]? ')

if add_review.upper() == 'Y':
    more = True
    while more:
        select_all(conn, '''SELECT * FROM videos;''')

        video_id = int(input('Enter the video id for the video you with to review: '))
        username = input('Enter your username: ')
        review = input('Write your review here: ')
        add_rating = input('Would you like to add a rating [Y/N]? ')

        if add_rating.upper() == 'Y':
            rating = int(input('Rate the video from 0 to 5: '))
            reviewers_values = (video_id, username, rating, review)
        else:
            reviewers_values = (video_id, username, review)

        if len(reviewers_values) == 4:
            insert_review = '''INSERT INTO reviewers(video_id, username, rating, review) VALUES(?,?,?,?);'''
            populate_table(conn, insert_review, [reviewers_values])
        else:
            insert_review = '''INSERT INTO reviewers(video_id, username, review) VALUES(?,?,?);'''
            populate_table(conn, insert_review, [reviewers_values])

        if input('Would you like to review another video [Y/N]? ').upper() != 'Y':
            more = False

conn.close()
