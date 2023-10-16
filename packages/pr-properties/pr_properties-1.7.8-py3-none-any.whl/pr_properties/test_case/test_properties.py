from pr_properties import pr_properties


class Test:
    def test_01(self):
        p = pr_properties
        p.read(r"./pool.properties")
        # 新增
        p['2'] = 2
        p['3'] = 3
        # 写入新增的内容
        p.write()

    def test_02(self):
        text = """# comment
    kk=123
    ks.1=222
    ks.1=222==333"""
        p = pr_properties
        p.loads(text)
        print(p.get('kk'))
        print('dumps', p)
        # 修改删除
        p['kk'] = 3
        del p['ks.1']
        print('\n' + p.__str__())
