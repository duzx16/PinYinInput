# -*- coding:utf-8 -*-
class AddSmoothNGram:
    def __init__(self, ngram_dict):
        self.ngrams = ngram_dict
 
    def __getitem__(self, ngram):
        if ngram in self.ngrams and ngram[:-1] in self.ngrams:
            return (self.ngrams[ngram]+1) / (self.ngrams[ngram[:-1]])
        else:
            return 0

class LinearSmoothNGram:
    def __init__(self, ngram_dict, length, alpha = 10, char_length = 1):
        self.ngrams = ngram_dict
        self.length = length
        self.alpha = alpha
        self.char_length = char_length

    def __getitem__(self, ngram):
        lamb, prob, sums = 0, 0, 0
        for i in range(len(ngram) // self.char_length - 1):
            count = self.ngrams.get(ngram[self.char_length * i:-1 * self.char_length], 0)
            lamb = (1 - sums) * count / (count + self.alpha)
            if lamb != 0:
                prob += lamb * self.ngrams.get(ngram[self.char_length * i:], 0) / count
            sums += lamb
        prob += (1-sums) * self.ngrams.get(ngram[-1 * self.char_length], 0) / self.length
        return prob
    
class FixedLinearNGram:
    def __init__(self, ngram_dict, length, alpha = [1]):
        self.ngrams = ngram_dict
        self.length = length
        self.alpha = alpha

    def __getitem__(self, ngram):
        lamb, prob, sums = 0, 0, 0
        for i in range(len(ngram)-1):
            count = self.ngrams.get(ngram[i:-1], 0)
            lamb = self.alpha[i]
            if lamb != 0 and count != 0:
                prob += lamb * self.ngrams.get(ngram[i:], 0) / count
            sums += lamb
        prob += (1-sums) * self.ngrams.get(ngram[-1], 0) / self.length
        return prob

class PinyinConverter:

    def __init__(self, ngram_model, pinyin_dict, gram_num = 2, begin_gram = "b", end_gram = "e", char_length = 1):
        self.gram_num = gram_num
        self.ngram = ngram_model
        self.begin = begin_gram
        self.end = end_gram
        self.pinyin = pinyin_dict
        self.pinyin["d"] = [end_gram]
        self.pinyin[begin_gram] = begin_gram
        self.char_length = char_length
        
    def convert(self, py_str, begin_padding=True, end_padding=True):
        padding_size = self.gram_num - 1
        py_list = py_str.split() + ["d"]
        form_nodes, next_nodes = {}, {}
        form_nodes[self.begin * padding_size] = (1, self.begin * padding_size)
        for i in range(len(py_list)):
            current_nodes = self.pinyin[py_list[i]]
            for current_node in current_nodes:
                for form_node, (form_prob, form_str) in form_nodes.items():
                    next_node = form_node[self.char_length:] + current_node
                    prob = self.ngram[form_node + current_node] * form_prob
                    if prob > next_nodes.get(next_node, [-1])[0]:
                        next_nodes[next_node] = (prob, form_str + current_node)
            form_nodes, next_nodes = next_nodes, {}
        result = max(form_nodes.values())[1][padding_size * self.char_length:-1]
        result_str = ""
        for i in range(len(result) // self.char_length):
            result_str += result[i * self.char_length]
        return result_str