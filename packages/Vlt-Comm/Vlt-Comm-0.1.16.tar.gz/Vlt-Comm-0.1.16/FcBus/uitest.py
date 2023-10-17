import numpy as np
import time
import asyncio

dtime = 0.05

async def f0():
    await asyncio.sleep(dtime)
    return np.random.normal()

async def f1():
    await asyncio.sleep(dtime)
    return np.random.normal()*10

def f00():
    time.sleep(dtime)
    return np.random.normal()

def f11():
    time.sleep(dtime)
    return np.random.normal()*10

async def f2():
    await asyncio.sleep(dtime)
    return np.random.normal()*30

u = ui(f0, f1, f2)
#u0 = ui(f00,f11,f2)
u.max_len=50
#u0.max_len = 50