import _sqlite3

conn = _sqlite3.connect('shopBase.db')

c = conn.cursor()



c.execute("""
ALTER TABLE user
  ADD password VARCHAR(255);
""")

conn.commit()
conn.close()