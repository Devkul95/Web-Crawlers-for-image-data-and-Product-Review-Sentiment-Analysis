import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)



@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/products', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")

            urls = []
            names = []
            # watches, shoes
            bigboxes = flipkart_html.find_all('div', {'class': 'IIdQZO _1SSAGr'})
            del (bigboxes[0:2])
            for b in bigboxes:
                href = b.find_all('a', {'class': '_2mylT6'})
                for a in href:
                    urls.append('https://www.flipkart.com' + a['href'])
                    names.append(a.text)
            # mobiles
            bigboxes = flipkart_html.find_all('div', {'class': '_3O0U0u'})
            for b in bigboxes:
                href = b.find_all('a', {'class': '_31qSD5'})
                for a in href:
                    urls.append('https://www.flipkart.com' + a['href'])
                name_ref = b.find_all('div', {'class': "_3wU53n"})
                for name in name_ref:
                    names.append(name.text)
            # books
            bigboxes = flipkart_html.find_all('div', {'class': '_3liAhj'})
            del (bigboxes[0:2])
            for b in bigboxes:
                href = b.find_all('a', {'class': '_2cLu-l'})
                for a in href:
                    urls.append('https://www.flipkart.com' + a['href'])
                    names.append(a.text)

            links_dict = {"name": names, "href": urls}
            return render_template('product.html', len=len(links_dict['name']), Links=links_dict)
        except Exception as e:
            print('The Exception message is: ', e)
            # return 'something is wrong'
    else:
        return render_template('index.html')

@app.route('/review/', methods=['POST'])  # route to show the review comments in a web UI
@cross_origin()
def review():
    # return 'the path is ' + mypath
    if request.method == 'POST':
        try:
            # print('Inside review page')
            # import pdb;pdb.set_trace()
            # print(mypath)
            productLinks = request.form['btn_url']
            prodRes = requests.get(productLinks)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            productName = prod_html.find_all('span',{'class': "_35KyD6"})[0].text
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            details = prod_html.find_all('li', {'class': '_2-riNZ'})
            highlights = []
            for i in details:
                highlights.append(i.text)
            reviews = []
            for commentbox in commentboxes:
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    # custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            return render_template('results.html', highlight=highlights[0:5], Product=productName, reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            print('The Exception message is :', e)
            return render_template('results.html')

    else:
        return render_template('results.html')


port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)
