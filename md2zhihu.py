# 用于md2zhihu函数的正则匹配
# 将latex公式转换为知乎的图片url形式
def latex2zhihu(matched):
    matched = matched.group()[1:-1]

    from urllib.parse import quote
    # 知乎公式解析的网站url编码
    url = quote(matched)
    res = '<img src="https://www.zhihu.com/equation?tex=' + url + '" alt="[公式]" eeimg="1" data-formula="' + matched + ' ">'
    return res


# md2zhihu
def md2zhihu(input_filename,output_filename):
    import re

    f = open(input_filename,'rb')
    all_lines = f.read().decode()

    output = open(output_filename,'w',encoding='utf-8')

    # latex公式为$...$之间的内容
    # 关键在于 [^\$]*
    # 之间的内容为非$字符 避免匹配到下一个公式
    pattern = r'\$[^\$]*\$'
    res = re.sub(pattern,latex2zhihu,all_lines)

    output.write(res)
    f.close()
    output.close()


# 用于zhihu2md函数的正则匹配
# 将url形式的公式转换为latex
def zhihu2latex(matched):
    matched = matched.group()[43:-1]
    matched = matched.split('+')
    temp = []
    for i in matched:
        temp.append(i+' ')
    tex = ''.join(temp)

    from urllib.parse import unquote
    tex = '$' + unquote(tex) + '$'
    return tex

def zhihu2md(input_filename,output_filename):
    import re

    f = open(input_filename,'rb')
    all_lines = f.read().decode()

    output = open(output_filename,'w',encoding='utf-8')

    # 所有括号都需要加转义
    # 匹配tex=后面的字符
    # 关键在于 [^公式\(\)]*
    # 由除了 '(' ')' '公' '式' 这四个字符的全部字符构成 避免匹配到下一个公式
    pattern = r'!\[\[公式\]\]\(https://www.zhihu.com/equation\?tex=[^公式\(\)]*\)'
    res = re.sub(pattern,zhihu2latex,all_lines)

    output.write(res)
    f.close()
    output.close()

    # 删除过多的换行符
    # 这里多余的换行符是由于在知乎上面编辑的时候使用enter 而不是shift+enter造成的
    # 我感觉知乎还会额外添加一个换行符 正常shift+enter应该是两个 这里边是三个
    # 这就导致输出的公式块 每行之间都有换行符 需要手动删除
    #--------------------------------------------------------------------------------------------------->
    # 有时间实现以下 代码块的多余换行符 删掉
    #--------------------------------------------------------------------------------------------------->
    f = open(output_filename,'r',encoding='utf-8')
    text = f.readlines()

    # 每三个换行符保留一个
    temp = []
    for i in range(len(text)):
        if text[i] != '\n':
            temp.append(text[i])
        else:
            if text[i+1] != '\n':
                temp.append(text[i])

    refine_text = ''.join(temp)

    f.close()
    # 'w+'模式 每次读写都会清空之前的全部内容
    output = open(output_filename,'w+',encoding='utf-8')
    output.write(refine_text)
    output.close()



if __name__ == '__main__':

    # md2zhihu('D:\\zmr\\study\\ctf\\notes\\test.md','D:\\zmr\\study\\ctf\\notes\\output_zhihu\\output.md')

    # zhihu2md('D:\\zmr\\study\\ctf\\notes\\test.md','D:\\zmr\\study\\ctf\\notes\\output_zhihu\\output.md')



# 以下是我debug过程中最折磨的一部分
# 最开始成功完成了正则匹配 写入文件后上传知乎 结果知乎居然识别不了
# 我很不理解 将写入的文件与能被知乎识别的文件（f12查看获得）一起丢到010editor中查看
# 发现 ‘公式’ 这个字符 两者的二进制居然不一样
# 开始尝试不同解码 如下
# 原来系统默认的write是gbk格式 然而知乎需要utf-8
# 给open() 函数添加一个 encoding='utf-8' 变量即可

# print('公式'.encode('gbk'))
# x = 'b9abcabd' #gbk
# print('公式'.encode('utf-8'))
# y = 'e585ace5bc8f' #utf-8
# for i in range(0,8,2):
#     print(bin(int(x[i:i+2],16)))
# for i in range(0,12,2):
#     print(bin(int(y[i:i+2],16)))