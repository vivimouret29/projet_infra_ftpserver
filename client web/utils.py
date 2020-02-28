#!/usr/bin/python3
import ftplib


class Ftp:
    def __init__(self, path, user, passwd):
        self.path = path
        self.user = user
        self.parser = ftplib.FTP()
        self.parser.connect(path)
        self.parser.login(user, passwd)

    def ls(self):
        files = []
        self.parser.dir(files.append)
        for i in range(len(files)):
            files[i] = files[i].split(" ")
            files[i] = [j for j in files[i] if j != ""]
        return(files)

    def cd(self, fichier):
        pwd = self.parser.pwd()
        path = pwd + '/' + fichier
        self.parser.cwd(path)
        self.path = self.parser.pwd()
        return self.ls()

    def mkdir(self, name):
        self.parser.mkd(self.path + '/' + name)
        self.ls()

    # def dowload(self, target):
    #     with open(file_copy, 'w') as fp:
    #         res = self.parser.retrlines('RETR ' + target, fp.write)


# if __name__ == '__main__':
#     parser = Ftp('')
#     parser.ls()
#     parser.cd('test')
#     parser.mkdir('test2')
