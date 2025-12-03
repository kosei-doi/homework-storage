void Multiply1(int m,int n,double X[m][n],double Y[m][n]){
  double X_t[n][m] = {0};
  for(int i = 0; i < m; i++){
    for(int j = 0; j < n; j++){
      X_t[j][i] = X[i][j];
    }


  for(int i = 0; i < m; i++){
    for(int j = 0; j < m; j++){
      double sum = 0;
      for(int k = 0; k < n; k++){
        sum += X[i][k] * X[j][k];
      }
      Y[i][j] = sum;
    }
  }
}
}

void Multiply2(int m,int n,double X[m][n],double Y[n][n]){
  for(int i = 0; i < n,i++){
    for(int j = 0; j < n,j++){
      double sum = 0;
      for(int k = 0;k < m; k++){
        sum += X[k][i] * X[k][j]
      }
      Y[i][j] = sum;
    }
  }
}