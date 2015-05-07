/* tst-unique5lib.so library for tst-unique5.cc.  */

extern int not_exist (void);

inline int make_unique (void)
{
  static int unique;
  return ++unique;
}

int foo (void)
{
  return make_unique () + not_exist ();
}
