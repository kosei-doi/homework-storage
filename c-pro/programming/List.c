#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    double* Data;
    int Size;
    int Count;
} List;

void Error(const char* message) {
    fprintf(stdout, "\e[91m%s\e[m\n", message);
    exit(EXIT_FAILURE);
}

void* Alloc(size_t size, int n) {
    if (n < 0) Error("Alloc: size < 0");
    void* p = calloc((size_t)n, size);
    if (p == NULL) Error("cannot allocate memory");
    return p;
}

#define ALLOC1(type) Alloc(sizeof(type), 1)
#define ALLOCN(type, n) Alloc(sizeof(type), n)

List* ListCreate(void) {
    List* l = ALLOC1(List);
    l->Count = 0;
    l->Size = 4;
    l->Data = ALLOCN(double, l->Size);
    return l;
}

void ListDispose(List* l) {
    free(l->Data);
    free(l);
}

double ListGetItem(List* l, int index) {
    if (index < 0 || index >= l->Count) Error("ListGetItem: index OutOfRange");
    return l->Data[index];
}

void ListSetItem(List* l, int index, double value) {
    if (index < 0 || index >= l->Count) Error("ListSetItem: index OutOfRange");
    l->Data[index] = value;
}

void ListInsert(List* l, int index, double value) {
    if (index < 0 || index > l->Count) Error("ListInsert: index OutOfRange");
    if (l->Count < l->Size) {
        for (int i = l->Count; --i >= index;) l->Data[i + 1] = l->Data[i];
    } else {
        double* old = l->Data;
        l->Size *= 2;
        l->Data = ALLOCN(double, l->Size);
        for (int i = 0; i < index; i++) l->Data[i] = old[i];
        for (int i = index; i < l->Count; i++) l->Data[i + 1] = old[i];
        free(old);
    }
    l->Data[index] = value;
    l->Count++;
}

void ListAdd(List* l, double value) {
    ListInsert(l, l->Count, value);
}

void ListRemove(List* l, int index) {
    if (index < 0 || index >= l->Count) Error("ListRemove: index OutOfRange");
    for (int i = index + 1; i < l->Count; i++) l->Data[i - 1] = l->Data[i];
    l->Count--;
}

bool IsPrime2(int x) {
    if (x < 2) return false;
    int w = (int)sqrt(x);
    for (int y = 2; y <= w; y++) {
        if (x % y == 0) return false;
    }
    return true;
}

bool IsPrime3(int x, List* l) {
    if (x < 2) return false;
    int w = (int)sqrt(x);
    for (int i = 0; i < l->Count; i++) {
        int y = (int)ListGetItem(l, i);
        if (y > w) break;
        if (x % y == 0) return false;
    }
    return true;
}

int CountPrimes2(int n) {
    int count = 0;
    for (int x = 2; x <= n; x++) {
        if (IsPrime2(x)) count++;
    }
    return count;
}

int CountPrimes3(int n) {
    List* l = ListCreate();
    int count = 0;
    for (int x = 2; x <= n; x++) {
        if (IsPrime3(x, l)) {
            ListAdd(l, (double)x);
            count++;
        }
    }
    ListDispose(l);
    return count;
}

double Measure(int n, int (*func)(int)) {
    clock_t c0 = clock();
    int count = func(n);
    clock_t c1 = clock();
    double span = (double)(c1 - c0) / (double)CLOCKS_PER_SEC;
    printf("\n%d以下の素数の個数: %d\n", n, count);
    return span;
}

int main(void) {
    int n = 100;
    List* l = ListCreate();
    for (int x = 2; x <= n; x++) {
        if (IsPrime3(x, l)) {
            ListAdd(l, (double)x);
        }
    }
    for (int i = 0; i < l->Count; i++) {
        printf("%.0f", ListGetItem(l, i));
        if (i < l->Count - 1) printf(", ");
    }
    printf("\n");
    printf("%d以下の素数の個数: %d\n", n, l->Count);
    ListDispose(l);
    
    n = 10000000;
    printf("試行除算法[2]: %f [秒]\n", Measure(n, CountPrimes2));
    printf("試行除算法[3]: %f [秒]\n", Measure(n, CountPrimes3));
    return 0;
}

