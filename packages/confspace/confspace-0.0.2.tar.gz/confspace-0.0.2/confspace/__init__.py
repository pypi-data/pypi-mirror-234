__version__ = "0.0.1"
from omegaconf import OmegaConf
from functools import reduce
class ConfigSpace:
    def __init__(self, config:OmegaConf, search_space:dict, name_call_back=None):

        if ConfigSpace.check_search_space_struct(search_space) == False:
            raise Exception("search_space 인자가 조건 만족을 안함")

        self.config = config
        self.search_space = search_space
        self.entire_space_size = ConfigSpace.get_entire_space_size(search_space)
        self.parameter_space_size = ConfigSpace.get_parameter_space_size(search_space)
        self.diviser = ConfigSpace.get_diviser(search_space)
        self.name_call_back = name_call_back
        self.iter_idx = 0

        search_space.keys()

    @staticmethod
    def get_diviser(search_space:dict)->dict:

        # diviser 구하기
        length_list = [len(space) for space in search_space.values()]
        diviser_list = [1 for i in range(len(length_list))]
        for i in range(len(length_list)-1, 0, -1):
            diviser_list[i-1] = diviser_list[i]*length_list[i]

        # dict로 변환
        diviser = {}        
        for i, key in enumerate(search_space.keys()):
            diviser[key] = diviser_list[i]
        return diviser
        
    @staticmethod
    def get_parameter_space_size(search_space:dict):
        # 파라미터 별 개수를 딕셔너리로 생성
        parameter_space_size = {}
        for name, values in search_space.items():
            parameter_space_size[name] = len(values)
        return parameter_space_size
    
    @staticmethod
    def get_entire_space_size(search_space:dict):
        # 전체 공간 크기 (파라미터 조합 개수) 반환
        paremeter_space_size_list = [len(space) for space in search_space.values()]
        return reduce(lambda x, y:x*y, paremeter_space_size_list)
    
    @staticmethod
    def check_search_space_struct(search_space:dict):
        # search_space의 모든 value가 list 형태인지 체크
        return all(isinstance(space, list) for space in search_space.values()) # 전부 리스트여야 함

    def get_parameter_indexes(self, i):
        indexes_dict = {}
        for parameter, diviser in self.diviser.items():
            indexes_dict[parameter] = (i//diviser)%self.parameter_space_size[parameter]        
        return indexes_dict

    def get_search_parameter(self, i):
        search_parameter = {}
        for parameter, index in self.get_parameter_indexes(i).items():
            search_parameter[parameter] = self.search_space[parameter][index]
        return search_parameter
    
    def get_config(self, i):
        search_parameter = OmegaConf.create(self.get_search_parameter(i))
        config = OmegaConf.merge(self.config, search_parameter)
        config["conf_space"] = {"try_num":i}
        if self.name_call_back != None:
            config["conf_space"]["path"] = self.name_call_back(i, search_parameter)
        return config

    def get_indexes(self, i):
        pass
    def __len__(self):
        return self.entire_space_size
    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_idx == self.__len__():
            raise StopIteration
        else:
            current_item = self.get_config(self.iter_idx) 
            self.iter_idx += 1
            return current_item
        
def name_call_back(i, search_parameter):
    return f"({i})_{'_'.join([value for value in search_parameter.values()])}.txt"

if __name__ == '__main__':
    config = OmegaConf.create({"1":"1", "2":"2"})
    search_space = {"A":["a1"],
                   "B":["b1", "b2"],
                   "C":["c1", "c2", "c3"]}

    conf_space = ConfigSpace(config=config, search_space=search_space, name_call_back = name_call_back)
    
    assert len(conf_space) == 6
    
    for conf in conf_space:
        print(conf)


