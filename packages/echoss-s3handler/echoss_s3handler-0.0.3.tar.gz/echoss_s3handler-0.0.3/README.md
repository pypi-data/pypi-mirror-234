## import 방법
 -  from echoss_s3handler import s3_handler

custom yolov7과 image_utils의 함수 사용시 S3에 있는 데이터를 사용하고자 하여 만든 Class

크게 두가지의 class가 존재함
1. client를 활용한 clas
2. resource를 활용한 class

# Client Class
내부 주요 함수
```
    # s3 config 파일 읽기
    with open("../s3 config file path/ai_solution_dataset_test.yaml") as f:
        data_dict = yaml.load(f, Loader=yaml.SafeLoader)
    # class 할당
    s3_client = S3ClientHandler(data_dict)
    
    
    s3_client.get_bucket_list()
     - 현재 config 파일에 해당하는 접속 계정에 있는 bucket들의 정보를 출력해준다.(버킷명, 버킷 생성날짜 등)
    
    s3_client.get_object_info()
     - parameter로 입력된 object의 마지막 수정일시(YYYY-MM-DD HH:MM:SS 꼴)와 s3link를 출력해준다.
    
    s3_client.get_object_list()
     - parameter로 입력된 prefix와 after_ts(기준이되는 시간 입렵 포맷:"2023-02-28 00:00:00")를 확인하여 object들의 path를 list로 반환한다.
```

# Resource Class
내부 주요 함수
```
    # s3 config 파일 읽기
    with open("../s3 config file path/ai_solution_dataset_test.yaml") as f:
        data_dict = yaml.load(f, Loader=yaml.SafeLoader)
    # class 할당
    s3_resource = S3ResourceHandler(data_dict)
    
    
    s3_resource.get_bucket_list()
     - 현재 config 파일에 해당하는 접속 계정에 있는 bucket들의 정보를 출력해준다.(버킷명, 버킷 생성날짜 등)
     - data_info를 True로 하게 되면 출력이 버킷명이 key값, 마지막 생성일자를 vlaue로 하는 Dict형태로 출력되며,
     false로 하면 버킷의 목록만 list형태로 출력.
    
    s3_resource.get_object_info()
     - parameter로 입력된 object의 마지막 수정일시(YYYY-MM-DD HH:MM:SS 꼴)와 s3link를 출력해준다.
    
    s3_resource.get_object_list()
     - parameter로 입력된 prefix와 after_ts(기준이되는 시간 입렵 포맷:"2023-02-28 00:00:00")를 확인하여 object들의 path를 list로 반환한다.
    
    s3_resource.download_object()
     - S3에 있는 object를 local에 다운로드하기 위한 함수
    
    s3_resource.upload_object()
     - locla에 있는 데이터를 S3에 업로드하기 위한 함수
    
    s3_resource.put_object()
     - 메모리상으로 저장되어있는 json혹은 txt 데이터를 S3 object로 업로드하는데 사용하는 함수
     - 이미지도 업로드할 수 있으나 이때에는 아래와 같이 이미지를 PIL, io라이브러리를 이용하여 가공한 뒤 업로드를 해야합니다.
        img0 = Image.fromarray(im0, mode='RGB')
        out_img = io.BytesIO()
        img0.save(out_img, format='png')
        out_img.seek(0)
    
    s3_resource.s3tos3_put_object()
     - 서로 다른 S3계정간의 데이터를 local에 따로 다운로드 한 뒤 업로드 하는 것이 아닌 메모리상으로 불러 업로드하는 함수
    
    s3_resource.read_file()
     - S3에 있는 파일을 메모리로 읽기 위한 함수
    
    s3_resource.read_image()
     - S3에 있는 이미지 파일을 메모리로 읽는 함수
     - 이후 사용되는 이미지 형식에 따라 옵션에 "cv2", "PIL"을 선택하여 사용 가능
    
```

```python

```
