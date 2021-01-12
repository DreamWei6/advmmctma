import math
import profile

useBpc = True
limits = [
    [
        [0, 100],
        [-128, 128],
        [-128, 128]
    ],
    [
        [0, 255],
        [0, 255],
        [0, 255]
    ],
    [
        [0, 100],
        [0, 100],
        [0, 100],
        [0, 100]
    ]
]
last = [0, 0, 0, 0]
smallXyzMode = True
illuminants = [
    [1.0985, 1, 0.35585],
    [1.11144, 1, 0.352],
    [0.98074, 1, 1.18232],
    [0.97285, 1, 1.16145],
    [0.96422, 1, 0.82521],
    [0.9672, 1, 0.81427],
    [0.95682, 1, 0.92149],
    [0.95799, 1, 0.90926],
    [0.95047, 1, 1.08883],
    [0.94811, 1, 1.07304],
    [0.94972, 1, 1.22638],
    [0.94416, 1, 1.20641]
]
illuminantIn = 4
illuminantOut = 4




def convert(mode, input0, input1, input2, input3, smallXyzMode, illuminantIn, illuminantOut):
    a = illuminants[illuminantIn]
    b = illuminants[illuminantOut]
    #c = document.getElementById("mode").selectedIndex,
    c = int(mode)
    #d = [document.getElementById("rgb"), document.getElementById("hex"), document.getElementById("cmyk"), document.getElementById("cielab"), document.getElementById("xyz")],
    #d = ["rgb", "hex", "cmyk", "cielab", "xyz"]
    e = [input0, input1, input2, input3] 
    if c == 0:
        i = [e[0], e[1], e[2]]
        for j in range(3):
            try:
                if i[j] != int(i[j]):
                    pass
            except:
                return "Invalid input"

        f = fixXyz(labToXyz(i, a)) 
        i = xyzToLab(f, b) 
        g = xyzTosRGB(f, b) 
        h = xyzToCMYK(f, b, useBpc)
    if c == 1:
        g = [e[0], e[1], e[2]]
        for j in range(3):
            try:
                if g[j] != int(g[j]):
                    pass
            except:
                return "Invalid input"

        f = fixXyz(sRGBtoXYZ(g, a)) 
        g = xyzTosRGB(f, b)
        h = xyzToCMYK(f, b, useBpc)
        i = xyzToLab(f, b)
    
    if c == 2:
        h = [e[0], e[1], e[2], e[3]]
        for j in range(4):
            try:
                if h[j] != int(h[j]):
                    pass
            except:
                return "Invalid input"
            
        k = [h[0] / 100, h[1] / 100, h[2] / 100, h[3] / 100]
        f = fixXyz(cmykToXyz(k, a, useBpc)) 
        h = xyzToCMYK(f, b, useBpc)
        g = xyzTosRGB(f, b)
        i = xyzToLab(f, b)
    if c == 3:
        hex_code = str(e[0])
        l = int(hex_code, 16)
        try:
            if len(hex_code) != 6:
                return "Invalid input"
        except:
            return "Invalid input"
        
        g = hexToRgb(l) 
        f = fixXyz(sRGBtoXYZ(g, a)) 
        g = xyzTosRGB(f, b)
        h = xyzToCMYK(f, b, useBpc)
        i = xyzToLab(f, b)
    if c == 4:
        if smallXyzMode == True:
            m = 1
        else:
            m = 100
        f = [e[0] / m, e[1] / m, e[2] / m]
        for j in range(3):
            try:
                if f[j] != int(f[j]):
                    pass
            except:
                return "Invalid input"

        f = fixXyz(f)
        g = xyzTosRGB(f, b)
        h = xyzToCMYK(f, b, useBpc)
        i = xyzToLab(f, b)
    
    n = [0,0,0]
    for j in range(3):
        n[j] = '{:02x}'.format(g[j])
    hex_code = n[0] + n[1] + n[2]

    for j in range(3):
        i[j] = '{:.2f}'.format(i[j])
    
    if smallXyzMode == False:
        for j in range(3):
            f[j] *= 100
            f[j] = '{:.2f}'.format(f[j])
    else:
        for j in range(3):
            f[j] = '{:.4f}'.format(f[j])
    
    o = [b[0], b[1], b[2]]
    if smallXyzMode == False:
        for j in range(3):
            o[j] *= 100
            o[j] = '{:.2f}'.format(o[j])
    else:
        for j in range(3):
            o[j] = '{:.4f}'.format(o[j])
    #p = "(0 to " + o[0] + ", 0 to " + o[1] + ", 0 to " + o[2] + ")"
    output = {
        'RGB': str(g[0]) + "," + str(g[1]) + "," + str(g[2]),
        'HEX': hex_code.upper(),
        'CMYK': str(h[0]) + "% " + str(h[1]) + "% " + str(h[2]) + "% " + str(h[3]) + "%",
        'CIELAB': i[0] + "," + i[1] + "," + i[2],
        'XYZ': f[0] + "," + f[1] + "," + f[2]
    }
    return output

def fixXyz(a):
    b = a[0] > illuminants[illuminantIn][0] or a[1] > illuminants[illuminantIn][1] or a[2] > illuminants[illuminantIn][2]
    #if illuminantIn != illuminantOut and a == convertXyz(a):
    if illuminantIn != illuminantOut and b != True : # ??
        for c in range(3):
            a[c] = illuminants[illuminantOut][c]
    return a


def convertXyz(a):
    return adaptXyz(a, illuminants[illuminantIn], illuminants[illuminantOut])


# function format(a, b) {
#     for (var c = 0; c < a.length; c++) a[c] = a[c].toFixed(b)
# }

# function idToIndex(a) {
#     return Number(a.slice(-1))
# }

# function limitInputs() {
#     var a = document.getElementById("mode").selectedIndex;
#     if ("" == this.value) return void(last[idToIndex(this.id)] = this.value);
#     if (3 === a) {
#         var b;
#         (/[^A-F0-9]/i.test(this.value) || this.value.length > 6 || (b = parseInt(this.value, 16)) > 16777215 || b < 0) && (this.value = last[idToIndex(this.id)])
#     } else if (4 === a) {
#         if (smallXyzMode) var c = 1;
#         else var c = 100;
#         var b = illuminants[illuminantIn][idToIndex(this.id)] * c,
#             d = Math.min(b, Math.max(this.value, this.min));
#         isNaN(d) || this.value.includes(".") || (this.value = d), /^\-?\d*\.?\d*$/.test(this.value) ? isNaN(d) || this.value == d || (this.value = d) : this.value = last[idToIndex(this.id)]
#     } else {
#         var d = Math.min(this.max, Math.max(this.value, this.min));
#         isNaN(d) || this.value.includes(".") || (this.value = d), /^\-?\d*\.?\d*$/.test(this.value) || (this.value = last[idToIndex(this.id)])
#     }
#     last[idToIndex(this.id)] = this.value;
#     var e = convert(),
#         f = document.getElementById("color_visualizer");
#     f.style.backgroundColor = "#" + e
# }

# function resetAll() {
#     var c, a = document.getElementById("mode").selectedIndex,
#         b = [document.getElementById("input0"), document.getElementById("input1"), document.getElementById("input2"), document.getElementById("input3")];
#     if (3 === a) b[0].value = "", last[0] = "";
#     else
#         for (c = 0; c < 4; c++) b[c].value = 0
# }

# function updateInputs() {
#     var c, a = document.getElementById("mode").selectedIndex,
#         b = [document.getElementById("input0"), document.getElementById("input1"), document.getElementById("input2"), document.getElementById("input3")];
#     switch (a) {
#         case 0:
#             document.getElementById("label0").innerHTML = "L* (0 to 100)", document.getElementById("label1").innerHTML = "a* (-128 to 128)", document.getElementById("label2").innerHTML = "b* (-128 to 128)", document.getElementById("label3").innerHTML = " ", b[1].style.visibility = "visible", b[2].style.visibility = "visible", b[3].style.visibility = "hidden", c = 3;
#             break;
#         case 1:
#             document.getElementById("label0").innerHTML = "R (0 to 255)", document.getElementById("label1").innerHTML = "G (0 to 255)", document.getElementById("label2").innerHTML = "B (0 to 255)", document.getElementById("label3").innerHTML = " ", b[1].style.visibility = "visible", b[2].style.visibility = "visible", b[3].style.visibility = "hidden", c = 3;
#             break;
#         case 2:
#             document.getElementById("label0").innerHTML = "C (0% to 100%)", document.getElementById("label1").innerHTML = "M (0% to 100%)", document.getElementById("label2").innerHTML = "Y (0% to 100%)", document.getElementById("label3").innerHTML = "K (0% to 100%)", b[1].style.visibility = "visible", b[2].style.visibility = "visible", b[3].style.visibility = "visible", c = 4;
#             break;
#         case 3:
#             document.getElementById("label0").innerHTML = "HEX (0 to F) (ex. 5F00AE)", document.getElementById("label1").innerHTML = " ", document.getElementById("label2").innerHTML = " ", document.getElementById("label3").innerHTML = " ", b[1].style.visibility = "hidden", b[2].style.visibility = "hidden", b[3].style.visibility = "hidden", c = 1;
#             break;
#         case 4:
#             document.getElementById("label0").innerHTML = "X", document.getElementById("label1").innerHTML = "Y", document.getElementById("label2").innerHTML = "Z", document.getElementById("label3").innerHTML = " ", b[1].style.visibility = "visible", b[2].style.visibility = "visible", b[3].style.visibility = "hidden", c = 3
#     }
#     var d;
#     if (a < 3)
#         for (d = 0; d < c; d += 1) b[d].min = limits[a][d][0], b[d].max = limits[a][d][1];
#     else 3 == a ? (b[0].min = 0, b[0].max = 16777215) : (b[0].min = 0, b[1].min = 0, b[2].min = 0, smallXyzMode ? (b[0].max = illuminants[illuminantIn][0], b[1].max = illuminants[illuminantIn][1], b[2].max = illuminants[illuminantIn][2]) : (b[0].max = 100 * illuminants[illuminantIn][0], b[1].max = 100 * illuminants[illuminantIn][1], b[2].max = 100 * illuminants[illuminantIn][2]));
#     resetAll()
# }

# function updateXyzMode() {
#     smallXyzMode = document.getElementById("smallXyzMode").checked, resetAll(), convert()
# }

# function updateIlluminantIn() {
#     illuminantIn = document.getElementById("illuminantIn").selectedIndex, convert()
# }

# function updateIlluminantOut() {
#     illuminantOut = document.getElementById("illuminantOut").selectedIndex, convert()
# }

def hexToRgb(a):
    b = [0,0,0]
    b[0] = a >> 16 & 255
    b[1] = a >> 8 & 255
    b[2] = 255 & a
    return b


def xyzToLab(a, b):
    c = 216 / 24389
    d = 24389 / 27
    e = []
    g = [0,0,0]
    i = []
    for h in range(3):
        i.append(a[h] / b[h])
        if i[h] > c:
            e.append(math.pow(i[h], 1 / 3))
        else: 
            e.append((d * i[h] + 16) / 116)
    g[0] = round(100 * (116 * e[1] - 16)) / 100 
    g[1] = round(500 * (e[0] - e[1]) * 100) / 100
    g[2] = round(200 * (e[1] - e[2]) * 100) / 100
    return g


def labToXyz(a, b):
    
    c = 216 / 24389
    d = 24389 / 27
    k = [0] * 3

    f = (a[0] + 16) / 116
    e = a[1] / 500 + f
    g = f - a[2] / 200
    if math.pow(e, 3) > c:
        h = math.pow(e, 3) 
    else: 
        h = (116 * e - 16) / d
    if a[0] > d * c:
        i = math.pow(f, 3) 
    else: 
        i = a[0] / d
    if math.pow(g, 3) > c:
        j = math.pow(g, 3) 
    else: 
        j = (116 * g - 16) / d
    k[0] = h * b[0]
    k[1] = i * b[1]
    k[2] = j * b[2]

    return k


# function radToDeg(a) {
#     return a / Math.PI * 180
# }

# function degToRad(a) {
#     return a * Math.PI / 180
# }

def matrixVectorProduct(a, b):
    c = len(b)
    d = [0] * 3
    g = []
    if (len(a[0]) != c):
        return "Error computing matrix vector products"
    for e in range(c):
        for f in range(c):
            d[e] += a[e][f] * b[f]
    return d


def adaptXyz(a, b, c): 
    return matrixVectorProduct(bradfordTransform(b, c), a)

def matrixMultiply3x3(a, b):
    c = [[],[],[]]
    for d in range(3):
        c[d] = [0,0,0]
    for d in range(3):
        for e in range(3):
            for f in range(3):
                c[d][e] += a[d][f] * b[f][e]
    return c


def matrixInvert3x3(a):
    c = [[],[],[]]
    for d in range(3):
        c[d] = [0,0,0]
    c[0][0] = a[1][1] * a[2][2] - a[1][2] * a[2][1]
    c[1][0] = -1 * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
    c[2][0] = a[1][0] * a[2][1] - a[1][1] * a[2][0]
    c[0][1] = -1 * (a[0][1] * a[2][2] - a[0][2] * a[2][1])
    c[1][1] = a[0][0] * a[2][2] - a[0][2] * a[2][0]
    c[2][1] = -1 * (a[0][0] * a[2][1] - a[0][1] * a[2][0])
    c[0][2] = a[0][1] * a[1][2] - a[0][2] * a[1][1]
    c[1][2] = -1 * (a[0][0] * a[1][2] - a[0][2] * a[1][0])
    c[2][2] = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    b = a[0][0] * c[0][0] + a[0][1] * c[1][0] + a[0][2] * c[2][0]
    for d in range(3):
        for e in range(3):
            c[d][e] = c[d][e] / b
    return c


def bradfordTransform(a, b):
    c = [
        [0.8951, 0.2664, -0.1614],
        [-0.7502, 1.7135, 0.0367],
        [0.0389, -0.0685, 1.0296]
    ]
    d = []
    e = []
    f = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    d = matrixVectorProduct(c, a)
    e = matrixVectorProduct(c, b) 
    for g in range(3):
        f[g][g] = e[g] / d[g]
    return matrixMultiply3x3(matrixMultiply3x3(matrixInvert3x3(c), f), c)



def xyzChromaticity(a):
    b = [0,0]
    b[0] = a[0] / (a[0] + a[1] + a[2])
    b[1] = a[1] / (a[0] + a[1] + a[2])
    return b


def rgbMatrix(a, b, c, d):
    e = [[],[],[]]
    f = [[],[],[]]
    g = [0,0,0]
    for h in range(3):
        e[h] = [0,0,0]
        f[h] = [0,0,0]
    f[0][0] = a[0] / a[1]
    f[1][0] = 1
    f[2][0] = (1 - a[0] - a[1]) / a[1]
    f[0][1] = b[0] / b[1]
    f[1][1] = 1
    f[2][1] = (1 - b[0] - b[1]) / b[1]
    f[0][2] = c[0] / c[1]
    f[1][2] = 1
    f[2][2] = (1 - c[0] - c[1]) / c[1]
    g[0] = d[0] / d[1]
    g[1] = 1
    g[2] = (1 - d[0] - d[1]) / d[1]
    j = matrixVectorProduct(matrixInvert3x3(f), g)
    for h in range(3):
        for i in range(3):
            e[h][i] = j[i] * f[h][i]
    return e

def xyzToRgb(a, b, c, d, e, f):
    g = [0,0,0]
    g[0] = f[0] / f[1]
    g[1] = 1
    g[2] = (1 - f[0] - f[1]) / f[1]
    h = adaptXyz(a, b, g)   
    i = matrixInvert3x3(rgbMatrix(c, d, e, f))
    return matrixVectorProduct(i, h)


def rgbToXyz(a, b, c, d, e, f):
    g = [0,0,0]
    g[0] = e[0] / e[1]
    g[1] = 1
    g[2] = (1 - e[0] - e[1]) / e[1]
    h = rgbMatrix(b, c, d, e)   
    i = matrixVectorProduct(h, a)
    return adaptXyz(i, g, f)


def xyzTosRGB(a, b):
    c = [0,0,0]
    d = [0.64, 0.33]
    e = [0.3, 0.6]
    f = [0.15, 0.06]
    g = [0.95047, 1, 1.08883]
    i = xyzToRgb(a, b, d, e, f, xyzChromaticity(g))
    for h in range(3):
        if i[h] > 0.0031308:    # ??
            i[h] = 1.055 * math.pow(i[h], 1 / 2.4) - 0.055
        else: 
            i[h] = 12.92 * i[h]
        i[h] = 255 * i[h] + 0.5
        if i[h] < 0:
            i[h] = 0 
        elif i[h] > 255:
            i[h] = 255 
        c[h] = i[h]
    for h in range(3):
        c[h] = math.floor(c[h])
    return c


def sRGBtoXYZ(a, b):
    c = [0,0,0]
    d = [0.64, 0.33]
    e = [0.3, 0.6]
    f = [0.15, 0.06]
    g = [0.95047, 1, 1.08883]
    for h in range(3):
        c[h] = a[h] / 255
        if c[h] > 0.04045:
            c[h] = math.pow((c[h] + 0.055) / 1.055, 2.4)
        else: 
            c[h] = c[h] / 12.92
    return rgbToXyz(c, d, e, f, xyzChromaticity(g), b)

def i3Dto1D(a, b, c, d, e, f):
    return c + b * e + a * e * f


def xyzToCMYK(a, b, c):
    d = [0,0,0,0]
    e = [16, 0, 0]
    f = [0.9642, 1, 0.82491]
    h = profile.b2a1_input_curves
    i = profile.b2a1_clut
    j = profile.b2a1_output_curves
    k = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
    ]
    a = adaptXyz(a, b, f)   
    if (c):
        l = [0, 0, 0]
        m = labToXyz(e, f)
        n = (1 - m[1]) / (1 - l[1])
        o = 1 - n
        for g in range(3):
            a[g] = a[g] * n + o * f[g]

    
    p = xyzToLab(a, f)
    p = matrixVectorProduct(k, p)

    if p[0] < 0:
        p[0] = 0 
    elif p[0] > 100:
        p[0] = 100 
    else: 
        p[0] = p[0]
    p[0] = 255 * p[0] / 100
    if p[1] < -128:
        p[1] = -128 
    elif p[1] > 128:
        p[1] = 128 
    else: 
        p[1]
    p[1] = 255 * (p[1] + 128) / 256
    if p[2] < -128:
        p[2] = -128
    elif p[2] > 128:
        p[2] = 128 
    else: 
        p[2]
    p[2] = 255 * (p[2] + 128) / 256
    
    for q in range(3):
        r = math.floor(p[q])
        s = math.ceil(p[q])
        t = p[q] - r
        p[q] = h[r][q + 1] * (1 - t) + h[s][q + 1] * t
        p[q] = 32 * p[q] / 255
    
    u = math.floor(p[0])
    v = math.floor(p[1])
    w = math.floor(p[2])
    x = math.ceil(p[0])
    y = math.ceil(p[1])
    z = math.ceil(p[2])
    
    A = p[0] - u
    B = p[1] - v
    C = p[2] - w
    D = i3Dto1D(u, v, w, 33, 33, 33)
    E = i3Dto1D(x, v, w, 33, 33, 33)
    F = i3Dto1D(u, y, w, 33, 33, 33)
    G = i3Dto1D(x, y, w, 33, 33, 33)
    H = i3Dto1D(u, v, z, 33, 33, 33)
    I = i3Dto1D(x, v, z, 33, 33, 33)
    J = i3Dto1D(u, y, z, 33, 33, 33)
    K = i3Dto1D(x, y, z, 33, 33, 33)
    for q in range(4):
        L = i[D][q + 1] * (1 - A) + i[E][q + 1] * A
        M = i[F][q + 1] * (1 - A) + i[G][q + 1] * A
        N = i[H][q + 1] * (1 - A) + i[I][q + 1] * A
        O = i[J][q + 1] * (1 - A) + i[K][q + 1] * A
        P = L * (1 - B) + M * B
        Q = N * (1 - B) + O * B
        d[q] = P * (1 - C) + Q * C
    for q in range(4):
        r = math.floor(d[q])
        s = math.ceil(d[q])
        t = d[q] - r
        d[q] = j[r][q + 1] * (1 - t) + j[s][q + 1] * t
        d[q] = round(d[q] / 255 * 100)
    
    return d


def i4Dto1D(a, b, c, d, e, f, g, h):
    return d + c * e + b * e * g + a * e * f * g


def cmykToXyz(a, b, c):
    d = [0,0,0]
    e = [0,0,0,0]
    f = [16, 0, 0]
    g = [0.9642, 1, 0.82491]
    i = profile.a2b1_input_curves
    j = profile.a2b1_clut
    for h in range(4):
        e[h] = 255 * a[h]
        k = math.floor(e[h])
        l = math.ceil(e[h])
        m = e[h] - k
        e[h] = i[k][h + 1] * (1 - m) + i[l][h + 1] * m
        e[h] = 8 * e[h] / 65535
    
    n = math.floor(e[0])
    o = math.floor(e[1])
    p = math.floor(e[2])
    q = math.floor(e[3])
    r = math.ceil(e[0])
    s = math.ceil(e[1])
    t = math.ceil(e[2])
    u = math.ceil(e[3])
    
    v = e[0] - n
    w = e[1] - o
    x = e[2] - p
    y = e[3] - q
    
    z = i4Dto1D(n, o, p, q, 9, 9, 9, 9)
    A = i4Dto1D(r, o, p, q, 9, 9, 9, 9)
    B = i4Dto1D(n, s, p, q, 9, 9, 9, 9)
    C = i4Dto1D(r, s, p, q, 9, 9, 9, 9)
    D = i4Dto1D(n, o, t, q, 9, 9, 9, 9)
    E = i4Dto1D(r, o, t, q, 9, 9, 9, 9)
    F = i4Dto1D(n, s, t, q, 9, 9, 9, 9)
    G = i4Dto1D(r, s, t, q, 9, 9, 9, 9)
    H = i4Dto1D(n, o, p, u, 9, 9, 9, 9)
    I = i4Dto1D(r, o, p, u, 9, 9, 9, 9)
    J = i4Dto1D(n, s, p, u, 9, 9, 9, 9)
    K = i4Dto1D(r, s, p, u, 9, 9, 9, 9)
    L = i4Dto1D(n, o, t, u, 9, 9, 9, 9)
    M = i4Dto1D(r, o, t, u, 9, 9, 9, 9)
    N = i4Dto1D(n, s, t, u, 9, 9, 9, 9)
    O = i4Dto1D(r, s, t, u, 9, 9, 9, 9)
    for h in range(3):
        
        P = j[z][h + 1] * (1 - v) + j[A][h + 1] * v
        Q = j[B][h + 1] * (1 - v) + j[C][h + 1] * v
        R = j[D][h + 1] * (1 - v) + j[E][h + 1] * v
        S = j[F][h + 1] * (1 - v) + j[G][h + 1] * v
        T = j[H][h + 1] * (1 - v) + j[I][h + 1] * v
        U = j[J][h + 1] * (1 - v) + j[K][h + 1] * v
        V = j[L][h + 1] * (1 - v) + j[M][h + 1] * v
        W = j[N][h + 1] * (1 - v) + j[O][h + 1] * v
        X = P * (1 - w) + Q * w
        Y = R * (1 - w) + S * w
        Z = T * (1 - w) + U * w
        qq = V * (1 - w) + W * w
        ww = X * (1 - x) + Y * x
        aa = Z * (1 - x) + qq * x
        d[h] = ww * (1 - y) + aa * y
    
    d[0] = 100 * d[0] / 65535
    d[1] = 256 * d[1] / 65535 - 128
    d[2] = 256 * d[2] / 65535 - 128

    ba = labToXyz(d, g)
    if (c):
        ca = [0, 0, 0]
        da = labToXyz(f, g)
        ea = (1 - ca[1]) / (1 - da[1])
        fa = 1 - ea
        for ga in range(3):
            ba[ga] = ba[ga] * ea + fa * g[ga]
        
    return adaptXyz(ba, g, b)


