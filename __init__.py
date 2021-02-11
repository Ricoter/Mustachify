import inspect
import os
import shutil

shutil.copy("./dlib-19.21.99-cp37-cp37m-linux_x86_64.whl", "/tmp")
os.chmod("/tmp/dlib-19.21.99-cp37-cp37m-linux_x86_64.whl", 0o666)
print(os.listdir("/tmp"))
