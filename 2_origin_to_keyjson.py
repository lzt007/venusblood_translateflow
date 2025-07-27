import os
import json
import traceback

export_dir = "./export_origin"
keyjson_dir = "./keyjson"

for root, dirs, files in os.walk(export_dir):
    for file in files:
        try:
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                origin_data = json.load(f)
            cuts = origin_data["cuts"]
            result = []
            # print(cuts)
            for cut in cuts:
                key_data = {
                    "subTitle": cut.get("subTitle"),
                    "window": cut.get("window")

                }
                if key_data["window"] is not None:
                    key_data["window"] = {
                        "texts": key_data["window"]["texts"],
                        "name": key_data["window"]["name"],
                        "tag": key_data["window"]["tag"]
                    }
                # print(json.dumps(key_data, ensure_ascii=False, indent=2))
                result.append(key_data)
            with open(os.path.join(keyjson_dir, file), "w", encoding="utf-8") as f:
                f.write(json.dumps(result,ensure_ascii=False,indent=2))
        except BaseException as e:
            print(f"解析{file}时发生错误：{e}\n{traceback.format_exc()}")
