from dataclasses import dataclass


@dataclass
class Version:
    x: int
    y: int
    z: int

    @classmethod
    def parse_str(clscls, content: str) -> 'Version':
        start = 0  # start相当于遍历字符串的索引指针
        v = []  # 保存版本号的所有数字
        for i in range(len(content)):
            if content[i] == '.':
                v.append(int(content[start:i]))  # 用切片来获取当前版本号数字
                start = i +1  # 指定下一个遍历起始位置

        # 最后一个数字版本号无法通过'.'获取
        v.append(int(content[start:]))
        assert len(v)==3  # python断言，用于判断一个表达式，在表达式条件为false时触发异常
        return Version(v[0], v[1], v[2])  # 直接返回Version对象

    # 返回完整版本号
    def get_full(self, split=".") -> str:
        return f"v{self.x}{split}{self.y}{split}{self.z}"