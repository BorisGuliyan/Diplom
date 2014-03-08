import subprocess

class DocReader:

    @staticmethod
    def Reader(path):
        cmd = "antiword -m cp1251.txt " + path
        text = subprocess.check_output(cmd.split(" "), shell=True)
        return text.decode("cp1251")


#a = DOCReader.Reader("C:\\Boris\\Учеба\\Diplom\\test.doc")
#print(a.decode("cp1251"))

