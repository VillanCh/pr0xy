# pr0xy
教学用多线程扫描框架（代理扫描）

* 支持插件拓展
* 多线程
* 架构简单

## 使用方法

	usage: pr0xy.py [-h] [--ports PORTS] [--type TYPE] IP
	
	Pr0xy Scan and collect proxy info
	
	positional arguments:
	  IP             The IP you want to check: INPUT format:\ 1.2.3.4-1.2.5.6 or
	                 45.67.89.0/24 or 45.78.1.48
	
	optional arguments:
	  -h, --help     show this help message and exit
	  --ports PORTS  The ports you want to check, Plz input single port or with a
	                 format like: 82,80 or 100-105
	  --type TYPE    Type of scan [Now Just Support proxy]

* IP 就表示 IP地址，你可以输入单个或者多个（必须是点分十进制），当然形式限制三种：
	* 1.单个 IP 地址
	* 2.短横线连接符表示的 IP 范围（例如 1.2.3.4-1.2.3.9 这表示 6 个 IP）
	* 3.带有掩码的网络范围（例如1.2.3.0/24）
* PORTS 端口：想要扫描的端口 支持格式：单个端口(80)，逗号分隔（80,82,83），短横线表范围（80-85）
* TYPE 类型：这里的类型还是有必要解释的，万一以后需要添加其他的功能，就可以直接改动一张表添加新的模块，然后通过指定类型调用。

## 结果说明
如果成功扫描到代理，会在当前目录生成一个 success.txt 的文件，并且在当前 console 中提示，如果没能扫描到，则会出现一个 failed.txt 记录失败的地址。