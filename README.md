# back.ih.by

This app tested on ubuntu 24.04 vs python 3.12, mint vs python 3.10

To run this app:
+ install myslq driver

create a .sh file, and paste this code. (you need change to your ubuntu version) then run it ./your_sh_name.sh
```
# Download the package to configure the Microsoft repo
#curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
curl -sSL -O https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev      
```
+ change values in file /etc/ssl/openssl.cnf
```
ssl_conf = ssl_sect
system_default = system_default_sect
MinProtocol = TLSv1.2
CipherString = DEFAULT:@SECLEVEL=0
```
+ install python3, pip3, python3-venv
+ copy this project 
+ cd project/dj
+ python3 -m venv venv
+ source venv/bin/activate (activate virtual enviroment)
+ pip3 install -r requirements.txt (install dependencies)
+ python3 manage.py migrate
+ python3 manage.py createsuperuser
+ python3 manage.py runserver {ip:port|port}
+ ./manage.py migrate (apply migrations for DB, if you need)
+ ./manage.py loaddata fixture/role.json (if you run at first)
+ ./manage.py loaddata fixture/type_of_work.json (if you run at first)
+ ./manage.py loaddata fixture/warehouse.json (if you run at first)
+ ./manage.py loaddata fixture/warehouse_action.json (if you run at first)
+ ./manage.py runsever {ip:port} (start app)


***.env:***
```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

DB_ENGINE=
DB_DRIVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

ORACLE_DB_NAME=
ORACLE_DB_USER=
ORACLE_DB_PASSWORD=

API_USERNAME=
API_PASSWORD=
API_1C_URL_GTD=
```



to upload DB table to json use
python3 manage.py dumpdata account.Role --output=fixture/role.json
python3 manage.py dumpdata warehouse.TypeOfWork --output=fixture/type_of_work.json
python3 manage.py dumpdata warehouse.Warehouse --output=fixture/warehouse.json
python3 manage.py dumpdata warehouse.WarehouseAction --output=fixture/warehouse_action.json