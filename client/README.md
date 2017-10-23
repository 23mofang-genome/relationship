## Usage:

### Step 1

Create a file named config_prod.py in pythonSdk/sdk directory

```python
#-*- encoding: utf-8 -*-
from .config import *
PUBLIC_KEY  = "ur public key"
PRIVATE_KEY = "ur private key"
```

### Step 2

fill in the `TestImageName` in `example_SubmitTaskAndGetResult.py` file
```python
# example
TestImageName="cn-bj2.ugchub.service.ucloud.cn/ur_bucket/ur_image:tag"
```

### Step 2
```bash
cd client
```

### Step 3
```bash
cat ../code/testdata/111-1173-9987.sfs ../code/testdata/separator.txt ../code/testdata/111-1175-1798.sfs ../code/testdata/separator.txt ../code/testdata/filenames.txt | python -u pythonSdk/example_SubmitTaskAndGetResult.py
```

## Some Explain

The cmd above has a `-u` flag, it's only for python2, to make sure stdin is binary then you can use:
```python
STDIN = sys.stdin.read()
```

In python3 you don't need `-u` flag, just use one line below:
```python
sys.stdin.buffer.read()
```
