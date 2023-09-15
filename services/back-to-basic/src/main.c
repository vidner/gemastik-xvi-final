#include <stdio.h>
#include <stdlib.h>

void give_me_idea() {
  char buf[64];
  puts("Do you have a good idea?");
  fgets(buf, 200, stdin);
}

void main() {
  setbuf(stdout, NULL);
  give_me_idea();
  puts("hmm... I'm also think the same thing...");
  return 0;
}