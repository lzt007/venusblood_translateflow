def translate(j_str, glossary: dict={},role=""):
    if j_str == "":
        return ""
    for k, v in glossary.items():
        j_str = j_str.replace(k, v)
    print(f"待翻译文本：{j_str}")
    c_str = input("输入译文：")
    return c_str
