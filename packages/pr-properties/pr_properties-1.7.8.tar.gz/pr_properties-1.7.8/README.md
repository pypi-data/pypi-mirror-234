安装
pip install pr-properties

这是一个读写properties工具

```python
from pr_properties import Properties

# 创建Properties对象
p = Properties()
# 读取字符
str_p = """# 读取字符=1
master.initialSize=4
master.minIdle=10=20=kk"""
p.loads(str_p)
# 修改
p['master.initialSize'] = 5
# 增加
p['master.cc'] = 5
# 输出对象的字符
print(p.dumps())
# 删除
del p['master.cc']
print(p.dumps())

# 读写properties文件
p = Properties()
p.read(path=r'./pool.properties')
print(p['master.initialSize'])  # 4
# 支持get
print(p.get('master.initialSize'))
# 修改
p['master.initialSize'] = 5
# 写入,写入后会关闭文件;写入功能请慎重使用
p.write()
p.read(path=r'./pool.properties')
# 验证是否修改
print(p['master.initialSize'])  # 5
```
