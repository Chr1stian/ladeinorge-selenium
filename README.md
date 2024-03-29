# Your own endpoint to start charging on a Defa/Ladeinorge charger

```diff
- WARNING! Sends phone number and password to your account in plain text. Use at own risk and only on secure local networks.
```

## Objective
As ladeinorge/Defa does not provide a public API and I was unable to reverse-engineer it I created a simple Flask endpoint to start charging. It uses Selenium to click trough the webpage and start charging manually like a human would.

## Limitations
There is basically no error handling

### Linux
Add ```172.17.0.1 host.docker.internal``` to ```/etc/hosts```

## Requirements
- Docker

## Usage
### Start application
```zsh
docker-compose up -d
```

### Send request to start charging
```GET
http://docker-host-ip:5000/startCharging?phone=12345678&password=replaceMe&charger=chargerID
```

- Phone and password are credentials used when signing into [ladeinorge.no](https://ladeinorge.no)
- Charger ID can be found at the end of URL after searching and selecting a charger at [https://ladeinorge.no/start-ladestasjonen/](https://ladeinorge.no/start-ladestasjonen/)

### See program in action
Navigate to `docker-host-ip:8900` in a browser to open a VNC connection to the browser. Password is `secret`

### Check Selenium Grid
Navigate to `docker-host-ip:4444` in a browser