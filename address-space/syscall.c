#include <stdio.h>

size_t strlen(const char *s) {
    const char *sc;

    for (sc = s; *sc != '\0'; ++sc)
        /* nothing */;
    return sc - s;
}

int main() {
    // 创建 str 字符串
    char str[] = "Hello World";
    // 调用 strlen 函数，并把值赋予 length
    int length = strlen(str);
    // 在终端打印内容
    printf("The length of str is %d\n", length);
    return 0;
}