def angleColour(angle,brightness=1):
    return tuple(max(0,min(int((math.cos(angle-math.tau*i/3)+1)/2*brightness*255),255)) for i in range(3))
def tap(func,*iterables): #Python 3 was a mistake
    return tuple(map(func,*iterables))
import random,math
from itertools import pairwise
from functools import reduce
import pygame
from pygame.locals import *
clock=pygame.time.Clock()
pygame.init()
size=[100,100]
minSize=min(size[:2])
FPS=60
screen=pygame.display.set_mode(size[:2],pygame.RESIZABLE)
mouse=pygame.mouse
zoom=1
iterations=1
exposure=1
exponent=2
shortcut=True
def factorial(n): #this is a Gaussian program (god save the Γ(n)=n!)
    return((reduce(int.__mul__,range(1,n+1)) if n else 1) if type(n)==int else sum((t/16)**n*math.e**(-t/16)/16 for t in range(65536))) #1/16≈0, 4096≈∞ (very suspicious)
def binomial(n,k):
    return(factorial(n)//(factorial(k)*factorial(n-k)) if k>=0<=n-k else 0)
def generateComplexExponentiation(n):
    binomials=tuple(binomial(n,k) for k in range(n+1)) #reduce(lambda b,i: (1,)+tap(int.__add__,pairwise(b))+(1,),range(n),(1,))
    return("""def exponentiate(r,i,t,o):
    return(("""+",".join("".join(("-" if i%2 else "+" if i else "")+"*".join((str(b),)*bool(b-1)+("r"+("**"+str(n-2*i-j))*bool(n-2*i-j-1),)*bool(n-2*i-j)+("i"+("**"+str(2*i+j))*bool(2*i+j-1),)*bool(2*i+j)) for i,b in enumerate(binomials[j::2]))+"+"+("o" if j else "t") for j in range(2))+"))")
#print("\n".join(map(generateComplexExponentiation,range(10))))
print(generateComplexExponentiation(exponent))
exec(generateComplexExponentiation(exponent))
def mandelbrot(t,o):
    r,i=0,0
    for n in range(iterations):
        (r,i)=exponentiate(r,i,t,o) #this program sponsored by 'ritos
        if shortcut and r**2+i**2>exponent**exponent:
            break
    return(r,i)
def renderMandelbrot():
    global complexes,colours
    complexes=[mandelbrot(((x-size[0]/2)/minSize)/zoom,((y-size[1]/2)/minSize)/zoom) for x in range(size[0]) for y in range(size[1])]
    colours=[(math.atan2(i,r),math.hypot(r,i)) for r,i in complexes]
    rerenderMandelbrot(colours)
def rerenderMandelbrot(colours):
    for (x,y),(c,b) in zip(((x,y) for x in range(size[0]) for y in range(size[1])),colours):
        screen.set_at((x,y),angleColour(c,exposure*b))
run=True
renderMandelbrot()
toggleKeys=(pygame.K_EQUALS,pygame.K_MINUS,pygame.K_LEFTBRACKET,pygame.K_RIGHTBRACKET,K_PERIOD,K_COMMA,K_SEMICOLON,K_QUOTE)
oldToggles=[False]*len(toggleKeys)
while run:
    keys=pygame.key.get_pressed()
    toggles=[keys[k] for k in toggleKeys]
    for i,(k,o) in enumerate(zip(toggles,oldToggles)):
        if not k and o:
            if i==4:
                exposure*=2
                print("exposure",exposure)
                rerenderMandelbrot(colours)
            elif i==5:
                exposure/=2
                print("exposure",exposure)
                rerenderMandelbrot(colours)
            else:
                if i==0:
                    zoom*=2
                    print("zoom",zoom)
                elif i==1:
                    zoom/=2
                    print("zoom",zoom)
                elif i==2:
                    if iterations>1:
                        iterations-=1
                        print(iterations)
                elif i==3:
                    iterations+=1
                    print(iterations)
                elif i==6:
                    if exponent>1:
                        exponent-=1
                        exec(generateComplexExponentiation(exponent))
                    print("exponent",exponent)
                elif i==7:
                    exponent+=1
                    exec(generateComplexExponentiation(exponent))
                    print("exponent",exponent)
                renderMandelbrot()
    oldToggles=toggles
    clickDone=False
    shortClickDone=False
    if mouse.get_pressed()[0]:
        framesMouseDown+=1
    else:
        framesMouseDown=0
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONUP:
            clickDone=True
            if framesMouseDown<0.2*FPS:
                shortClickDone=True
        if event.type==pygame.WINDOWRESIZED:
            size[:2]=screen.get_rect().size
            minSize=min(size[:2])
            renderMandelbrot()
    pygame.display.flip()
    size[:2]=screen.get_size()
    clock.tick(FPS)
