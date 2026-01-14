import os

os.system("apt install -y mariadb-server mariadb-client")
os.system("yum install -y mariadb-server mariadb-client")
os.system("systemctl start mariadb")
os.system("systemctl enable mariadb")
os.system("mysql_secure_installation")

os.system('mysql -u root < ./sqlsetup.sql')

os.system("systemctl restart mariadb")