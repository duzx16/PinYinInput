清华大学计算机系"人工智能导论"课拼音输入法大作业

## 运行方式

使用命令行运行bin文件夹下的pinyin  

```shell
cd bin
./pinyin ../data/input.txt ../data/output.txt
```

可执行文件是使用pyinstaller打包的，但是因为打包环境是Mac所以我并不能保证（实际上是肯定不会）程序能在Windows下正常运行。所以如果可执行文件运行不了可以用**python3**直接运行src文件夹下的main.py，其他参数与运行pinyin时一致，即，

```shell
cd src
python3 main.py ../data/input.txt ../data/output.txt
```

默认使用的是三元模型+区分多音字的不同读音

另外请保证所给的拼音对于多音字的处理是正确的，比如“银行”没有标成“yin xing”。
## 文件结构：
### src
存放有程序的所有代码，其中model.py是定义的类，main.py是具体执行的代码
### bin
只存放有程序运行的主程序pinyin
### data
存放有程序的输入文件input.txt和输出文件output.txt。以及程序运行时必要的数据文件pinyin.txt,bigrams.txt,trigrams.txt。请不要变更这三个文件的位置。
