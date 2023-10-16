import sqlite3


def connect_db(db="test.db"):
    cx = sqlite3.connect(db)
    cu = cx.cursor()

    # create a table
    cu.execute("create table lang(name, first_appeared)")

    cu.execute("insert into lang values (?, ?)", ("C", 1972))

    # execute a query and iterate over the result
    for row in cu.execute("select * from lang"):
        print(row)

    cx.close()
