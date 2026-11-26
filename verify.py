"""Exact displacement-word certificate for A187176; standard library only."""
from collections import Counter
from itertools import product
from pathlib import Path
import json

MOVES=((2,1),(-1,2),(-2,-1),(1,-2))
CELLS=6
THRESHOLD=10

def spans():
    found=Counter()
    for word in product(MOVES,repeat=CELLS-1):
        x=y=0
        path=[(0,0)]
        for a,b in word:
            x+=a
            y+=b
            path.append((x,y))
        if len(set(path))==CELLS:
            found[tuple(sorted(max(axis)-min(axis) for axis in zip(*path)))]+=1
    return found

if __name__=="__main__":
    h=spans()
    file=Path(__file__).with_name("spans.json")
    assert sorted([w,d,k] for (w,d),k in h.items())==json.loads(file.read_text("utf-8"))
    assert max(d for w,d in h)==THRESHOLD
    quad=[sum(h.values()),-sum(k*(w+d) for (w,d),k in h.items()),
          sum(k*w*d for (w,d),k in h.items())]
    assert quad==[284,-3100,7944],quad
    nmax=THRESHOLD+2
    a=[sum(k*max(n-w,0)*max(n-d,0) for (w,d),k in h.items()) for n in range(nmax+1)]
    den=(1,-3,3,-1)
    got=[sum(den[j]*a[n-j] for j in range(min(n+1,4))) for n in range(nmax+1)]
    want=[0]*6+[8*x for x in [11,29,27,18,-3,-9,-2]]
    want += [0]*(len(got)-len(want))
    assert got==want,(got,want)
    print("A187176 proven: 1024 words; 284 self-avoiding; exact GF numerator.")
