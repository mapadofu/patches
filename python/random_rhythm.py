import itertools
import random
random.seed()
import math

class BeatPattern(object):
    def __init__(self, lily, onsets, endings):
        self.lily=lily
        self.onsets=onsets
        self.endings=endings
        #self.inverted=0 # TBD: allow for "inverted"
    def __iter__(self):
        ''' Make me look like a (single-element) sequence of beats '''
        yield self

options=[
    BeatPattern( 'c4', [1,0,0,0], [0,0,0,1] ),
    BeatPattern( 'c4-.', [1,0,0,0], [0,1,0,0] ),
    BeatPattern( 'r4', [0,0,0,0], [0,0,0,0] ),
    BeatPattern( 'c8 c8', [1,0,1,0], [0,1,0,1] ),
    BeatPattern( 'c8-. c8', [1,0,1,0], [1,0,0,1] ),
    BeatPattern( 'c8-. c8-.', [1,0,1,0], [1,0,1,0] ),
    BeatPattern( 'c8 c8-.', [1,0,1,0], [0,1,1,0] ),
    BeatPattern( 'r8 c8', [0,0,1,0], [0,0,0,1] ),
    BeatPattern( 'r8 c8-.', [0,0,1,0], [0,0,1,0] ),
    BeatPattern( 'c16 c16 c16 c16', [1,1,1,1], [1,1,1,1] ),
    BeatPattern( 'r16 c16 c16 c16', [0,1,1,1], [0,1,1,1] ),
    BeatPattern( 'c8-. c16 c16', [1,0,1,1], [1,0,1,1] ),
    BeatPattern( 'c16 c16 r16 c16', [1,1,0,1], [1,1,0,1] ),
    BeatPattern( 'c16 c16 c8-.', [1,1,1,0], [1,1,1,0] ),
    BeatPattern( 'c8 c16 c16', [1,0,1,1], [0,1,1,1] ),
    BeatPattern( 'r8 c16 c16', [0,0,1,1], [0,0,1,1] ),
    BeatPattern( 'c8 r16 c16', [1,0,0,1], [0,1,0,1] ),
    BeatPattern( 'c16 c16 c8', [1,1,1,0], [1,1,0,1] ),
    BeatPattern( 'r16 c16 c8', [0,1,1,0], [0,1,0,1] ),
    BeatPattern( 'c16 c16 c8-.', [1,1,1,0], [1,1,1,0] ),
]


def _ndiff(seq1, seq2):
    return len( [(a,b) for (a,b) in itertools.izip(seq1,seq2) if a!=b])
def _onsets( beats ):
    return itertools.chain( *[b.onsets for b in beats])
def _endings(beats):
    return itertools.chain( *[b.endings for b in beats])
def _onoffs(beats):
    return itertools.chain( _onsets(beats), _endings(beats) )
def _lily(beats):
    return " ".join( [b.lily for b in beats] )

def E1( patt ):
    on_the_one=patt[0].onsets[0] # do we "hit the one?"
    if on_the_one:
        return -0.1
    else:
        return 0.0

def E2( patt ):
    (head,tail)=(patt[:2], patt[2:])
    return 0.0 # TBD: is there something sensible here

def E4(patt):
    (a,b,c,d)=patt
    g_ac=0.1*(1.0/16)
    g_bd=0.05*(1.0/16)
    g_ab=0.05*(1.0/16)
    return g_ac*_ndiff( _onoffs(a), _onoffs(c) )+g_bd*_ndiff( _onoffs(b), _onoffs(d) )+ g_ab*_ndiff( _onoffs(a), _onoffs(b) )

def E(patt):
    return E1(patt)+E2(patt)+E4(patt)

def metropolis(patt, kT=1.0):
    proposed=patt[:]
    proposed[int(random.random()*len(proposed))]=random.choice( options )
    dE=E(proposed)-E(patt)
    print "E-initial: {0} E-final: {1}, dE={2}".format( E(patt), E(proposed), dE)
    if dE<0.0 or random.random()<math.exp(-dE/kT):
        return proposed
    else:
        return patt

def relax(patt, n, kT=1.0):
    for i in xrange(n):
        patt=metropolis(patt, kT)
    return patt


lilytemplate="""
\\version "2.18.0"
\\paper {{
    #(set-paper-size "b8")
}}
\\header {{
  tagline="" % removed
}}
\score {{
  \\new Staff {{
    \\omit Staff.Clef
    \\omit Staff.TimeSignature
    \\relative c'' {{
        {0}
    }}
  }}
  \\layout{{
  }}
}}

"""

A=[random.choice(options) for i in xrange(4)]
A=relax(A, 2)
B=relax(A, 3)
C=relax(B, 3)
D=relax(C, 3)
print lilytemplate.format( _lily(A+B+C+D) )
