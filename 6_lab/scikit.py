import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from math import sqrt

from sklearn.metrics import mean_squared_error

data = pd.read_csv("train.csv")
print(data)

plt.scatter(data["GrLivArea"], data["SalePrice"])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)
plt.show()

model = LinearRegression()
x = pd.DataFrame(data["GrLivArea"])
y = pd.DataFrame(data["SalePrice"])

print(model.fit(x,y))
print(model.coef_)
print(model.intercept_)

plt.scatter(data["GrLivArea"], data["SalePrice"])
plt.plot(x, model.predict(x), color="red")
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)
plt.show()

rmse = sqrt(mean_squared_error(x, model.predict(x)))
print("Среднеквадратичное отклонение: ", rmse)
