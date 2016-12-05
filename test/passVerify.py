import sqlite3
import bcrypt
conn = sqlite3.connect('RMHS.db')

user = ('abe',)
dat = "hi"
datToHash = dat.encode('UTF-8')
c = conn.cursor()



print(c.execute('SELECT * FROM Credentials WHERE c_credentialKey = ?',user))
(uname,pwd,salt) = c.fetchone()
print("PWD: " + str(pwd))

if(bcrypt.hashpw(datToHash,salt.encode('UTF-8')) == pwd):
    print("IT matches!")

conn.close()
