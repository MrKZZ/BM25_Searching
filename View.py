from flask import Flask, render_template, request
import BM25
import os

app = Flask(__name__)


@app.route('/')  # 装饰器把一个函数绑定到对应的 URL 上
def hello_world():
    return render_template('search.html', error=True)  # search.html 可以做得美观

# 读取表单数据，获得doc_ID
@app.route('/search/', methods=['POST'])  # get，post方法是由浏览器提交给下一进程的方法
def search():
    global bm25, w_qd, page, docs, query
    try:
        checked = ['checked="true"', '', '']
        query = request.form['key_word']
        if query is not '':
            bm25, w_qd = BM25.Level_search(dic, dic_level, query)
            page, docs = Page_Docs(w_qd, flag=False)
            docs_ = docs[:10]
            page_ = page[:10]
            return render_template('search.html', checked=checked, key=query, docs=docs_, page=page_,
                                   error=True)
        else:
            return render_template('search.html', error=False)
    except:
        print('search error')

# 根据回传id查找文件
@app.route('/search/<id>/', methods=['GET'])
def content(id):
    try:
        result = {}
        for doc in docs:
            if doc['id'] == id:
                result = doc
                break
        return render_template('content.html', doc=result)
    except:
        print('content error')

@app.route('/search/page/<key>/', methods=['GET', 'POST'])  # 在这里的key是由页面返回的参数
def page_view(key=0):
    checked = ['checked="true"', '', '']
    key = int(key)
    docs_ = find(doc_id[key * 10: 10 * key + 10])
    page_ = page[key: key+10]
    return render_template('search.html', checked=checked, key=query, docs=docs_, page=page_,
                           error=True)

def Page_Docs(w_qd, key=0, flag=True):  # key表示返回页面数
    # 返回docid列表
    global doc_id
    doc_id = ["0" + i for i, s in w_qd]
    page = []
    for i in range((len(doc_id) // 10)):
        page.append(i + 1)
    if flag:
        docs = find(doc_id[key * 10: 10 * key + 10])
    else:
        docs = find(doc_id)
    return page, docs

# 将需要的数据以字典形式打包传递给search函数
def find(docids):
    docs = []
    dir_path = os.getcwd().replace("Kzz_Search", "clinicaltrials_txt")
    for id in docids:
        path = dir_path + "\\" + id[0:3] + "\\" + id[0:5] + "\\NCT" + id + ".txt"
        with open(path, "r") as fr:
            file = fr.readlines()
            fr.close()
        title = file[1]
        content = "\n\r".join(file)
        extra = ["NCT" + e for e in docids[:3]]
        doc = {'title': title, 'datetime': '2017', 'shortshot': content[:200] + "...", 'id': id,
               'url': id[0:3] + "\\" + id[0:5] + "\\NCT" + id + ".txt", 'content': content, "extra": extra}
        docs.append(doc)
    return docs

if __name__ == '__main__':
    dic, dic_level = BM25.LoadInvertable()
    bm25 = {}
    w_qd = {}
    page = []
    docs = []
    query = ''
    doc_id = []
    app.run(debug=False)
