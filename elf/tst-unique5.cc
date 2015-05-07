#include "../dlfcn/dlfcn.h"
#include <stdlib.h>

/* unique5lib.so library contains both STB_GNU_UNIQUE and undefined symbols.
   First dlopen call fails because of undefined symbols.  Test checks that
   library does not remain locked in the memory in this case. [BZ #17833]  */

int
main (void)
{
  void *h;
  dlopen ("$ORIGIN/tst-unique5lib.so", RTLD_NOW);
  h = dlopen ("$ORIGIN/tst-unique5lib.so", RTLD_LAZY | RTLD_NOLOAD);
  return h != NULL;
}
