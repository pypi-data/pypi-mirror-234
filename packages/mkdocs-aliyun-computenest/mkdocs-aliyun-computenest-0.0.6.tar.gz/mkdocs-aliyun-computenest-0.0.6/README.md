# QuickStart Demo 计算巢样式主题仓库

查看服务实例部署在线文档，请访问 [服务实例部署文档](https://aliyun-computenest.github.io/quickstart-demo)

本文档通过 [MkDocs](https://github.com/mkdocs/mkdocs) 生成，请参考[使用文档](https://www.mkdocs.org/getting-started/#installation) 

1）安装和使用：

```shell
$ pip install mkdocs # or pip3 install mkdocs
$ mkdocs serve # in root folder
```
2）本地预览：本地在浏览器打开 [http://localhost:8000/](http://localhost:8000/) 。

3) 打包发布主题

```shell
$ python setup.py check # 检查配置
$ python setup.py sdist build # build
$ pip3 install twine # 安装twine
$ twine upload dist/* # 发布
```