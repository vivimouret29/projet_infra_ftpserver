# Projet Infra

## Création serveur VsFTPd

Il faut commencer par télécharger les packages vsftpd et ftp pour pouvoir tester et s'y connecter.
Installer Rsyncd, pour améliorer la connexion ssh prochainement.

```bash
$ sudo yum –y install vsftpd ftp
$ sudo yum -y install rsyncd
```

Vérifier que le serveur vsftpd ne s'est pas lancé avec :

```bash
systemctl status vsftpd
systemctl start vsftpd
systemctl stop vsftpd
```


Dans `/etc/vsftpd/vsftpd.conf`, faites une backup des configurations de base puis décommentez ou modifiez :
(le port 22 est par défaut)

```
anonymous_enable=NO
local_umask=022
xferlog_file=/var/log/xferlog
ascii_upload_enable=YES
ascii_download_enable=YES
use_localtime=YES
local_root=/home/$USER
```

Il faut maintenant ouvrir les ports utilisé par le serveur : 

```bash
$ firewall-cmd --permanent --add-port=22/tcp
$ firewall-cmd --permanent --add-service=ftp
```

Et relancer le pare-feu :

```bash
$ firewall-cmd --reload
```

Par défaut, VsFTPd n'accepte pas les connexions avec root.
Il faut créer un nouvel utilisateur où le /home/ sera la page d'accueil de l'utilisateur :

```bash
$ useradd ftpadmin
$ passwd ftpadmin
```

On peut maintenant lancer le serveur ftp.
Pour pouvoir se connecter à notre serveur FTP en ligne de commande, il suffit de taper votre nom de domaine ou l'IP du serveur : 

```bash
$ ftp 192.168.56.2
$ ftp localftpservice.net
```

Ensuite à vous de rentrer votre user et mot de passe, une fois la connexion établie, vous pouvez utiliser votre serveur librement.

```bash
$ ftp localftpservice.net
Connected to localftpservice.net (192.168.56.2).
220 Please, enter your id and password
Name (localftpservice.net:root): ftpadmin
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```

Maintenant, on peut créer la backup, archiver le `/home` puis avec la commande ci-dessus, on envoie la fichier **backup** sur la vm backup
 
```bash
$ rsync -avz backup_ftpserver.zip root@192.168.58.2:/root
```

C'est manuel, mais on a mieux, en utilisant crontab on peut lui demander de crére des archives à des horaires précises :

```bash
$ crontab -e
* */1 * * * rsync -a /home/ root@192.168.58.2:/root
$ crontab -l
```

On demande ici de faire la mise à jour de la backup toutes les heures.
On aura un mail, disponible dans `/var/spool/mail/root` qui nous affiche les erreurs possible en cas d'échec.