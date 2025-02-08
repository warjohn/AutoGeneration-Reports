import yaml
import sklearn as sk

class LoaderConfig():

    def __init__(self, filepath):
        self.pictures = None
        self.filepath = self.__check(filepath)
        self.metrics = []
        self.steps = []
        self.model = None
        self.config = None
        self.searchFlag = None
        self.pipeline = None

    def loadPictures(self):
        tmp = []
        for i in self.config['pictures']:
            tmp.append(i['name'])
        return tmp

    def __check(self, filepath):
        if filepath is None:
            raise ValueError("File doesn't exist")
        return filepath

    def __Searchflag(self):
        return True if self.config['selectionParams']['enable'] else False

    def openFile(self):
        with open(self.filepath, 'r') as file:
            self.config = yaml.safe_load(file)
        self.searchFlag = self.__Searchflag()

    def loadTransformers(self):
        transformers = []
        for transformer in self.config['transformers']:
            transformer_class = getattr(sk.preprocessing, transformer['name'])
            transformers.append((transformer['name'], transformer_class(**transformer['params'])))

        for i in transformers:
            self.steps.append(i)

    def loadMetrics(self):
        self.metrics = self.config['metrics']

    def loadModel(self):
        model_class = self.__get_model_by_name(self.config['model']['name'])
        self.model = model_class(**self.config['model']['params'])
        self.steps.append((f"{self.model.__class__.__name__}", self.model))

    def geneartePipelines(self):
        self.pipeline = sk.pipeline.Pipeline(self.steps)

    def generateWay(self):
        self.openFile()
        self.loadTransformers()
        self.loadMetrics()
        self.loadModel()
        self.geneartePipelines()

        self.pictures = self.loadPictures()

        if self.searchFlag:
            selectonModel = self.__get_model_by_name(self.config['selectionParams']['name'])
            self.pipeline = selectonModel(self.pipeline,
                                          param_grid = self.config['selectionParams']['param_grid'],
                                          **self.config['selectionParams']['params'])
        return self.pipeline


    def __get_model_by_name(self, model_name):
        for module_name in dir(sk):
            module = getattr(sk, module_name)
            if isinstance(module, type(sk)):
                for class_name in dir(module):
                    model_class = getattr(module, class_name)
                    if isinstance(model_class, type):
                        if model_name.lower() in class_name.lower():
                            return model_class
        return None