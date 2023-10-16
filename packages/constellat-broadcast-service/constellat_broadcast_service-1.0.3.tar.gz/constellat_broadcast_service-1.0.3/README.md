# broadcast-service

broadcast-service is a lightweight python broadcast library. You can easily construct a broadcast pattern through this library.

## Reference
[Python最佳实践-构建自己的第三方库](https://blog.csdn.net/linZinan_/article/details/127944610)

## Setup

```sh
pip install constellat-broadcast-service
```


## Usage

There is a easy demo to show how to use broadcast-service.

```python
from broadcast_service import broadcast_service

def handle_msg(params):
    print(params)

if __name__ == '__main__':
    info = 'This is very important msg'

    # listen topic
    broadcast_service.listen('Test', handle_msg)

    # publish broadcast
    broadcast_service.broadcast('Test', info)

```


## Upload

```shell
# 打包项目
python setup.py sdist
# 上传包
twine upload dist/*
twine upload dist/constellat_broadcast_service.tar.gz
```
