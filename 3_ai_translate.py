import os
import json
import traceback
from translator import translate
# from translator_manual import translate

keyjson_dir = "./keyjson"
translated_dir = "./translated"
roles_path = "./static/roles.json"
subTitles_path = "./static/subTitles.json"

with open(roles_path, "r", encoding="utf-8") as f:
    roles: dict = json.load(f)

with open(subTitles_path, "r", encoding="utf-8") as f:
    subTitles: dict = json.load(f)

for root, dirs, files in os.walk(keyjson_dir):
    for file in files:
        try:
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                data_list = json.load(f)
            total = len(data_list)
            for i in range(0, len(data_list)):
                print(f"{i}/{total}")
                if data_list[i]["subTitle"] in subTitles:
                    subtitle = subTitles[data_list[i]["subTitle"]]
                else:
                    subtitle = translate(data_list[i]["subTitle"])
                    subTitles[data_list[i]["subTitle"]] = subtitle
                    with open(subTitles_path, "w", encoding="utf-8") as f:
                        f.write(json.dumps(subTitles, ensure_ascii=False))
                data_list[i]["subTitle"] = subtitle
                if data_list[i]["window"] is None:
                    continue
                if data_list[i]["window"]["tag"] != "" and data_list[i]["window"]["name"] == "":
                    # 实际游戏中应当存在某个数据表根据tag查名字，tag不是用于显示的值，不要修改tag！！！
                    # name在不为空时会覆盖显示名字，原本用于给初次登场的角色显示？？？用，这里利用这个键值覆写中文名
                    if data_list[i]["window"]["tag"] in roles:
                        name = roles[data_list[i]["window"]["tag"]]
                    else:
                        name = translate(data_list[i]["window"]["tag"])
                        roles[data_list[i]["window"]["tag"]] = name
                        with open(roles_path, "w", encoding="utf-8") as f:
                            f.write(json.dumps(roles, ensure_ascii=False))
                    data_list[i]["window"]["name"] = name

                for j in range(0, len(data_list[i]["window"]["texts"])):
                    j_str = data_list[i]["window"]["texts"][j]
                    # 先将对话中的人名都替换为中文并用《》标记在翻译时让ai跳过人名
                    for k, v in roles.items():
                        j_str = j_str.replace(k, f"《-{v}-》")
                    data_list[i]["window"]["texts"][j] = translate(data_list[i]["window"]["texts"][j])
                print(data_list[i])
            with open(os.path.join(translated_dir, file), "w", encoding="utf-8") as f:
                f.write(json.dumps(data_list, ensure_ascii=False, indent=2))


        except BaseException as e:
            print(f"解析{file}时发生错误：{e}\n{traceback.format_exc()}")
