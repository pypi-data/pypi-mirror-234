import pandas as pd
import numpy as np

## Función para convertir las variables continuas en integrales
def clean_continuous_var(df, column=None):
    '''
    Return a dataframe 
    '''
    df=df.copy()
    df_columns=df.columns.tolist()[1:-1] ## Todas las columnas con excepción de la Fila y el ubigeo
    df_columns = [x for x in df_columns if str(x) != 'nan']
    try:
        df[column]=(df[column].
                    apply(lambda x:"".join(filter(str.isnumeric, str(x)))).
                   astype(int))
        for cols in df_columns:
            try:
                df[cols]=df[cols].replace("-","0", regex=True).astype(int)
            except:
                df[cols]=(df[cols].
                          replace("-","0", regex=True).
                          replace(" ","", regex=True).
                          astype(int)
                         )
    except:
        raise AssertionError("La variable bajo análisis no es continua")
    return df_columns, df


def cal_intervalos(df, valor_inicio, intervalo, column="resp"):
    '''
    Return a DataFrame where each column is a class interval
    '''    
    df=df.copy()
    len_var=df[column].max() ##valor máximo
    list_in=(list(range(valor_inicio,len_var+1,intervalo))) # lista con los intervalos 

    df["resp2"]=""
    df["lim_s"]=0
    for p in list_in:
        df["lim_s"]=np.where((df[column]>=p)&(df[column]<=p+intervalo),p+intervalo-1,df.lim_s)
        df["resp2"]=np.where((df[column]>=p)&(df[column]<=p+intervalo),str(p)+"-"+str(p+intervalo-1),df.resp2)

    del df[column]
    df=(df.
        rename({"resp2":column},axis=1).
        groupby(["ubigeo","lim_s",column]).
        sum(numeric_only=True).  ## BUG The default value of numeric_only in DataFrameGroupBy.sum is deprecated.
        reset_index(["lim_s",column]).
        sort_values("lim_s").
        copy()
       )
    return df

def cal_descriptivos(df, values="fre", fila="resp"):
    '''
    Return a DataFrame with descriptive statistics
    '''
    df=df.copy()
    df=(df.
          assign(freq2=df[values]*df[fila]).
          assign(mean_2=lambda df_: df_.freq2.sum()/df_[values].sum()).
          assign(var1=lambda df_:((df_[fila]-df_.mean_2)**2)*df_[values])
         )

    data={"numero de casos":[],"suma":[],"maximo":[],"minimo":[],"promedio":[],"varianza":[],"des estandar":[]}
    
    data["numero de casos"].append(df[values].sum())
    data["suma"].append(df.freq2.sum())
    data["maximo"].append(df[fila].max())
    data["minimo"].append(df[fila].min())
    data["promedio"].append(df.freq2.sum()/df[values].sum())
    data["varianza"].append(df.var1.sum()/df[values].sum())
    data["des estandar"].append(np.sqrt(df.var1.sum()/df[values].sum()))
    
    df_f=(pd.DataFrame(data).
          assign(ubigeo=df.ubigeo.iloc[0],
                 coeficiente=lambda df_:(df_["des estandar"]/df_["promedio"])*100).
          rename({"coeficiente":"coeficiente de variacion"},axis=1).
          set_index("ubigeo")
         )
    
    return df_f
    
def multi_column_des(df, values=None):
    fila_1=values
    tup=[(fila_1,'numero de casos'), (fila_1,'suma'), (fila_1,'maximo'), (fila_1,'minimo'), (fila_1,'promedio'), (fila_1,'varianza'),
           (fila_1,'des estandar'), (fila_1,'coeficiente de variacion')]

    df.columns=pd.MultiIndex.from_tuples(tup)
    return df