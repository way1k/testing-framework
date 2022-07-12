FROM python:3.10.5-buster

# Изменение SECLEVEL для openssl
#RUN sed -i "s/\(MinProtocol *= *\).*/\1TLSv1.0 /" "/etc/ssl/openssl.cnf"
#RUN sed -i "s/\(CipherString *= *\).*/\1DEFAULT@SECLEVEL=1 /" "/etc/ssl/openssl.cnf"

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Unpacking the pytest.ini file
COPY pytest.ini.dist .
RUN cp pytest.ini.dist pytest.ini
