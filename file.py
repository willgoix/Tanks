import json


# Thanks Otávio Capovilla by the idea

class File(object):

    def __init__(self, fileName, default={}):
        self.fileName = fileName
        self.jsonFile = self.read(default)

    def read(self, default):
        try:
            file = open(self.fileName + '.json', 'r')
            jsonFile = json.load(file)
            file.close()

            return jsonFile
        except Exception as e:
            print("Ocorreu um erro ao ler o arquivo '{}' (configuracao default sera usada): {}".format(self.fileName, e))
        return default

    def get(self, key):
        if key in self.jsonFile:
            return self.jsonFile.get(key)
        else:
            return None

    def set(self, key, value):
        try:
            self.jsonFile.update({key: value})
        except Exception as e:
            print("Ocorreu um erro ao definir valor em '{}': {}".format(self.fileName, e))

    def remove(self, key):
        try:
            self.jsonFile.pop(key)
        except Exception as e:
            print("Ocorreu um erro ao remover valor de '{}': {}".format(self.fileName, e))

    def save(self):
        try:
            file = open(self.fileName + '.json', 'w')
            json.dump(self.jsonFile, file, indent=4, sort_keys=True, separators=(',', ': '))
            file.close()
        except Exception as e:
            print("Ocorreu um erro ao salvar o arquivo '{}': {}".format(self.fileName, e))
