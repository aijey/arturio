import os


os.environ['DATABASE_URL'] = "postg:5e1f78a6757d254a38893e2e80a15cab11e69c00e5ede338bc39bf2@ec2-174-129-29-101.compute-1.amazonaws.com:5432/dfrd04dtf0cajn"
os.environ['ADMIN_PASSWORD'] = "pass"
os.environ['TOKEN'] = "2222"

os.system('python3 main.py')
