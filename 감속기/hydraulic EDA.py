### CSV 파일 read 및 데이터 scaling

```
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # visualization library
import matplotlib.pyplot as plt # visualization library
import chart_studio.plotly as py # visualization library
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import os
import warnings
from glob import glob
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
```

``` 
origin_path = os.getcwd()
data_path = os.path.join(origin_path, 'csv')
csv_30 = glob(os.path.join(data_path, '*_30_*.csv'))
csv_50 = glob(os.path.join(data_path, '*_30_*.csv'))
csv_70 = glob(os.path.join(data_path, '*_70_*.csv'))
features = ['Time[s]','RPM','TOQ','OTS','TE1','P_','P_.1','P_UD','E.RPM','E.Vlt','E.Iq',
            'E.Tmp','E.Pwr','E.Tar','P_.2','P_.3','S_UD/B','S_OD/C','S_26/B','S_35R/C',
            'S_LP','E.Id','S_SS-A','SCU.S1','SCU.FB','SCU.Set','SCU.S1.1','EOP.AEOP.Targe']

for i in range(1, 19):
    globals()['csv_30_%d'%i] = pd.read_csv(csv_30[i-1], usecols = features)
    globals()['csv_50_%d'%i] = pd.read_csv(csv_50[i-1], usecols = features)
    globals()['csv_70_%d'%i] = pd.read_csv(csv_70[i-1], usecols = features)
    globals()['under4bar_30_%d'%i] = globals()['csv_30_%d'%i].iloc[1000 : 2001]
    globals()['under4bar_50_%d'%i] = globals()['csv_50_%d'%i].iloc[1000 : 2001]
    globals()['under4bar_70_%d'%i] = globals()['csv_70_%d'%i].iloc[1000 : 2001]
    globals()['scale_30_%d'%i] = StandardScaler().fit_transform(globals()['csv_30_%d'%i])
    globals()['scale_50_%d'%i] = StandardScaler().fit_transform(globals()['csv_50_%d'%i])
    globals()['scale_70_%d'%i] = StandardScaler().fit_transform(globals()['csv_70_%d'%i])
    globals()['scale_4bar_30_%d'%i] = StandardScaler().fit_transform(globals()['under4bar_30_%d'%i])
    globals()['scale_4bar_50_%d'%i] = StandardScaler().fit_transform(globals()['under4bar_50_%d'%i])
    globals()['scale_4bar_70_%d'%i] = StandardScaler().fit_transform(globals()['under4bar_70_%d'%i])
    globals()['scale_30_%d'%i] = pd.DataFrame(globals()['scale_30_%d'%i], columns= features)
    globals()['scale_50_%d'%i] = pd.DataFrame(globals()['scale_50_%d'%i], columns= features)
    globals()['scale_70_%d'%i] = pd.DataFrame(globals()['scale_70_%d'%i], columns= features)
    globals()['scale_4bar_30_%d'%i] = pd.DataFrame(globals()['scale_4bar_30_%d'%i], columns= features)
    globals()['scale_4bar_50_%d'%i] = pd.DataFrame(globals()['scale_4bar_50_%d'%i], columns= features)
    globals()['scale_4bar_70_%d'%i] = pd.DataFrame(globals()['scale_4bar_70_%d'%i], columns= features)
a = csv_30_2.columns[:]
```
```
plt.figure(figsize=(12,5))
for i in range(18) :
    csv_num = 'csv_30_%i'%(i+1)
    plt.plot(globals()['csv_30_%d'%(i+1)]['Time[s]'], globals()['csv_30_%d'%(i+1)]['P_UD'])
plt.xlabel('sec')
plt.ylabel('P_UD')
```

### 4bar 이하 클러치 출력 유압
```
plt.figure(figsize=(12,12))
for i in range(18) :
    csv_num = 'csv_30_%i'%(i+1)
    plt.plot(globals()['under4bar_30_%d'%(i+1)]['Time[s]'], globals()['under4bar_30_%d'%(i+1)]['P_UD'], label = 'condition %d'%(i+1))
    plt.legend()
```

# 설명력 분석
import statsmodels.api as sm
import itertools

result = list(itertools.combinations((['x1', 'x2', 'x3', 'x4', 'x5', 'x6']), 2))
print(result[0])

def hydraulic_OLS(df) :
    
    x1 = df['TE1']
    x2 = df['E.RPM']
    x3 = df['E.Vlt']
    x4 = df['E.Iq']
    x5 = df['E.Tmp']
    x6 = df['E.Pwr']
    y = df['P_UD']
    c = []
    d = []

    for i in range(0,5) :

        if i == 0 :
            result = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
            a = []
            b = []
            for i in range(len(result)) :
                res = sm.OLS.from_formula("y ~" + "%s"%result[i] , data = df).fit()
                
                a.append(result[i])
                b.append(res.rsquared)
        else :
            result = list(itertools.combinations((['x1', 'x2', 'x3', 'x4', 'x5', 'x6']), i+1))

            for i in range(len(result)) :
                e = []
                f = []
                res = sm.OLS.from_formula("y ~" + "+".join(result[i]) , data = df).fit()
                c.append(result[i])
                d.append(res.rsquared)
                
        
            
        g = a + c
        h = b + d
        result_df = pd.DataFrame(data = [g, h]).transpose()
        result_df.columns = ['Variable', 'R_squared']
    return result_df
  
final = pd.DataFrame(columns= ['Variable', 'R_squared'])


for i in range(1,19) : 
    df_30 = globals()['under4bar_30_%d'%i]
    df_50 = globals()['under4bar_50_%d'%i]
    df_70 = globals()['under4bar_70_%d'%i]
    result_30 = hydraulic_OLS(df_30)
    result_50 = hydraulic_OLS(df_50)
    result_70 = hydraulic_OLS(df_70)
    result_total = pd.concat([result_30, result_50, result_70])
    final = pd.concat([final, result_total])

pd.set_option('display.max_rows', 100)
print(final.groupby(['Variable'], as_index= False).mean())


### OLS 모델을 이용해서 독립변수를 통해 종속변수의 설명력을 구할 수 있다. 이때 18개씩 3세트 총 54개의 csv 파일을 모두 이용해야하므로 해당 코드는 이를 포함한다.

