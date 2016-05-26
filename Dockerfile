FROM python:onbuild

ENTRYPOINT [ "python", "-u", "/usr/src/app/announce.py", "--daemon" ]
