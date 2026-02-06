FROM python:3.13-slim

WORKDIR /ItkAcademy
COPY /src /ItkAcademy/src

CMD ["python", "-m", "src.app"]
