import os
import happybase

master = os.getenv('TARGET_HOST') if os.getenv('TARGET_HOST') else 'bd1'

print("Master", master)
connM=happybase.Connection(host=master)
print(connM.tables())

# Create Schema
try:
    connM.create_table(
        'student',
        {
            'name': dict(max_versions=10),
            'sex': dict(),
            'age': dict()
        }
    )
except:
    pass

# Upsert Data
ts = connM.table('student')
bat = ts.batch()
bat.put(row='rk_1', data={'name:': 'jason', 'age:': '46', 'sex:': 'man'})
bat.put(row='rk_2', data={'name:': 'nancy', 'age:': '34', 'sex:': 'girl'})
bat.send()

print(ts.row('rk_1'))

# Scan
for key, value in ts.scan():
    print(key, value)
    
print("Done!")
