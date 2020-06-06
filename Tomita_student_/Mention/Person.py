class Persona:
    def __init__(self, path):
        self.path_file = path
        self.list_person_position = []
        self.dct_person_position = dict()
        self.text = ""

    def ListPersonPosition(self):
        self.text = ' '.join(self.text.split('\n'))
        while True:
            try:
                flag = self.text.find('\t{')
                start = self.text.find('\t\tName = ')
                end = self.text.find('\t}')
                string = self.text[start:end].split(' = ')[1].strip()
                if self.text[flag - 4: flag].strip() == 'SAO':
                    self.list_person_position.append([string, "SAO"])
                elif self.text[flag - 6: flag].strip() == 'Chief':
                    self.list_person_position.append([string, "Chief"])
                self.text = self.text[end + 1:]
            except:
                break

    def ReadFileText(self):
        file = open(self.path_file, 'r', encoding='utf-8')
        self.text = file.read()
        file.close()

    def DictFIOPosition(self):
        for i in self.list_person_position:
            if i[1] == 'SAO' and i[0] not in self.dct_person_position:
                self.dct_person_position[i[0]] = set()
                self.text = i[0]
            elif i[1] == 'SAO':
                self.text = i[0]

            if i[1] == 'Chief':
                self.dct_person_position[self.text].add(i[0])

    def PostProcessing(self):
        for i in self.dct_person_position.keys():
            if len(self.dct_person_position[i]) > 0:
                self.dct_person_position[i] = sorted(list(self.dct_person_position[i]))[0]
            else:
                self.dct_person_position[i] = ''

