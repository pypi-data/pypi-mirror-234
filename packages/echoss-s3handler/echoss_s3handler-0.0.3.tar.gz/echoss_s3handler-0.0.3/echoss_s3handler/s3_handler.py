import os
import boto3
import cv2
import yaml
import json
import numpy as np
import time
import datetime
from tqdm import tqdm
from PIL import Image

class S3ClientHandler():
    """
    S3 client를 활용하기 위한 class
    input으로는 s3설정 정보가 있는 config파일을 읽은 다음의 data를 넣어주어야 한다.
    """
    def __init__(self, config_file: dict or str):
        if type(config_file) == dict:
            self.config_file = config_file
        elif type(config_file) == str:
            with open(config_file, 'r') as file:
                self.config_file = yaml.load(file, Loader=yaml.FullLoader)
        else:
            print("설정 파일을 dict형식 혹은 파일의 경로로 입력해주세요.")

        self.s3_client = boto3.client(service_name='s3',
                                      region_name=self.config_file['region_name'],
                                      aws_access_key_id=self.config_file['access_key_id'],  # 용어 정립 access_key -> access_key_id 23.07.13
                                      aws_secret_access_key=self.config_file['secret_access_key'],  # 용어 정립 access_token -> secret_access_key 23.07.13
                                      endpoint_url=self.config_file['endpoint_url'])

    def get_bucket_list(self):
        """
        S3의 버킷 리스트를 알기 위한 함수
        사용 방법은 S3ClientHandler class를 호출 한 뒤 별다른 파라미터 없이
        함수를 사용하면 된다.
        class 호출시 입력 받은 config파일을 사용합니다.
        """
        s3_cliet = self.s3_client
        bucket_list = s3_cliet.list_buckets()
        bucket_list_info = bucket_list['Buckets']
        return bucket_list_info

    def get_object_info(self, bucket, file_path):
        """
        object들의 정보(마지막 수정, s3_link)를 output으로 내보내는 함수
        """
        object_info = self.s3_client.head_object(Bucket=bucket, Key=file_path)
        last_modified = object_info['LastModified']
        last_modified = last_modified+datetime.timedelta(hours=9)
        last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")

        url = "%s/%s/%s" % (self.config_file['endpoint_url'], bucket, file_path)
        return last_modified, url

    def split_s3_key(self, s3_key):
        key = str(s3_key)
        last_name = key.split('/')[-1]
        return key.replace(last_name, ""), last_name

    # 빈문자열 체크
    def is_blank(self, str):
        if str and str.strip():
            return False
        return True
    def get_object_list(self, bucket, prefix, after_ts=0):
        """
        after_ts 에는 "2023-02-28 00:00:00" 포맷으로 작성해야 한다.
        :param bucket: bucket name
        :param s3_prefix: 버킷 이후 공통되는 경로
        :param after_ts: 입력 되는 시간 이후 수정된 데이터만 추리기 위한 파라미터 ex) "2023-02-28 00:00:00"
        :param pattern: 예를 들면 확장자
        :return:
        """
        object_list = []
        count = 0
        objects = self.s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        for object in tqdm(objects['Contents']):
            count += 1

            last_modified_dt = object['LastModified']
            s3_ts = last_modified_dt.timestamp() * 1000

            if after_ts != 0:
                after_ts_ = datetime.datetime.strptime(after_ts, "%Y-%m-%d %H:%M:%S")
                after_ts__ = time.mktime(after_ts_.timetuple()) * 1000
            else:
                after_ts__ = after_ts
            if s3_ts > after_ts__:
                s3_path, s3_filename = self.split_s3_key(object['Key'])
                # directory check
                if self.is_blank(s3_filename) or s3_filename.endswith("/"):
                    pass
                else:
                    object_list.append(s3_path + s3_filename)

        return object_list

    def download_object(self):
        """
        object를 로컬에 다운 받기 위한 함수
        S3ResourceHandler에서 사용 권장
        """
        pass

    def upload_object(self):
        """
        object를 로컬에 업로드 하기 위한 함수
        S3ResourceHandler에서 사용 권장
        """
        pass

    def modify_object(self):
        """
        object를 메모리상에서 수정 한 뒤 덮어쓰거나 업로드 하기 위한 함수
        S3ResourceHandler에서 사용 권장
        """
        pass

class S3ResourceHandler():
    def __init__(self, config_file):
        """

        :param config_file: Not file_path, Put in the yaml data or dict data
        """
        if type(config_file) == dict:
            self.config_file = config_file
        elif type(config_file) == str:
            with open(config_file, 'r') as file:
                self.config_file = yaml.load(file, Loader=yaml.FullLoader)
        else:
            print("설정 파일을 dict형식 혹은 파일의 경로로 입력해주세요.")

        if self.config_file['endpoint_url'] == None:
            self.s3 = boto3.Session(region_name=self.config_file['region_name'],
                                    aws_access_key_id=self.config_file['access_key_id'],  # 용어 정립 access_key -> access_key_id 23.07.13
                                    aws_secret_access_key=self.config_file['secret_access_key']).resource(service_name='s3')  # 용어 정립 access_token -> secret_access_key 23.07.13
        else:
            self.s3 = boto3.Session(region_name=self.config_file['region_name'],
                                    aws_access_key_id=self.config_file['access_key_id'],  # 용어 정립 access_key -> access_key_id 23.07.13
                                    aws_secret_access_key=self.config_file['secret_access_key']).resource(service_name='s3',  # 용어 정립 access_token -> secret_access_key 23.07.13
                                                                                                     endpoint_url=self.config_file['endpoint_url'])
    def get_bucket_list(self, date_info=False):
        """
        S3ClientHandler class의 get_bucket_list 함수를 사용하며,
        data_info 옵션을 사용하여
        단순히 버킷의 리스트만 출력하거나, 버킷의 생성날짜까지 확인할 수 있도록 한 함수
        :param date_info: True or False
        :return: If date_info is True -> Output : Dict,
        False -> Output : List
        """
        s3_client = S3ClientHandler(self.config_file)
        bucket_list_info = s3_client.get_bucket_list()
        if date_info:
            bucket_list = dict()
            for bucket_info in bucket_list_info:
                name = bucket_info['Name']
                date = bucket_info['CreationDate'].strftime('%Y-%m-%d')
                bucket_list[name] = date
        else:
            bucket_list = list()
            for bucket_info in bucket_list_info:
                name = bucket_info['Name']
                bucket_list.append(name)

        return bucket_list

    def select_bucket(self, bucket):
        """
        s3에서 작업 하기 전 작업할 버킷을 선택하는 단계 독립적으로는 거의 사용하지 않음
        거의 아래의 함수들에 사용
        """
        s3bucket = self.s3.Bucket(bucket)
        return s3bucket

    def split_s3_key(self, s3_key):
        key = str(s3_key)
        last_name = key.split('/')[-1]
        return key.replace(last_name, ""), last_name

    # 빈문자열 체크
    def is_blank(self, str):
        if str and str.strip():
            return False
        return True

    def get_object_list(self, bucket, s3_prefix, after_ts=0, pattern=None, tqdm_=True):
        """
        after_ts 에는 "2023-02-28 00:00:00" 포맷으로 작성해야 한다.
        :param bucket: bucket name
        :param s3_prefix: 버킷 이후 공통되는 경로
        :param after_ts: 입력되는 시간 이후 수정된 데이터만 추리기 위한 파라미터 ex) "2023-02-28 00:00:00"
        :param pattern: 예를들면 확장자
        :return:
        """
        s3bucket = self.s3.Bucket(bucket)
        objects = s3bucket.objects.filter(Prefix=s3_prefix)

        filenames = []
        count = 0
        if tqdm_:
            iterator = tqdm(objects)
        else:
            iterator = objects

        for obj in iterator:
            count += 1
            if pattern is not None and not pattern in obj.key:
                continue

            last_modified_dt = obj.last_modified
            s3_ts = last_modified_dt.timestamp() * 1000
            if after_ts != 0:
                after_ts_ = datetime.datetime.strptime(after_ts, "%Y-%m-%d %H:%M:%S")
                after_ts__ = time.mktime(after_ts_.timetuple())*1000
            else:
                after_ts__ = after_ts
            if s3_ts > after_ts__:
                s3_path, s3_filename = self.split_s3_key(obj.key)
                # directory check
                if self.is_blank(s3_filename) or s3_filename.endswith("/"):
                    pass
                else:
                    filenames.append(s3_path + s3_filename)
        return filenames
        # return {
        #     'directory': s3_prefix,
        #     'items': filenames,
        #     'login_id': pattern
        # }

    def download_object(self, bucket_name, target_file_path, download_file_path):
        """
        버킷내의 object를 로컬로 다운로드 하기 위한 함수
        :param bucket_name: 버킷명
        :param target_file_path: 다운로드 하고자하는 버킷 내의 object 이름(경로)
        :param download_file_path: 로컬에 다운로드 받고자 하는 경로(파일의 이름 포함)
        :return:
        """
        s3bucket = self.s3.Bucket(bucket_name)
        s3bucket.download_file(target_file_path, download_file_path)

    def upload_object(self, bucket_name, target_file_path, upload_file_path, ExtraArgs = None):
        """
        로컬의 파일을 s3로 업로드 하기 위한 함수
        :param bucket_name: 버킷명
        :param target_file_path: 업로드 하고자하는 로칼의 파일 경로(파일 이름 포함)
        :param upload_file_path: S3에 업로드 하고 싶은 경로(폴더 구조와 파일의 이름 포함)
        :param ExtraArgs: metadata 입력 ex. {'Metadata': {'myKey': 'myValue'}, 'ACL': 'public-read'}
        :return:
        """
        s3bucket = self.s3.Bucket(bucket_name)
        if ExtraArgs == None:
            s3bucket.upload_file(target_file_path, upload_file_path)
        else:
            s3bucket.upload_file(target_file_path, upload_file_path, ExtraArgs)

    def put_object(self, object_body, object_name, trg_bucket):
        """
        로컬의 파일을 s3로 업로드 하기 위한 함수
        이 함수는 json파일또는 txt파일을 업로드하는데 사용
        (이미지 업로드에 사용할 수 있으나 이미지의 경우 입력 데이터를 잘 넣어주어야 함)
        이미지를 업로드 하고 싶다면 yolov7/utils/detect.py 파일 164번째 줄 참고
        :param object_body: Object data
        :param object_name: The full path to upload
        :param trg_bucket: The bucket to upload
        :return:
        """
        extention = os.path.basename(object_name).split(".")[-1]
        if (extention == ".json") | (extention == "json"):
            object_body = json.dumps(object_body, indent="\t", ensure_ascii=False)
        trg_s3bucket = self.select_bucket(trg_bucket)
        trg_s3bucket.put_object(Body=object_body, Key=object_name, ACL="public-read")

    def s3tos3_put_object(self, src_file_name, trg_file_name, trg_s3_config, fin_print=True):
        """
        ex) src_s3 = S3ResourceHandler(src_s3_config)\n
        src_s3.s3tos3_put_object(Put parameters)
        :param src_file_name: File path
        :param trg_file_name: Final file path
        :param trg_s3_config: Target s3 config data, yaml data
        :param fin_print:
        :return: None
        """
        trg_s3 = S3ResourceHandler(trg_s3_config)
        extention = os.path.basename(src_file_name).split(".")[-1]
        file = self.read_file(self.config_file['bucket'], src_file_name)
        file.seek(0)
        if (extention == ".json") | (extention == "json"):
            file = json.loads(file.read().decode())
        trg_s3.put_object(file, trg_file_name, trg_s3_config['bucket'])
        if fin_print:
            print(f"{colorstr(self.config_file['bucket'])}: {src_file_name} {colorstr('red', 'bold', '->')} {colorstr(trg_s3_config['bucket'])}: {trg_file_name}")

    def move_object(self, src_file_name, trg_file_name, bucket):
        """
        Args:
            src_file_name(str) : 원본 파일 명(버킷명을 포함하지 않음) \n
            trg_file_name(str) : 이동 대상 경로 파일 명(버킷명을 포함하지 않음) \n
            bucket(str) : 버킷명 \n
        Returns:
            src_file들을 같은 버킷 내에서 이동
        """
        self.s3.Object(bucket,trg_file_name).copy_from(CopySource='/'.join([bucket,src_file_name]), ACL='public-read')
        self.s3.Object(bucket,src_file_name).delete()

    def remove_empty_folder(self, bucket):
        """
        버킷 내부 Temp 폴더 속 빈 폴더들을 자동으로 삭제시키는 함수
        Args:
            bucker(str) : 버킷명
        Returns:
            빈 폴더들을 자동으로 삭제
        """
        s3_bucket = self.select_bucket(bucket)
        for obj in s3_bucket.objects.filter(Prefix='Temp/',Delimiter='/*'):
            # 폴더 객체가 없는 경우에만 삭제
            if obj.key[-1] != '/':
                continue
            prefix = obj.key
        
            # 해당 폴더의 객체 수를 세어 빈 폴더인지 확인
            num_objects = sum(1 for _ in s3_bucket.objects.filter(Prefix=prefix))
            if (num_objects > 0) and (prefix != 'Temp/'):
                print('Delete empty folder -',prefix)
                s3_bucket.objects.filter(Prefix=prefix).delete()
                continue

    def read_file(self, bucket, file_name):
        """
        파일을 메모리상으로 읽기 위한 함수
        
        output으로 나오는 file을 사용하는것은 아래와 같습니다.
        ex)
        json의 경우
        file.seek(0)  # 커서를 가장위로 올린다.
        dict_ = file.read().decode()  # 바이너리 상태의 데이터를 읽고 디코딩한다.
        json_data = json.loads(dict_)  # 디코딩된 데이터를 json 라이브러리를 이용하여 메모리로 읽는다.
        
        txt의 경우
        file.seek(0)
        l = [x.split() for x in file.read().decode().strip().splitlines()]
        
        :param bucket: 버킷 명
        :param file_name: object의 path
        :return: file
        """
        import io
        s3bucket = self.select_bucket(bucket)
        file = io.BytesIO()
        obj = s3bucket.Object(file_name)
        obj.download_fileobj(file)
        return file

    def read_image(self, bucket, file_name, library="cv2"):
        """
        이미지 파일을 메모리상으로 읽기 위한 함수
        이후 사용되는 이미지의 형식에 따라 opencv, PIL라이브러리중 선택하여 사용 가능
        
        :param bucket: 버킷 명
        :param file_name: object path
        :param library: "cv2" or "PIL"
        :return: img
        """
        bucket = self.select_bucket(bucket)
        object_ = bucket.Object(file_name)
        response = object_.get()
        img_body = response['Body']
        del response  # delete memory
        try:
            if library == "cv2":
                img_ = img_body.read()
                img = cv2.imdecode(np.asarray(bytearray(img_)), cv2.IMREAD_COLOR)
            elif library == "PIL":
                img = Image.open(img_body)
            else:
                raise Exception("Input only 'cv2' or 'PIL' in the library parameter")

            return img

        except Exception as e:
            print(e)

    def get_object_info(self, bucket, file_path):
        """
        object의 최종 수정일시와 s3_link를 output으로 출력한다.
        출력된 값을 DB에 적재할 수 있다. 
        
        :param bucket: 버킷 명
        :param file_path: object path
        :return: (last_modified, url)
        """
        object_info = self.s3.Object(bucket, file_path)
        last_modified = object_info.last_modified
        last_modified = last_modified + datetime.timedelta(hours=9)
        last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")

        url = "%s/%s/%s" % (self.config_file['endpoint_url'], bucket, file_path)

        return last_modified, url

# print시 문자에 색을 넣을 수 있는 함수
def colorstr(*input):
    # Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
    colors = {'black': '\033[30m',  # basic colors
              'red': '\033[31m',
              'green': '\033[32m',
              'yellow': '\033[33m',
              'blue': '\033[34m',
              'magenta': '\033[35m',
              'cyan': '\033[36m',
              'white': '\033[37m',
              'bright_black': '\033[90m',  # bright colors
              'bright_red': '\033[91m',
              'bright_green': '\033[92m',
              'bright_yellow': '\033[93m',
              'bright_blue': '\033[94m',
              'bright_magenta': '\033[95m',
              'bright_cyan': '\033[96m',
              'bright_white': '\033[97m',
              'end': '\033[0m',  # misc
              'bold': '\033[1m',
              'underline': '\033[4m'}
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']

if __name__ == '__main__':
    import yaml
    with open("../data/45_abalone_data/yolo_data/ai_solution_dataset_test.yaml") as f:
        data_dict = yaml.load(f, Loader=yaml.SafeLoader)  # data dict
    s3resource = S3ResourceHandler(data_dict)
    bucket_list = s3resource.get_bucket_list()
    print(bucket_list)

    # with open("../data/45_abalone_data/yolo_data/AI_Hub_s3_config.yaml") as f:
    #     aihub_data_dict = yaml.load(f, Loader=yaml.SafeLoader)
    # objects_list = s3resource.get_object_list(data_dict['bucket'], "bb_seg_data")
    # print(objects_list[0])
    # new_name = f"113.패류 종자생산(전복) 데이터/02.저작도구/{os.path.basename(objects_list[0])}"
    #
    # s3resource.s3tos3_put_object(objects_list[0], new_name, data_dict, aihub_data_dict)
    object_lists = s3resource.get_object_list(data_dict['bucket'], data_dict['yolo_data_path'], "2023-02-28 14:00:00")
    print(len(object_lists))
    object_lists = s3resource.get_object_list(data_dict['bucket'], data_dict['yolo_data_path'])
    print(len(object_lists))
    # ob_info = s3resource.get_object_info(data_dict['bucket'], object_lists[0])
    # print(ob_info)

    s3client = S3ClientHandler(data_dict)
    # ob_info_client = s3client.get_object_info(data_dict['bucket'], object_lists[0])
    # print(ob_info_client)
    #
    objects = s3client.get_object_list(data_dict['bucket'], data_dict['yolo_data_path'], "2023-02-28 14:00:00")
    print(len(objects))
    objects = s3client.get_object_list(data_dict['bucket'], data_dict['yolo_data_path'])
    print(len(objects))
