import sqlite3

conn = sqlite3.connect("instance/dent_ai_care.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM user WHERE id IN (3, 16)")

print("Rows deleted:", cursor.rowcount)

conn.commit()
conn.close()