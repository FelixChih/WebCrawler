import requests
from bs4 import BeautifulSoup
import os
import json
from urllib import request

path = "D:/Python/爬蟲/FoodTank" # 自定義路徑 and 路徑名稱
if not os.path.exists(path): # 如果路徑不存在
    os.mkdir(path) # 創建路徑

page = 1 # 頁數

for time in range(20): # 爬取20頁
    url = "https://food.tank.tw/default.asp?cateID=5&page={0}".format(page) # 格式化帶入頁數
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Connection": "keep-alive"}
    res = requests.get(url, headers=headers)
    res.encoding = "UTF-8"
    soup = BeautifulSoup(res.text, "html.parser")
    titles = soup.select("div.entry-image-wrapper div.entry-thumbnail a.icon-effect")

    for t in titles:
        food_url = "https://food.tank.tw/" + t["href"] # 取得每道菜個別的 href
        food_res = requests.get(food_url, headers=headers) # 再次 requests 進入個別分頁爬取資料
        food_res.encoding = "UTF-8"
        food_soup = BeautifulSoup(food_res.text, "html.parser")
        RecipeName = food_soup.select(("div.entry-content-container.clearfix h2"))[0].text
        ingredients = food_soup.select("span.ingredient-name")
        img_url = food_soup.select("img.img-responsive")[0]["src"]
        request.urlretrieve(img_url, path + "/" + str(RecipeName) + ".jpg") # 下載圖片 urlretrieve(圖片網址, 存放路徑 + .jpg）

        Ingredients = [] # 建立一個空list，接收下面迴圈取得的食材資訊

        for i in ingredients:
            tmp_i = i.text

            if "\u3000\u3000" in tmp_i: # 以兩個空格為條件，將回傳的字串分割為list（有些有兩個）
                tmp_i = tmp_i.split("\u3000\u3000")
            else:                       # 有些只有一個空格
                tmp_i = tmp_i.split("\u3000")

            try:
                Ingredients.append(tmp_i[0]) # 分割後的list index 0 為 食材名稱
                Ingredients.append(tmp_i[1]) # 分割後的list index 1 為 食材數量
            except IndexError:
                pass

        RecipeDetails = "" # 建立一個空字串，接收下面迴圈取得的料理方法
        recipeDetails = food_soup.select("span.recipeInstructions")
        for r in recipeDetails:
            RecipeDetails += r.text+"\n" # 一句一句傳回上面的空字串中

        # 建立一個字典，統整收集到的資料
        collection = {'RecipeName':RecipeName,
                      'Url':food_url,
                      'Ingredients':Ingredients,
                      'RecipeDetail':RecipeDetails}

        with open(path + "/" + str(RecipeName) + ".json", "w") as j:
            json.dump(collection, j)

    page += 1 # 下一頁


