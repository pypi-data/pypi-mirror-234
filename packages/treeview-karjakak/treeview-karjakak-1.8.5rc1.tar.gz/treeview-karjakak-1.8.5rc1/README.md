# TreeView
## Writing an outline note with tree-view look.

## Installation
```
pip install treeview-karjakak
```
## Usage
```Python
from treeview import TreeView, conftv

# To configure the childs (by default 50 childs, and 4 spaces)
TreeView = conftv(TreeView, 5, 1)
print(dict(TreeView.childs))

w = 'Amazing Grace'
with TreeView('test') as tv:

    # First time write on note as parent
    tv.writetree(w)

    # Write it with loop in childs 
    for i in range(5):
        tv.quickchild(w, child = f'child{i+1}')
        
    # Edit the parent
    tv.edittree('Amazing Grace, how sweet the sound')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Edit again in row 4 to child2
    tv.edittree('Mantaaaaaaap!', row = 4, child = 'child2')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Write new parent
    tv.addparent('Wow good job')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Edit again in row 6 to child5
    tv.edittree('Wow good job buddy', row = 6, child = 'child5')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Write again new childs
    tv.quickchild('Totally awesome', child = 'child1')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    tv.quickchild('This is quick child edit', child = 'child2')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    tv.quickchild('Thank You', child = 'child1')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Delete row 10
    tv.delrow(10)
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Insert to row 8 as child1
    tv.insertrow('God bless you', row = 8, child = 'child1' )
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Moving position from row 6 to row 4
    tv.movetree(6, 4)
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Moving position of child in row 6 as child1
    tv.movechild(6, child = 'child1')
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    
    # Print an iterator to dict
    pprint(dict(tv.insighttree()))
    
    # Create spaces between rows
    for i in range(1, tv.getdatanum()+4, 2):
        if i == 15:
            break
        tv.insertspace(i)
    print('-'* 12)
    tv.readtree()
    print('-'* 12)
    pprint(dict(tv.insighttree()))
    
    # Backup note as json file
    tv.backuptv()
    del tv, w, i
```
**Result:**
```Python
{'child1': 1, 'child2': 2, 'child3': 3, 'child4': 4, 'child5': 5}
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
    -Amazing Grace
     -Amazing Grace
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace

Wow good job:
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy

Wow good job:
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy

Wow good job:
 -Totally awesome
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy

Wow good job:
 -Totally awesome
  -This is quick child edit
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy

Wow good job:
 -Totally awesome
  -This is quick child edit
 -Thank You
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy

Wow good job:
 -Totally awesome
 -Thank You
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
  -Mantaaaaaaap!
     -Amazing Grace
     -Wow good job buddy
 -God bless you

Wow good job:
 -Totally awesome
 -Thank You
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
     -Wow good job buddy
  -Mantaaaaaaap!
     -Amazing Grace
 -God bless you

Wow good job:
 -Totally awesome
 -Thank You
------------
------------
Amazing Grace, how sweet the sound:
 -Amazing Grace
  -Amazing Grace
   -Amazing Grace
     -Wow good job buddy
  -Mantaaaaaaap!
 -Amazing Grace
 -God bless you

Wow good job:
 -Totally awesome
 -Thank You
------------
{0: ('parent', 'Amazing Grace, how sweet the sound:\n'),
 1: ('child1', '-Amazing Grace\n'),
 2: ('child2', '-Amazing Grace\n'),
 3: ('child3', '-Amazing Grace\n'),
 4: ('child5', '-Wow good job buddy\n'),
 5: ('child2', '-Mantaaaaaaap!\n'),
 6: ('child1', '-Amazing Grace\n'),
 7: ('child1', '-God bless you\n'),
 8: ('space', '\n'),
 9: ('parent', 'Wow good job:\n'),
 10: ('child1', '-Totally awesome\n'),
 11: ('child1', '-Thank You\n')}
------------
Amazing Grace, how sweet the sound:

 -Amazing Grace

  -Amazing Grace

   -Amazing Grace

     -Wow good job buddy

  -Mantaaaaaaap!

 -Amazing Grace

 -God bless you

Wow good job:
 -Totally awesome
 -Thank You
------------
{0: ('parent', 'Amazing Grace, how sweet the sound:\n'),
 1: ('space', '\n'),
 2: ('child1', '-Amazing Grace\n'),
 3: ('space', '\n'),
 4: ('child2', '-Amazing Grace\n'),
 5: ('space', '\n'),
 6: ('child3', '-Amazing Grace\n'),
 7: ('space', '\n'),
 8: ('child5', '-Wow good job buddy\n'),
 9: ('space', '\n'),
 10: ('child2', '-Mantaaaaaaap!\n'),
 11: ('space', '\n'),
 12: ('child1', '-Amazing Grace\n'),
 13: ('space', '\n'),
 14: ('child1', '-God bless you\n'),
 15: ('space', '\n'),
 16: ('parent', 'Wow good job:\n'),
 17: ('child1', '-Totally awesome\n'),
 18: ('child1', '-Thank You\n')}
```