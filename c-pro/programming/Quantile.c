#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void Swap(double* x, double* y) {
    double a = *x;
    double b = *y;
    *y = a;
    *x = b;
}

void PrintData(int n, double data[n], int L, int R) {
    return;
    for (int i = 0; i < n; i++) {
        if (L <= i && i <= R)
            printf("%02.0f ", data[i]);
        else
            printf(" | ");
    }
    printf("\n");
}

void SetData(int n, double data[n]) {
    srandom(1127);
    for (int i = 0; i < n; i++)
        data[i] = (int)random() % 100;
}

void LetQuickSort_(int n, double data[n], int L, int R) {
    int l = L;
    int r = R;
    double pivot = data[(L + R) / 2];
    while (true) {
        if (r < l) break;
        while (data[l] < pivot) l++;
        while (pivot < data[r]) r--;
        if (r < l) break;
        if (l < r) Swap(&data[l], &data[r]);
        l++;
        r--;
        PrintData(n, data, L, R);
    }
    if (L < r) LetQuickSort_(n, data, L, r);
    if (l < R) LetQuickSort_(n, data, l, R);
}

void LetQuickSort(int n, double data[n]) {
    PrintData(n, data, 0, n - 1);
    if (n >= 2) LetQuickSort_(n, data, 0, n - 1);
}

double Quantile(int n, double data[n], double q) {
    if (n < 2) return data[0];
    double s = (n - 1) * q;
    int t = (int)floor(s);
    double r = s - t;
    if (r == 0.0) {
        return data[t];
    } else {
        return (1.0 - r) * data[t] + r * data[t + 1];
    }
}

int main(void) {
    int n = 20;
    double data[n];
    SetData(n, data);
    LetQuickSort(n, data);
    printf("%d/4-quantile: %f\n", 0, Quantile(n, data, 0.0));
    printf("%d/4-quantile: %f\n", 1, Quantile(n, data, 0.25));
    printf("%d/4-quantile: %f\n", 2, Quantile(n, data, 0.5));
    printf("%d/4-quantile: %f\n", 3, Quantile(n, data, 0.75));
    printf("%d/4-quantile: %f\n", 4, Quantile(n, data, 1.0));
    return 0;
}

