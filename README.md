### 项目简介
本项目用于协助开展对venusblood的翻译工作。  
理论上支持基于unity开发的B以外的venusblood。  
使用者通过简单的配置即可开展对venusblood的剧情文本翻译工作而无需对软件开发知识有所了解。  
我的梦想，就是让每人一个翻译，都能做自己的赵云。（其实只是希望有赵云让我玩上中文的VBV~）  
4070+deepseek:r1机翻序章花了一个多点还翻的像狗屎:D，感觉我和AI之间有了一层可悲的厚壁障了（指买不起4卡A100集群，甚至买不起token）  

### 安装说明
本项目基于python3开发，仅在3.10上完整运行过，但理论上不强求python版本。  
安装python3后，clone或下载项目到本地，在代码根目录通过pip安装必要的依赖：  
`pip install -r requirements.txt`  
之后直接运行：  
`python 1_export_file_to_origin.py`  

### 使用说明
#### 1_export_file_to_origin.py
用于从游戏资源文件中解析原始脚本json。将venuablood游戏根目录`\Standalone\scenario`文件夹中的文件复制到项目根目录同名文件夹中，之后运行脚本即可。解析出的原始json会被输出到`export_origin`文件夹中。  
#### 2_origin_to_keyjson.py
用于从原始json中提取需要翻译的内容，简化json提高可读性。从`export_origin`中读取并输出到`keyjson`文件夹中。  
#### 3_ai_translate.py
读取`keyjson`文件夹中的json，调用大模型翻译其中内容，将结果输出到`translated`文件夹中。其中，调用大模型进行翻译的具体实现应在`translator.py`中实现，可以通过实现不同的translate函数来调用翻译器或完全手工翻译。  
样例的`translator.py`展示了通过调用本地部署的deepseek:r1进行翻译的简单过程（如何部署和调优大模型不属于本项目的内容）。  
样例的`translator_manual.py`展示了简单的手工翻译方法，可通过重命名简单尝试。名为`translator`的文件生效。  
注意：手动翻译目前并不完善，仅供实验。整个文件完全翻完才会输出结果文件，中途退出会丢失所有翻译！！！  
翻译过程中的人名和章节名，为了保持翻译的一致性，在任意新出现的名字完成翻译后，会缓存在`static`下的对应json中。之后再遇到同名的文本会直接替换无需翻译。后续考虑对专有名词做同样的处理。  
在开始翻译前手工完善专有名词字典也是比较推荐的做法。以人名为例，格式如下(遵循标准json格式，后期可能支持yaml提高易读性)：  
`{"日文名1":"译名1","日文名2":"译名2","日文名3":"译名3"}`  
#### 4_generate_output.py
读取`translated`文件夹中的文件和`scenario`中的游戏原始文件，重新封包新的游戏资源文件输出到`output`中  

### 汉化游戏
！！！备份游戏`\Standalone\scenario`中的原始文件  
将`output`中的文件替换到游戏`\Standalone\scenario`中进行替换。  
将`xunity_package`中的所有文件拷贝到游戏根目录（xunity用于补全游戏中的字体，不开启翻译功能）。  
运行游戏即可  

### 依赖项目
[UnityPy](https://github.com/K0lb3/UnityPy)用于解封包unity资源文件  
[XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator)用于向游戏中注入中文字体。  
PS:VBL姥爷汉化版时永远的痛，花了两个星期才干进去的字体，还有各种奇怪的显示bug，还因为修改了游戏文件导致要绑定游戏版本。如今直接通用外挂就可以了（大人时代变了.jpg）。  

### 注意事项
1.祝所有看不看说明的朋友好运  
2.请一定记得把补丁解压缩到游戏目录里
