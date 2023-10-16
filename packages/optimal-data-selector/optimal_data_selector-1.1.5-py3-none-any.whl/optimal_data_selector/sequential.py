def timeseries_split(data,column,n_previous_values,train_size=0.8,scaling=None,n_dimention=3,return_index=None):
  """
    Splits a time series dataset into training and testing sets with specified parameters.

    Parameters:

       # data (pd.DataFrame or pd.Series): The input time series data. 

       # column (str): The column name to be used as the time series data.

       # n_previous_values (int): The number of previous values to consider as input for predictions.

       # train_size (float, optional): The proportion of data to be used for training. Default is 0.8.

       # scaling (str, optional) --> ['normal','st_normal'] : Type of data scaling to be applied ('normal' or 'st_normal'). Default is None.

       # n_dimension (int, optional) --> [2,3] : Number of dimensions for input data (2 or 3). Default is 3.

       # return_index (str, optional) --> ['training','validation','both'] : use this parameter to get back the index value of the data

                                            specially in the case of Date and time. Default is None

    Returns:
        tuple: A tuple containing the split data and labels depending on n_dimension.
            If n_dimension = 2:
                - x_train (numpy.ndarray): 2D array of training input sequences.
                - x_test (numpy.ndarray): 2D array of testing input sequences.
                - y_train (numpy.ndarray): 1D array of training output values.
                - y_test (numpy.ndarray): 1D array of testing output values.
            If n_dimension = 3:
                - x_train (numpy.ndarray): 3D array of training input sequences.
                - x_test (numpy.ndarray): 3D array of testing input sequences.
                - y_train (numpy.ndarray): 1D array of training output values.
                - y_test (numpy.ndarray): 1D array of testing output values.

    Example:
        x_train, x_test, y_train, y_test, train_indices, test_indices = timeseries_split(
        data=data, column='column_name', n_previous_values=30, n_dimension=3, return_index='both')  


    """
    
  import numpy as np
  import pandas as pd
  import math
  from sklearn.preprocessing import MinMaxScaler,StandardScaler
  mn=MinMaxScaler()
  std=StandardScaler()
    
  df=0
  x_train1=0
  y_train1=0
  x_test1=0
  y_test1=0
  x_train2=0
  y_train2=0
  x_test2=0
  y_test2=0
    
  window=n_previous_values
    
  if type(data) == pd.core.frame.DataFrame:
      df=data
  elif type(data) == pd.core.series.Series:
      df=pd.DataFrame(data[column])
  elif type(data) not in(pd.core.series.Series,pd.core.frame.DataFrame):
      raise TypeError("'data' must be ether 'Series' or 'DataFrame' object")
      
        
  if scaling == 'normal':
      df[column]= mn.fit_transform(df)
  elif scaling == 'st_normal':
      df[column]=std.fit_transform(df)
  elif scaling not in('normal','st_normal',None):
      raise ValueError("'scaling' value must be ether 'normal' or 'st_normal'")    
      
        
  train_len=math.ceil(len(df)*train_size)
  train_ds=df[:train_len]
  test_ds=df[train_len:]
    
  train_x=pd.Series(train_ds[column].values)
  train_x.index=train_ds.index
  #window=n_previous_values
  x_train=[]
  y_train=[]
  x_train_ind=[]
  for i in range(window,len(train_x)):
      x_train.append(train_x[i-window:i])
      y_train.append(train_x[i])
      x_train_ind.append(train_x.index[i])
  x_train1=np.array(x_train)    
  y_train1=np.array(y_train)
        
  test_x=pd.Series(test_ds[column].values)
  test_x.index=test_ds.index
  x_test=[]
  y_test=[]
  x_test_ind=[]
  for r in range(window,len(test_x)):
      x_test.append(test_x[r-window:r])
      y_test.append(test_x[r])
      x_test_ind.append(test_x.index[r])
  x_test1=np.array(x_test)    
  y_test1=np.array(y_test)
    
  if n_dimention == 2 and return_index == None:
      return x_train1,x_test1,y_train1,y_test1
  elif n_dimention == 3 and return_index == None:
      x_train2 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1],1))
      x_test2 = np.reshape(x_test1, (x_test1.shape[0], x_test1.shape[1],1))

      return x_train2,x_test2,y_train1,y_test1

  
  elif n_dimention == 2 and return_index == 'training':
      return x_train1,x_test1,y_train1,y_test1,x_train_ind  

  elif n_dimention == 2 and return_index == 'validation':
      return x_train1,x_test1,y_train1,y_test1,x_test_ind  

  elif n_dimention == 2 and return_index == 'both':
      return x_train1,x_test1,y_train1,y_test1,x_train_ind,x_test_ind 

  elif n_dimention == 3 and return_index == 'training':
      x_train2 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1],1))
      x_test2 = np.reshape(x_test1, (x_test1.shape[0], x_test1.shape[1],1))

      return x_train2,x_test2,y_train1,y_test1,x_train_ind    

  elif n_dimention == 3 and return_index == 'validation':
      x_train2 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1],1))
      x_test2 = np.reshape(x_test1, (x_test1.shape[0], x_test1.shape[1],1))

      return x_train2,x_test2,y_train1,y_test1,x_test_ind     

  elif n_dimention == 3 and return_index == 'both':
      x_train2 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1],1))
      x_test2 = np.reshape(x_test1, (x_test1.shape[0], x_test1.shape[1],1))

      return x_train2,x_test2,y_train1,y_test1,x_train_ind,x_test_ind    

  else: 
    raise ValueError("valid values for return_index are 'training', 'validation', or 'both' | and n_dimension should be either 2 or 3 ")
