# Decrypting the test secrets

To decrypt the test secrets, get the password from the admin. Then, use GPG:

    gpg --output secrets.yml --decrypt secrets.yml.gpg

To encrypt new settings, use:

    gpg --encrypt --output secrets.yml.gpg --symmetric secrets.yml

