## Web Scrapping Code for totalwine.com
import bs4
import pandas as pd
import requests

def main():

    pd.set_option('display.max_colwidth', 1000)

    baseUrl = 'https://www.totalwine.com/wine/c/c0020?tab=fullcatalog&viewall=true&text=&pagesize=180&page='
    maxPage=130

    data = pd.DataFrame(columns=['Title', 'Price', 'StarRating', 'numRater', 'Shopping_Link', 'Img_src'])

    #Page 1
    result = requests.get('https://www.totalwine.com/wine/c/c0020?tab=fullcatalog&viewall=true&text=&pagesize=180')
    c = result.content
    soup = bs4.BeautifulSoup(c, 'html.parser')
    # Find all the products in current page
    productList = soup.find_all('div', class_='plp-product-content-wrapper')
    for j in range(0, len(productList)):
        # Get Title and Link
        prod = productList[j].find('a', class_='analyticsProductName')
        prodName = prod.text.strip()
        data = data.append({'Title': prodName}, ignore_index=True)
        prodLink = prod['href']
        data.ix[j, 'Shopping_Link'] = str(prodLink)

        # Get Price
        prodPrice = productList[j].find('span', class_='price')
        data.ix[j, 'Price'] = prodPrice.text.strip()

        # Get Star Rating
        prodStar = productList[j].find('span', class_='stars')
        if prodStar.span.has_attr('style'):
            starRating = prodStar.span['style']
            data.ix[j, 'StarRating'] = str(starRating)

        # Get Rater Number
        prodRater = productList[j].find('a', class_='analyticsProductReviews')
        if prodRater:
            numRater = prodRater.span.string
            data.ix[j, 'numRater'] = numRater

        # Get Image Scr
        prodImg = productList[j].find('div',class_='plp-list-product-img')
        if prodImg:
            if(prodImg.a.img.has_attr('data-lazy-src')):
                src = prodImg.a.img['data-lazy-src']
            else:
                src = prodImg.a.img['src']
            data.ix[j, 'Img_src'] = str(src)

    #Page 2 ~ 130
    for i in range(2, maxPage+1):
        url=baseUrl+str(i)
        result = requests.get(url)
        c = result.content
        soup=bs4.BeautifulSoup(c, 'html.parser')
        # Find all the products in current page
        productList = soup.find_all('div',class_='plp-product-content-wrapper')
        for j in range(0, len(productList)):
            # Get Title and Link
            indexNum = (i - 1) * 180 + j
            prod = productList[j].find('a', class_='analyticsProductName')
            prodName=prod.text.strip()
            data = data.append({'Title': prodName}, ignore_index=True)
            prodLink=prod['href']
            data.ix[indexNum, 'Shopping_Link'] = str(prodLink)

            #Get Price
            prodPrice = productList[j].find('span', class_='price')
            data.ix[indexNum, 'Price'] = prodPrice.text.strip()

            # Get Star Rating
            prodStar = productList[j].find('span', class_='stars')
            if prodStar.span.has_attr('style'):
                starRating = prodStar.span['style']
                data.ix[indexNum, 'StarRating'] = str(starRating)

            # Get Rater Number
            prodRater = productList[j].find('a', class_='analyticsProductReviews')
            if prodRater:
                numRater = prodRater.span.string
                data.ix[indexNum, 'numRater'] = numRater

            # Get Image Scr
            prodImg = productList[j].find('div', class_='plp-list-product-img')
            if prodImg:
                if (prodImg.a.img.has_attr('data-lazy-src')):
                    src = prodImg.a.img['data-lazy-src']
                else:
                    src = prodImg.a.img['src']
                data.ix[indexNum, 'Img_src'] = str(src)
                

    #Write data to csv file
    data.to_csv("TotalWine.csv")


if __name__ == '__main__':
    main()
