
import pandas as pd
import matplotlib.pyplot as plt
wine = pd.read_csv('/Users/chizhang/95-888 Python for Data Analytics/WineDotCom.csv', index_col = 0)
wine = wine[wine["StarRating"]>0]

count = pd.DataFrame(wine.groupby('Country').agg(['count'])['Title']).reset_index()
avg_price = pd.DataFrame(wine.groupby('Country')['Price'].agg(['mean'])).reset_index()
avg_star = pd.DataFrame(wine.groupby('Country')['StarRating'].agg(['mean'])).reset_index()

count['avg_price'] = avg_price['mean']
count['avg_star'] = avg_star['mean']
count_revised =  count.loc[count['count'] >= 5].reset_index()

col = ['yellow','black','green','yellow','yellow','green',
       'green','green','green','green','blue','green','red','red','yellow','yellow',
       'yellow','yellow','black','yellow','yellow','green','red','blue','green',
       'yellow','yellow']

plt.title('Rating vs Price by Region')
plt.xlabel('Average Price')
plt.ylabel('Average Rating')
plt.scatter(x = count_revised['avg_price'], y = count_revised['avg_star'], s = count_revised['count'], c = col, alpha = 0.8)
