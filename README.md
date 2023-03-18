# python-app
 App code using CircleCI

On Server create ssh key
1. ssh-keygen -t ed25519 -C "email@email.com" #Creates id_ed25519 and id_ed25519.pub key pair
2. Add id_ed25519 content to ssh key on circle ci
3. Add id_ed25519.pub content to authorized_keys on server.