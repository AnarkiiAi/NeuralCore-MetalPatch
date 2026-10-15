import ast,pathlib,typing,unittest
import numpy as np
P=pathlib.Path(__file__).parent
class MX:
 array=staticmethod(np.array)
 arange=staticmethod(np.arange)
 zeros=staticmethod(np.zeros)
 concatenate=staticmethod(np.concatenate)
 eval=staticmethod(lambda *x:None)
class Base:pass
def load(path):
 tree=ast.parse(path.read_text())
 cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='ArraysCache')
 env={'mx':MX(),'_BaseCache':Base,'Optional':typing.Optional,'List':typing.List}
 exec(compile(ast.fix_missing_locations(ast.Module(body=[cls],type_ignores=[])),str(path),'exec'),env)
 return env['ArraysCache']
Old=load(P.parent/'028'/'cache.upstream.py')
New=load(P/'cache.patched.py')
class Tests(unittest.TestCase):
 def pair(self):
  a,b=Old(2,[1,3]),New(2,[1,3])
  for c in (a,b):c.prepare([9,7])
  return a,b
 def same(self,a,b):
  for attr in ('lengths','left_padding'):
   x,y=getattr(a,attr),getattr(b,attr)
   if x is not None:np.testing.assert_array_equal(x,y)
  np.testing.assert_array_equal(a.make_mask(12),b.make_mask(12))
 def test_20000(self):
  a,b=self.pair()
  for _ in range(20000):a.advance(1);b.advance(1)
  self.same(a,b)
 def test_interleaved(self):
  a,b=self.pair()
  for i in range(100):
   self.same(a,b);a.advance(i%3+1);b.advance(i%3+1)
  self.same(a,b)
 def test_state(self):
  a,b=self.pair()
  for c in (a,b):c.advance(4)
  x,y=Old(2),New(2)
  x.state=a.state;y.state=b.state
  self.same(x,y)
 def test_filter(self):
  a,b=self.pair()
  for c in (a,b):c.advance(2);c.filter([1])
  self.same(a,b)
 def test_extend(self):
  a,b=self.pair();c,d=self.pair()
  for x in (a,b,c,d):x.advance(2)
  a.extend(c);b.extend(d);self.same(a,b)
 def test_finalize(self):
  a,b=self.pair()
  for c in (a,b):c.advance(3);c.finalize();c.prepare([8,6])
  self.same(a,b)
 def test_empty_merge(self):
  a,b=self.pair()
  for c in (a,b):c.advance(2)
  self.same(Old.merge([a]),New.merge([b]))
 def test_setter(self):
  a,b=self.pair()
  for c in (a,b):
   c.advance(2);c.lengths=np.array([6,4]);c.left_padding=np.array([-1,1])
  self.same(a,b)
if __name__=='__main__':unittest.main(verbosity=2)
