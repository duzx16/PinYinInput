# -*- coding:utf-8 -*-
import os, sys
from model import *

assert(len(sys.argv) == 4 or len(sys.argv) == 3)

# 载入拼音文件
pinyin_dict = {}
with open("../data/pinyin.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split()
        pinyin_dict[line[0]] = line[1:]
        
pinyin_dict["lve"] = pinyin_dict["lue"]
pinyin_dict["nve"] = pinyin_dict["nue"]
pinyin_dict["n"] = pinyin_dict["en"]

# 载入ngram count的数据
if len(sys.argv) == 4:
    assert(sys.argv[1] == "-n2")
    gram_file = "../data/bigrams.txt"
    input_path = sys.argv[2]
    output_path = sys.argv[3]
else:
    gram_file = "../data/trigrams.txt"
    input_path = sys.argv[1]
    output_path = sys.argv[2]

ngram_dict = {}
with open(gram_file, encoding="utf-8") as file:
    for line in file:
        line = line.strip().split()
        ngram_dict[line[0]] = int(line[1])

print("ngram file loaded")


# 生成转换模型
if sys.argv[1] == "n2":
    ngrams = FixedLinearNGram(ngram_dict, 564481535, [0.99])
    converter = PinyinConverter(ngrams, pinyin_dict, gram_num=2)
else:
    ngrams = LinearSmoothNGram(ngram_dict, 564481535, alpha=100, char_length=2)
    converter = PinyinConverter(ngrams, pinyin_dict, gram_num=3, begin_gram="b0", end_gram="d0", char_length=2)


inputs = []
with open(input_path, encoding="utf-8") as file:
    for line in file:
        inputs.append(line.strip())

print("输入加载完毕，开始转换")

# 进行转换
output_results = []
for p in inputs:
	output_results.append(converter.convert(p))

print("转换完成")

with open(output_path, "w", encoding="utf-8") as output:
	for sentence in output_results:
		output.write(sentence + "\n")

