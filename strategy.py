from sklearn.model_selection import TimeSeriesSplit

# Position sizing
def position_size(confidence):
  if confidence < 0.6:
    return 0
  elif confidence < 0.8:  
    return 1
  else:
    return 2

# Risk management
max_loss = 100
loss = 0

# Walk-forward testing
wf = TimeSeriesSplit(n_splits=5)

for train_index, test_index in wf.split(df):
  
  X_train, X_test = df.iloc[train_index], df.iloc[test_index]

  model.fit(X_train, y_train)

  # Make predictions
  conf = model.predict_proba(X_test)[:,1]
  
  for i in range(len(X_test)):
    ps = position_size(conf[i])
    
    if ps > 0:
      # Execute trade
      if ps == 1:
        invest = 50
      elif ps == 2:
        invest = 100
        
      if model.predict(X_test.iloc[i]) == 1:
        buy_call(invest)
      else: 
        buy_put(invest)

    if loss > max_loss:
      print("Max loss reached, stopping.")
      break
