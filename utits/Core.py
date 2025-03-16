from tqdm import tqdm
from PIL import Image
import distance,json,os,cv2,imagehash,threading
from typing import Literal
from pillow_heif import register_heif_opener
register_heif_opener()

Config = {
    "Hash_Size":12,
    "Search_Distance":25,
    "Confidence_Distance":10,
}

class Indexing:
    def __init__(self,Index_File:os.PathLike=''):
        if Index_File == '':
            self.Index = {
                'MOV':{},
                'HEIC':{}
            }
        else:
            self.Index = json.loads(open(Index_File,"r",encoding="utf-8").read())

    def _save_index(self,path_to_save:os.PathLike)->str:
        path = os.path.join(path_to_save,'./Indexed.json')
        open(path,"w",encoding="utf-8").write(json.dumps(self.Index,indent=2))
        return os.path.abspath(path)

    def Create_Index(self,HEIC_Path:os.PathLike='',Mov_Videos_Path:os.PathLike='',Thread_Num:int=1):
        """
        :param path: Path of .MOV file
        :param intervel: Intervel to Calculate
        :return:
        """
        def split_list(lst,nums:int):
            # 计算每份的长度
            n = len(lst)
            part_size = n // nums
            remainder = n % nums
            # 分割列表
            result = []
            start = 0
            for i in range(nums):
                if i < remainder:
                    end = start + part_size + 1
                else:
                    end = start + part_size
                result.append(lst[start:end])
                start = end

            return result

        def _cal(format:list,types:Literal['HEIC','MOV'],file_path:os.PathLike,thread_num:int=1):
            List = [fn for fn in os.listdir(file_path)
                if any(fn.endswith(formats) for formats in format)
            ]
            _all_indexed = self.Index['HEIC']
            _all_indexed.update(self.Index['MOV'])
            _to_calculate = [fn for fn in List if fn not in _all_indexed]
            if types == 'HEIC':
                print(f"Hashing {len(_to_calculate)} HEIC items")
                for i in tqdm(_to_calculate,desc='Calculating Hash'):
                    _path = os.path.join(file_path,i)
                    self.Index['HEIC'].update({i:imagehash.phash(Image.open(_path),hash_size=Config["Hash_Size"]).__str__()})
            if types == 'MOV':
                _threads = []
                print(f"Hashing {len(_to_calculate)} MOV items, with Thread {thread_num}")
                for item in split_list(lst=_to_calculate,nums=thread_num):
                    _t = threading.Thread(target=self._index_videos,kwargs={'file_path':file_path,'paths':item})
                    _threads.append(_t)
                    _t.start()
                for _t in _threads: _t.join()

        if HEIC_Path != '': _cal(format=['heic','HEIC'],types='HEIC',file_path=HEIC_Path,thread_num=Thread_Num)
        if Mov_Videos_Path != '': _cal(format=['mov','MOV'],types='MOV',file_path=Mov_Videos_Path,thread_num=Thread_Num)
        _p = self._save_index('./')
        print(f"Indexfile saved to {_p}")

    def _index_videos(self,file_path:str,paths:list,intervel:int=3)->dict:
        for i in paths: self.Index['MOV'].update(self.Index_SingleVideo(path=os.path.join(file_path,i),intervel=intervel))

    def Index_SingleVideo(self,path:str,intervel:int=1)->dict:
        """
        :param path: Path of .MOV file
        :param intervel: Intervel to Calculate
        :return: 
        """
        mov_name = os.path.split(path)[-1] #xxx.mov
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():  print(f"can't open {mov_name}")
        frame_count = 0
        #intervel = int(cap.get(cv2.CAP_PROP_FPS)) # 每秒的帧数
        result = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_count += 1
                if frame_count % intervel == 0:
                    hash = imagehash.phash(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)),hash_size=Config["Hash_Size"]).__str__()
                    result.append(hash)
            else:
                break
        cap.release()
        return {mov_name:result}
    
class Connect:
    def __init__(self,Indexed_File:os.PathLike):
        self.Index = json.loads(open(Indexed_File,"r",encoding="utf-8").read())
    
    def Compare(self)->list:
        print("Start Comparing")
        result = []
        for heic_name,heic_hash in tqdm(self.Index["HEIC"].items(),desc='Compareing HEIC'):
            for mov_name,mov_hashs in self.Index['MOV'].items():
                for mov_hash_item in mov_hashs:
                    distancse = int(distance.hamming(heic_hash,mov_hash_item))
                    if distancse < Config["Search_Distance"]:
                        result.append({'HEIC_File':heic_name,'MOV_File':mov_name,"Confidence":round(1-distancse/len(heic_hash),2)})
                    if distancse < Config["Confidence_Distance"]:
                        break
        return result
    
class LLM:
    def __init__(self):
        self.Prompt = ''

if __name__ =="__main__":
    ...