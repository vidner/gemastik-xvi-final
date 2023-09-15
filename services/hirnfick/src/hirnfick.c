#include <stdio.h>
// gcc hirnfick.c -o hirnfick -Wl,-z,norelro -no-pie
#define match(from, to, ptr, dir, level)                                       \
  while (*(dir ptr)) {                                                         \
    if (*ptr == to && level == 0)                                              \
      break;                                                                   \
    if (*ptr == from)                                                          \
      ++level;                                                                 \
    if (*ptr == to)                                                            \
      --level;                                                                 \
  }

int debug = 0;
char data[1024] = {0};
char code[1024] = {0};

void exec() {
  char *pc = code;
  char *p = data;
  ;
  int level = 0;
  int ch;
  while (*pc) {
    switch (*pc) {
    case '>':
      ++p;
      break;
    case '<':
      --p;
      break;
    case '+':
      ++*p;
      break;
    case '-':
      --*p;
      break;
    case '.':
      putchar(*p);
      break;
    case ',':
      *p = ((ch = getchar()) == EOF) ? 0 : ch;
      break;
    case '[':
      if (!*p)
        match('[', ']', pc, ++, level);
      break;
    case ']':
      if (*p)
        match(']', '[', pc, --, level);
      break;
    default:
      break;
    }
    pc++;
  }
}

int main(int argc, const char *argv[]) {
  FILE *fp = fopen(argv[1], "r");
  char *pc = code;
  int ch;
  puts("HirnFick 1.0");
  while ((ch = fgetc(fp)) != EOF) {
    if (ch == '>' || ch == '<' || ch == '+' || ch == '-' || ch == '[' ||
        ch == ']' || ch == '.' || ch == ',')
      *(pc++) = ch;
  }
  fclose(fp);
  exec();
  if (debug) {
    puts(data);
  }
  return 0;
}
