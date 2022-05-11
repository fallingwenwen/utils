from unittest import main
import pandas as pd;

if __name__ == '__main__':
    #任意的多组列表
    a = [1,2,3]
    b = [4,5,6]    

    #字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'a_name':a,'b_name':b})

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("./RESULT.csv",index=False,sep=',')