class Attractions:
    def __init__(self, path):
        self.path_file = path
        self.text = ""
        self.list_attractions = []
        self.set_attractions = set()

    def ReadFileText(self):
        file = open(self.path_file, 'r', encoding='utf-8')
        self.text = file.read()
        file.close()

    def ListAttractions(self):
        list_string = self.text.split('\n')
        for i in range(len(list_string)):
            if '\tAttractionS' == list_string[i] or '\tAttractionFIO' == list_string[i]:
                self.list_attractions.append((list_string[i:i + 4]))

    def SetAttractions(self):
        for i in self.list_attractions:
            i = i[2].split(' = ')[1]
            self.set_attractions.add(i)





