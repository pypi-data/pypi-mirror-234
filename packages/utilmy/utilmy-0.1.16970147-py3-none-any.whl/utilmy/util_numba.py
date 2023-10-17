'''Numba  High Speed Computation utilities   ----------------------------------------------------------------------------
Docs ::

    https://github.com/barbagroup/numba_tutorial_scipy2016/blob/master/notebooks/09.Tips.and.FAQ.ipynb

    ####################### Signature Type #################################################################################
    Explicit @jit signatures can use a number of types. Here are some common ones:
      void is the return type of functions returning nothing (which actually return None when called from Python)
      intp and uintp are pointer-sized integers (signed and unsigned, respectively)
      intc and uintc are equivalent to C int and unsigned int integer types
      int8, uint8, int16, uint16, int32, uint32, int64, uint64 are fixed-width integers of the corresponding bit width (signed and unsigned)
      float32 and float64 are single- and double-precision floating-point numbers, respectively

      array types can be specified by indexing any numeric type, e.g. float32[:] for a one-dimensional
      single-precision array or int8[:,:] for a two-dimensional array of 8-bit integers.

    The first character specifies the kind of data and the remaining characters specify the number of bytes per item,
    except for Unicode, where it is interpreted as the number of characters.
    'b'	boolean
    'i'	(signed) integer
    'u'	unsigned integer
    'f'	floating-point
    'c'	complex-floating point
    'O'	(Python) objects
    'S', 'a'	(byte-)string
    'U'	Unicode
    'V'	raw data (void)

    f2: 16bits, f4: 32 bits,  f8: 64bits
    dt = np.dtype('i4')   # 32-bit signed integer
    dt = np.dtype('f8')   # 64-bit floating-point number
    np.dtype('c16')  # 128-bit complex floating-point number
    np.dtype('a25')  # 25-character string


'''
import  numpy as np, math as mm,  numba, numexpr as ne
from numba import jit, njit,  autojit, int32, float32, float64, int64, double
from math import exp, sqrt, cos, sin, log1p




def test_all():
  pass


def test1():
  pass




###################################  Statistical #######################################################################
@dv.parallel(block=True)
def np_std_par(x):
    return np_std(x)

# bsk= np.array(bsk, dtype=np.float64)
# %timeit std(bsk)


@njit(float64(float64[:]),  cache=True, nogil=True, target='cpu')
def np_mean(x):
    """Mean  """
    return x.sum() / x.shape[0]


@njit([float64(float64,float64)], cache=True, nogil=True, target='cpu')
def np_log_exp_sum2 (a, b):
    if a >= b: return a + log1p(exp (-(a-b)))
    else:      return b + log1p(exp (-(b-a)))
    ## return max (a, b) + log1p (exp (-abs (a - b)))


@njit('Tuple( (int32, int32, int32) )(int32[:], int32[:])', cache=True, nogil=True, target='cpu')
def _compute_overlaps(u, v):
    a = 0
    b = 0
    c = 0
    m = u.shape[0]
    for idx in xrange(m):
        a += u[idx] & v[idx]
        b += u[idx] & ~v[idx]
        c += ~u[idx] & v[idx]
    return a, b, c
 
 
@njit(float32(int32[:], int32[:]), cache=True, nogil=True, target='cpu')
def distance_jaccard2(u, v):
    a, b, c = _compute_overlaps(u, v)
    return 1.0 - (a / float(a + b + c))


@njit(float32(int32[:], int32[:]),  cache=True, nogil=True, target='cpu')
def distance_jaccard(u, v):
    a = 0;    b = 0;    c = 0
    m = u.shape[0]
    for idx in range(m):
        a += u[idx] & v[idx]
        b += u[idx] & ~v[idx]
        c += ~u[idx] & v[idx] 
    return 1.0 - (a / float(a + b + c))


@njit(float32[:,:](int32[:,:]),  cache=True, nogil=True, target='cpu' )
def distance_jaccard_X(X):
 n= X.shape[0]    
 dist= np.zeros((n,n), dtype=np.float32)
 for i in range(0,n):
    for j in range(i+1,n):
      dist[i,j]=  distance_jaccard(X[i,:], X[j,:])
      dist[j,i]=  dist[i,j]
 return dist
 
     

@njit('float64(float64[:], float64[:])', cache=True, nogil=True, target='cpu')
def cosine(u, v):
    m = u.shape[0]
    udotv = 0
    u_norm = 0
    v_norm = 0
    for i in range(m):
        if (np.isnan(u[i])) or (np.isnan(v[i])):
            continue
             
        udotv += u[i] * v[i]
        u_norm += u[i] * u[i]
        v_norm += v[i] * v[i]
 
    u_norm = np.sqrt(u_norm)
    v_norm = np.sqrt(v_norm)
     
    if (u_norm == 0) or (v_norm == 0):
        ratio = 1.0
    else:
        ratio = udotv / (u_norm * v_norm)
    return ratio
    
# %timeit cosine(x, y)



