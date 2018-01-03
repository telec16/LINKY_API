import linky
import ids


print("logging in as " + ids.username + "...")
token = linky.login(ids.username, ids.password)
print("logged in successfully")
res = linky._get_data(token, linky.R_ID_DAY,  '23/11/2017', '23/12/2017')
print(res)
