import pandas as pd
import pylab
from scipy.stats import ttest_ind

df = pd.read_csv("marketing_AB.csv")
df.head()
print("Общее количество в группах: \n", df["test group"].value_counts())
print("Доли в группах: \n", df["test group"].value_counts(normalize=True))
print(
    "Количество пользователей в каждой из групп: \n",
    df.groupby("test group")["user id"].agg(["count", "nunique"]),
)
df.groupby("most ads hour")["user id"].count().plot()
pylab.show()  # график зависимости пользователей от времени
print(
    "Инфо с графика: \n",
    df.groupby("most ads hour")["user id"].agg(["count", "nunique"]),
)
# создаем 2 группы
group1 = df[df["test group"] == "ad"]
group2 = df[df["test group"] == "psa"]
df["total ads flag"] = (df["total ads"] > 0) * 1
df["most ads hour flag"] = (df["most ads hour"] > 0) * 1
print(
    ":\n",
    df.groupby(["test group"])[["total ads flag", "total ads"]].agg(
        {"total ads flag": ["count", "mean"], "total ads": ["mean", "median"]}
    ),
)
print(":\n", ttest_ind(a=group1["total ads"], b=group2["total ads"]))
print(":\n", ttest_ind(a=group1["most ads hour"], b=group2["most ads hour"]))
