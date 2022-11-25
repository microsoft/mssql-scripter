FROM python:3.11-slim-bullseye as builder
RUN pip install future

WORKDIR /bld
COPY . . 
RUN python3 dev_setup.py
RUN python3 build.py 
RUN python build.py build manylinux1_x86_64
RUN apt update && apt -y install bzip2 wget
RUN wget https://github.com/microsoft/go-sqlcmd/releases/download/v0.10.0/sqlcmd-v0.10.0-linux-x64.tar.bz2
RUN tar -xvf sqlcmd-v0.10.0-linux-x64.tar.bz2


FROM python:3.11-slim-bullseye
COPY --from=builder  /bld/sqlcmd /usr/bin/sqlcmd 
COPY --from=builder  /bld/dist/mssql_scripter-1.0.0a23-py2.py3-none-manylinux1_x86_64.whl /tmp
RUN pip install  /tmp/mssql_scripter-1.0.0a23-py2.py3-none-manylinux1_x86_64.whl
RUN rm -rf /tmp/mssql_scripter-1.0.0a23-py2.py3-none-manylinux1_x86_64.whl
RUN apt update && apt -y install libicu67
CMD ["python3", "-m","sqlscripter"]
