# python-app
 App code using CircleCI

## To connect to server for test and deploy
On Server create ssh key
1. ssh-keygen -t ed25519 -C "email@email.com" #Creates id_ed25519 and id_ed25519.pub key pair
2. Add id_ed25519 content to ssh key on circle ci
3. Add id_ed25519.pub content to authorized_keys on server.
https://www.digitalocean.com/community/tutorials/how-to-automate-deployment-using-circleci-and-github-on-ubuntu-18-04


## How to get gpx data from watch
How do I export data from the Health app on my iPhone?
1. On your iPhone, open the Health app.
2. Tap the Account icon in the top-right corner.
3. At the bottom of the page, select Export Health Data.
4. Confirm you want to export your Health data.
5. Wait for Health to prepare the file.
6. Choose how you want to share the exported data: AirDrop it, send it through messages or other apps, or save it to your device using Files. 
7. To find *.gpx files open exported folder and navigate to \apple_health_export\workout-routes. All workouts that use gps data will be logged here.

https://appletoolbox.com/how-to-export-apple-health-data-from-your-iphone-and-apple-watch/

## Setting up gunicorn on ubuntu
```bash
sudo apt install python3-pip python3 libpq-dev python3-dev gunicorn
sudo vi /etc/systemd/system/gunicorn.service
sudo vi /etc/systemd/system/gunicorn.socket
systemctl start gunicorn-prod.socket
systemctl enable gunicorn-prod.socket
sudo ln -s /etc/nginx/sites-available/vermontvt.com /etc/nginx/sites-enabled/vermontvt.com
nginx -t
sudo systemctl restart nginx
```
## Running app without setting up service/socket
```bash
gunicorn --workers=5 --threads=1 -b 0.0.0.0:8080 map-app:server
```

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04