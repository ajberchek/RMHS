import sqlite3
import bcrypt
conn = sqlite3.connect('RMHS.db')

user = "abe"
dat = "hi"

dataToHash = dat.encode('UTF-8')

print(dataToHash)

salt = bcrypt.gensalt()
hashedData = bcrypt.hashpw(dataToHash,salt)

print("Salt: " + str(salt))
print("Hashed PW: " + str(hashedData))


c = conn.cursor()

c.execute('INSERT INTO Credentials VALUES (?,?,?)',(user,hashedData,salt));
conn.commit()
conn.close()
