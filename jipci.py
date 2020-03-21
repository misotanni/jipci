import math

class incorrect_syntax(Exception): pass
class limit_bj(Exception): pass
class limit_he(Exception): pass
class unknown_input(Exception): pass
class unknown_output(Exception): pass
class wrong_format_bj(Exception): pass
class wrong_format_color(Exception): pass
class wrong_format_fjs(Exception): pass
class wrong_format_he(Exception): pass
class wrong_format_monzo(Exception): pass
class wrong_format_ratio(Exception): pass
class wrong_interval(Exception): pass
class zero_ratio(Exception): pass

# special auxiliary functions

def accidentals_bj(b, n): # lookup table for Ben Johnston accidentals
	o = ["", None, None, "7", "^", "13", "17", "19", "23", "29", "31"]
	u = ["", None, None, "L", "v", "-13", "-17", "-19", "-23", "-29", "-31"]
	if b: return o[n]
	else: return u[n]

def accidentals_he(n): # lookup table for Helmholtz-Ellis accidentals
	i = ["", None, "5", "7", "11", "13", "17", "19", "23", "29", "31", r"{17}", r"{5}", r"{23}", r"{49}", r"{29}", r"{13}", r"{7}"]
	return i[n]

def color_prime(n, b): # irregular prime colors
	o = [None, None, "y", "z", "1o", "3o"]
	u = [None, None, "g", "r", "1u", "3u"]
	if b: return o[n]
	else: return u[n]

def color_mapping(p): # "pseudo-edomapping" for primes in color notation
	g = math.log2(p)
	u = 0
	while g >= 1:
		g -= 1
		u += 7
	g = int(g*24)
	i = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7]
	return i[g] + u

def commas_bj(n): # lookup table for Ben Johnston commas
# format: otonal comma monzo minus focus prime
	i = [None, None]
	i.append([4, -4])   # 5
	i.append([-2, -2, 1])  # 7
	i.append([-5, 1, 0])   # 11
	i.append([-6, 0, 1])   # 13
	i.append([-1, 1, -2])  # 17
	i.append([-5, -1, 1])  # 19
	i.append([1, -2, -1])  # 23
	i.append([-4, -2, 1])  # 29
	i.append([-1, -1, -1]) # 31
	return i[n]

def commas_he(n): # lookup table for Helmholtz-Ellis commas
# format: otonal comma monzo minus focus prime
	i = [None, None]
	i.append([4, -4])           # 5
	i.append([-6, 2])           # 7
	i.append([-5, 1])           # 11
	i.append([1, -3])           # 13
	i.append([-8, 1, 1])        # 17
	i.append([-9, 3])           # 19
	i.append([5, -6])           # 23
	i.append([-4, -2, 1])       # 29
	i.append([-10, 1, 0, 0, 1]) # 31
	i.append([3, -3, 0, 0, -1]) # 37
	i.append([1, -4])           # 41
	i.append([-7, 1])           # 43
	i.append([4, -6])           # 47
	i.append([-5, 1, -1])       # 53
	i.append([-9, 2])           # 59
	i.append([-2, -1, -1])      # 61
	return i[n]

def fjs(n): # FJS master algorithm
	if n == 3: return [-19, 12] # Pythagorean comma special case
	l = math.log2(65/63) # (octave size of) radius of tolerance
	k = 0
	while True:
		c = math.log2(n/(3**k))
		while c >= 0.5: c -= 1
		while c < -0.5: c += 1
		if abs(c) < l: # found k = fifth shift
			g = -k * math.log2(3)
			p = math.log2(n)
			o = 0
			while o + p + g >= 0.5: o -= 1
			while o + p + g < -0.5: o += 1
			return [o, -k] # formal comma minus focus prime, in monzo form
		if k > 0: k = -k
		else: k = -k+1

def intervals_diatonic(n): # circle of diatonic fifths to stepspan
	i = [0, 4, 1, 5, 2, 6, 3]
	return i[n]

def intervals_letters(n): # musical alphabet
	i = ["C", "D", "E", "F", "G", "A", "B"]
	return i[n]

def intervals_monzos(n): # monzos of P1, M2, M3, P4, P5, M6, M7
	i = [[0, 0], [-3, 2], [-6, 4], [2, -1], [-1, 1], [-4, 3], [-7, 5]]
	return i[n]

def intervals_perfect(n): # whether the interval has a perfect variant
	i = [True, False, False, True, True, False, False]
	return i[n]

def matrix_bj(n, m): # Ben Johnston matrix of pluses and minuses; n = letter, m = stepspan
	i = []
#	          1   2   3   4   5   6   7
	i.append([0,  0,  1,  0,  0,  1,  1]) # C
	i.append([0,  1,  2,  0,  1,  1,  2]) # D
	i.append([0,  1,  1,  0,  0,  1,  1]) # E
	i.append([0,  0,  1, -1,  0,  0,  1]) # F
	i.append([0,  1,  1,  0,  0,  1,  2]) # G
	i.append([0,  0,  1, -1,  0,  1,  1]) # A
	i.append([0,  1,  1,  0,  1,  1,  2]) # B
	return i[n][m]

def polarity_he(n): # Helmholtz-Ellis comma polarities
	i = [None, None, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1]
	return i[n]

def pyth_split(s): # split general EJI interval into Pythagorean part and remainder
	j = False
	for i in s:
		if i.isnumeric():
			j = True
			break
	if not j: raise wrong_interval
	i = 0
	while not s[i].isnumeric(): i += 1
	i += 1
	return [s[:i], s[i:]]

# output-only systems

def size(l, u): # list to size in cents or millioctaves; u = 1200 for cents, u = 1000 for millioctaves
	a = []
	p = 2
	c = 0
	while len(a) < len(l):
		a.append(u * math.log2(p))
		while True:
			if p == 2: p += 1
			else: p += 2
			j = True
			for z in range(2, int(math.sqrt(p))+1):
				if p % z == 0: j = False
			if j: break
	for i in range(len(l)):
		c += a[i] * l[i]
	return round(c, 4)

# general EJI conversion functions

def pyth_to_staff(l): # Pythagorean list to conventional interval class
	while len(l) < 2: l.append(0)
	o, a, c = 0, 0, l[1]
	while c < -1 or c > 5:
		if c < -1:
			c += 7
			a -= 1
		if c > 5:
			c -= 7
			a += 1
	c = intervals_diatonic(c)
	if a > 0: ad = a * "A"
	elif intervals_perfect(c):
		if a == 0: ad = "P"
		else: ad = -a * "d"
	else:
		if a == 0: ad = "M"
		elif a == -1: ad = "m"
		else: ad = (-a-1) * "d"
	t = intervals_monzos(c)[0] - 11 * a
	while l[0] != t:
		if l[0] < t:
			l[0] += 1
			o -= 1
		if l[0] > t:
			l[0] -= 1
			o += 1
	v = False
	if c == 0 and a < 0: v = True  # special "d1" to "-cd8" case
	if c == 0 and a == 0 and o == 1: v = True # special "cP1" to "P8" case
	o -= v
	if o < 0: od = "-"
	else: od = ""
	od += abs(o) * "c"
	o += v
	f = od + ad + str(1+c+7*v)
	return [f, a, c] # f = string form, a, c = raw form (accidentals & stepspan)

def staff_to_pyth(s): # conventional interval class to Pythagorean list
	variants = ["d", "m", "P", "M", "A"]
	l = 0
	j = False
	for i in s:
		if i in variants:
			j = True
			break
	if not j: raise wrong_interval
	while s[l] not in variants: l += 1
	q = s[:l]
	s = s[l:]
	if "-" in q and "c" not in q: raise wrong_interval
	v = False
	if len(q) > 0:
		if q[0] == "-":
			v = True
			q = q[1:]
	for i in q:
		if i != "c": raise wrong_interval
	o = len(q)
	if v: o = -o
	l = 0
	j = False
	for i in s:
		if i.isnumeric():
			j = True
			break
	if not j: raise wrong_interval
	while not s[l].isnumeric(): l += 1
	q = s[:l]
	s = s[l:]
	if len(q) != 1:
		if q[0] not in ["d", "A"]: raise wrong_interval
		for ia in q:
			for ib in q:
				if ia != ib: raise wrong_interval
		if q[0] == "d": a = -len(q)
		else: a = len(q)
	else:
		if q[0] == "A": a = 1
		elif q[0] == "d": a = -1
		elif q[0] == "m": a = -0.5
		else: a = 0
	for i in s:
		if not i.isnumeric(): raise wrong_interval
	c = int(s)
	if c == 0: raise wrong_interval
	while c > 7:
		c -= 7
		o += 1
	c -= 1
	if intervals_perfect(c) and q[0] in ["M", "m"]: raise wrong_interval
	if not intervals_perfect(c) and q[0] == "P": raise wrong_interval
	if not intervals_perfect(c):
		if a < -0.5: a -= 1
		if a == -0.5: a = -1
	f = intervals_monzos(c)
	f[0] += o
	f[0] += -11 * a
	f[1] += 7 * a
	return [f, a, c] # f = list form, a, c = raw form (accidentals & stepspan)

# bidirectional systems: conversion functions from X to list

def from_bj(s): # Ben Johnston to list
	q = pyth_split(s)
	s = q[1]
	q = q[0]
	x = staff_to_pyth(q)
	z = x[0]
	while len(z) < 11: z.append(0)
	if s.count("(") != 1 or s.count(")") != 1 or s[len(s)-1] != ")": raise wrong_format_bj
	if s[0] not in [",", "("]: raise wrong_format_bj
	a = []
	i = 0
	while True:
		if s[i] == "(": break
		else:
			i += 1
			ia = i
			while s[i] not in [",", "("]: i += 1
			ib = i
			a.append(s[ia:ib])
	s = s[i+1:]
	for i in a:
		j = False
		for k in range(2, 11):
			for r in [True, False]:
				if i == accidentals_bj(r, k):
					j = True
					if r: v = 1
					else: v = -1
					for h in range(len(commas_bj(k))):
						z[h] += v * commas_bj(k)[h]
					z[k] += v
					break
		if not j: raise wrong_format_bj
	j = False
	for i in range(7):
		if s[0] in [intervals_letters(i), intervals_letters(i).lower()]:
			j = True
			n = i
	if not j: raise wrong_format_bj
	i = 1
	w = 0
	while True:
		if s[i] == ")": break
		if s[i] not in ["+", "-"]: raise wrong_format_bj
		if s[i] == "+": w += 1
		else: w -= 1
		i += 1
	g = matrix_bj(n, x[2]) + 2*x[1] - w
	z[0] += 4 * g
	z[1] -= 4 * g
	z[2] += g
	for i in range(len(z)-1, -1, -1):
		if z[i] != 0: break
		z = z[:(len(z)-1)]
	return z

def from_color(s): # color notation to list
	i = 0
	h = [7, 11, 16, 20, 24, 26]
	pq = s.count("p") - s.count("q")
	for v in ["p", "q"]: s = s.replace(v, "")
	while s[i] in ["-", "c"]: i += 1
	q = s[:i]
	s = s[i:]
	v = False
	if len(q) > 0:
		if q[0] == "-":
			v = True
			q = q[1:]
	for i in q:
		if i != "c": raise wrong_format_color
	o = len(q)
	if v: o = -o
	i = 0
	while s[i] in ["s", "L"]: i += 1
	q = s[:i]
	s = s[i:]
	if s.isnumeric(): raise wrong_format_color
	v = False
	if len(q) > 0:
		if q[0] == "s": v = True
	for i in q:
		if (v and (i != "s")) or (not v and (i != "L")): raise wrong_format_color
	m = len(q)
	if v: m = -m
	i = len(s) - 1
	if i == -1: raise wrong_format_color
	if not s[i].isnumeric(): raise wrong_format_color
	while s[i].isnumeric(): i -= 1
	i += 1
	c = int(s[i:]) - 1
	s = s[:i]
	if s == "": raise wrong_format_color
	if len(s) > 1 and "w" in s: raise wrong_format_color
	if s == "w": s = ""
	w = [2, 3, 5, 7, 11, 13]
	p = 17
	a = [0, 0, 0, 0, 0, 0]
	for i in range(2, 4): a[i] = s.count(color_prime(i, True)) - s.count(color_prime(i, False))
	for v in ["y", "g", "z", "r"]: s = s.replace(v, "")
	s += "!"
	i = 0
	ia = i
	while s[i] != "!":
		while s[i] not in ["o", "u"]:
			i += 1
		i += 1
		ib = i
		t = s[ia:ib]
		if t[len(t)-1] == "o": v = 1
		else: v = -1
		t = t[:len(t)-1]
		if not t.isnumeric(): print(t)
		t = int(t)
		if t == 1: a[4] += v
		elif t == 3: a[5] += v
		elif t < 17: raise wrong_format_color
		else:
			for k in range(2, int(math.sqrt(t))+1):
				if t % k == 0: raise wrong_format_color
			j = True
			while p <= t or not j:
				w.append(p)
				a.append(0)
				while True:
					p += 2
					j = True
					for z in range(2, int(math.sqrt(p))+1):
						if p % z == 0: j = False
					if j: break
			k = 0
			while w[k] != t: k += 1
			a[k] += v
		ia = i
	while len(h) < len(a): h.append(color_mapping(w[len(h)]))
	x = 0
	for i in range(len(a)):
		x += a[i] * h[i]
	a[1] = (2*c - 2*x + 3) % 7 + 7*m - 3
	a[0] = (c - x - 11*a[1]) // 7
	a[1] += 12 * pq
	a[0] += o - 19 * pq
	return a

def from_fjs(s): # FJS to list
	q = pyth_split(s)
	s = q[1]
	q = q[0]
	x = staff_to_pyth(q)[0]
	for i in range(len(s)-1):
		if s[i] == "," and not (s[i-1].isnumeric() and s[i+1].isnumeric()): raise wrong_format_fjs
	s += ",!"
	if s[0] not in ["^", "_", "!"]: raise wrong_format_fjs
	if s.count("^") > 1 or s.count("_") > 1 or s.count("!") > 1 or "^_" in s: raise wrong_format_fjs
	to, tu = 1, 1
	i = 0
	if s[i] == "^":
		i += 1
		ia = i
		while s[i] not in ["_", "!"]:
			i += 1
			if s[i] in [",", "_", "!"]:
				ib = i
				to *= int(s[ia:ib])
				if s[i] == ",":
					i += 1
					ia = i
	if s[i] == "_":
		i += 1
		ia = i
		while s[i] != "!":
			i += 1
			if s[i] in [",", "!"]:
				ib = i
				tu *= int(s[ia:ib])
				if s[i] == ",":
					i += 1
					ia = i
	w = []
	co, cu, c = [], [], []
	n, p = 0, 2
	if to < 1 or tu < 1: raise wrong_format_fjs
	while to > 1 or tu > 1:
		w.append(p)
		co.append(0)
		cu.append(0)
		while to % p == 0:
			to /= p
			co[n] += 1
		while tu % p == 0:
			tu /= p
			cu[n] += 1
		n += 1
		while True:
			if p == 2: p += 1
			else: p += 2
			j = True
			for z in range(2, int(math.sqrt(p))+1):
				if p % z == 0: j = False
			if j: break
	cl = max(len(co), len(cu))
	while len(c) < cl: c.append(0)
	for i in range(len(co)):
		if co[i] != 0: c[i] += co[i]
	for i in range(len(cu)):
		if cu[i] != 0: c[i] += -cu[i]
	if c == []: return x
	while len(c) < 2: c.append(0)
	if c[0] != 0: raise wrong_format_fjs
	for i in range(1, len(c)):
		f = fjs(w[i])
		for k in range(2):
			x[k] += f[k] * c[i]
	c = c[2:]
	x += c
	return x

def from_he(s): # Helmholtz-Ellis to list
	q = pyth_split(s)
	s = q[1]
	q = q[0]
	z = staff_to_pyth(q)[0]
	while len(z) < 18: z.append(0)
	s += "!"
	a = []
	i = 0
	while True:
		if s[i] == "!": break
		elif s[i] not in ["+", "-"]: raise wrong_format_he
		else:
			ia = i
			i += 1
			while s[i] not in ["+", "-", "!"]: i += 1
			ib = i
			a.append(s[ia:ib])
	for i in a:
		if (i[0] not in ["+", "-"]) or len(i) < 2: raise wrong_format_he
		if i[0] == "-": v = -1
		else: v = 1
		i = i[1:]
		j = False
		for k in range(2, 18):
			if i == accidentals_he(k):
				j = True
				v *= polarity_he(k)
				for h in range(len(commas_he(k))):
					z[h] += v * commas_he(k)[h]
				z[k] += v
				break
		if not j: raise wrong_format_he
	for i in range(len(z)-1, -1, -1):
		if z[i] != 0: break
		z = z[:(len(z)-1)]
	return z

def from_monzo(s): # monzo to list
	if s.count("[") != 1 or s.count("]") != 1 or s[0] != "[" or s[len(s)-1] != "]" or ",," in s or ",]" in s or "-," in s or "-]" in s: raise wrong_format_monzo
	xl = []
	if s == "[]": return xl
	else:
		l = 0
		while s[l] != "]":
			l += 1
			n = l
			if s[n] == "-": n += 1
			while s[n].isnumeric(): n += 1
			if s[n] not in ["]", ","]: raise wrong_format_monzo
			xl.append(int(s[l:n]))
			l = n
		return xl

def from_ratio(s): # ratio to list
	if "/" not in s: raise wrong_format_ratio
	for l in range(len(s)):
		if s[l] == "/":
			num, den = s[:l], s[l+1:]
			if not num.isnumeric() or not den.isnumeric(): raise wrong_format_ratio
			break
	o, u = int(num), int(den)
	if o == 0 or u == 0: raise zero_ratio
	g = math.gcd(o, u)
	o, u = o/g, u/g
	ol, ul, xl = [], [], []
	sr = [o, u]
	sl = [ol, ul]
	for i in range(2):
		si = sr[i]
		so = sl[i]
		n, p = 0, 2
		while si > 1:
			so.append(0)
			while si % p == 0:
				si /= p
				so[n] += 1
			n += 1
			while True:
				if p == 2: p += 1
				else: p += 2
				j = True
				for z in range(2, int(math.sqrt(p))+1):
					if p % z == 0: j = False
				if j: break
	ol, ul = sl[0], sl[1]
	m = max(len(ol), len(ul))
	while len(ol) < m: ol.append(0)
	while len(ul) < m: ul.append(0)
	for i in range(m):
		if ol[i] == 0 and ul[i] == 0: xl.append(0)
		elif ol[i] != 0: xl.append(ol[i])
		elif ul[i] != 0: xl.append(-ul[i])
	return xl

# bidirectional systems: conversion functions from list to X

def to_bj(l): # list to Ben Johnston
	w = len(l)
	if w > 11: raise limit_bj
	a = [None, None]
	for n in range(9): a.append(0)
	for n in range(w-1, 1, -1):
		q = commas_bj(n)
		while l[n] != 0:
			if l[n] > 0:
				l[n] -= 1
				for k in range(len(q)): l[k] -= q[k]
				a[n] += 1
			if l[n] < 0:
				l[n] += 1
				for k in range(len(q)): l[k] += q[k]
				a[n] -= 1
	b = l[:2]
	t = pyth_to_staff(b)
	d = []
	for n in range(7): d.append(a[2] - 2*t[1] - matrix_bj(n, t[2]))
	s = t[0]
	for n in range(3, 11):
		c = (a[n] > 0)
		m = ","
		m += accidentals_bj(c, n)
		m *= abs(a[n])
		s += m
	s += "("
	for n in range(7):
		if d[n] != 0:
			if s[len(s)-1] in ["+", "-"]: s += ","
			s += intervals_letters(n)
		if d[n] > 0: s += d[n] * "-"
		elif d[n] < 0: s += -d[n] * "+"
	s += ")"
	return s

def to_color(l): # list to color notation
	s = ""
	while len(l) < 2: l.append(0)
	p = 17
	w = [None, None, None, None, None, None]
	v = [7, 11, 16, 20, 24, 26]
	if len(l) >= 7:
		for n in range(6, len(l)):
			w.append(p)
			v.append(color_mapping(p))
			if len(w) == len(l): break
			while True:
				p += 2
				j = True
				for z in range(2, int(math.sqrt(p))+1):
					if p % z == 0: j = False
				if j: break
	for i in range(len(l)-1, 1, -1):
		if l[i] != 0:
			if i >= 6:
				ss = str(w[i])
				if l[i] > 0: ss += "o"
				else: ss += "u"
				s += abs(l[i]) * ss
			else:
				e = (l[i] > 0) - (l[i] < 0)
				s += abs(l[i]) * color_prime(i, e)
	if s == "": s = "w"
	u, o, a = 0, 0, 0
	for i in range(len(l)): u += v[i] * l[i]
	if u != 7:
		while u > 6: # u = 7 (octave) is allowed
			u -= 7
			o += 1
	while u < 0:
		u += 7
		o -= 1
	for i in range(1, len(l)): a += l[i]
	a = round(a/7)
	if o < 0: x = "-" + (-o) * "c"
	elif o > 0: x = o * "c"
	else: x = ""
	if a < 0: x += (-a) * "s"
	elif a > 0: x += a * "L"
	x += s
	x += str(u+1)
	return x

def to_fjs(l): # list to FJS
	while len(l) < 2: l.append(0)
	q = l[:2]
	l = l[2:]
	n, p = 0, 5
	a = []
	while n < len(l):
		b = fjs(p)
		for i in range(2): q[i] -= l[n] * b[i]
		a.append(p)
		n += 1
		while True:
			p += 2
			j = True
			for z in range(2, int(math.sqrt(p))+1):
				if p % z == 0: j = False
			if j: break
	x = pyth_to_staff(q)[0]
	j = False
	i = 0
	while i < len(l):
		if l[i] > 0:
			j = True
			x += "^"
			break
		else: i += 1
	if j:
		while i < len(l):
			if l[i] > 0:
				if not x[len(x)-1] == "^": x += ","
				d = str(a[i])
				x += d
				x += (l[i]-1) * ("," + d)
			i += 1
	j = False
	i = 0
	while i < len(l):
		if l[i] < 0:
			j = True
			x += "_"
			break
		else: i += 1
	if j:
		while i < len(l):
			if l[i] < 0:
				if not x[len(x)-1] == "_": x += ","
				x += str(a[i])
			i += 1
	return x

def to_he(l): # list to Helmholtz-Ellis
	w = len(l)
	if w > 18: raise limit_he
	a = [None, None]
	for n in range(16): a.append(0)
	for n in range(w-1, 1, -1):
		q = commas_he(n)
		while l[n] != 0:
			if l[n] > 0:
				l[n] -= 1
				for k in range(len(q)): l[k] -= q[k]
				a[n] += 1
			if l[n] < 0:
				l[n] += 1
				for k in range(len(q)): l[k] += q[k]
				a[n] -= 1
	b = l[:2]
	s = pyth_to_staff(b)[0]
	for n in range(2, 18):
		c = ((a[n] > 0) - (a[n] < 0))
		v = polarity_he(n) * c
		if v == 1: m = "+"
		else: m = "-"
		m += accidentals_he(n)
		m *= abs(a[n])
		s += m
	return s

def to_monzo(l): # list to monzo
	s = ""
	for i in l:
		s += ","
		s += str(i)
	s = s[1:]
	s = "[" + s
	i = len(s)
	while s[i-1] == "0":
		s = s[:(i-2)]
		i -= 2
	s = s + "]"
	return s

def to_ratio(l): # list to ratio
	o, u = 1, 1
	n, p = 0, 2
	while n < len(l):
		if l[n] > 0: o *= (p ** l[n])
		elif l[n] < 0: u *= (p ** -l[n])
		n += 1
		while True:
			if p == 2: p += 1
			else: p += 2
			j = True
			for z in range(2, int(math.sqrt(p))+1):
				if p % z == 0: j = False
			if j: break
	s = str(o) + "/" + str(u)
	return s

# main

try:
	r = input("Enter conversion command.\n")
	i = r + " "
	if (i.count(" ") != 3): raise incorrect_syntax
	for n in range(3):
		for l in range(len(i)):
			if i[l] == " ":
				o, i = i[:l], i[l+1:]
				if n == 0: oc = o
				elif n == 1: ic = o
				elif n == 2: ix = o
				break
# convert input to list: bidirectional systems
	if ic == "bj": s = from_bj(ix)
	elif ic == "color": s = from_color(ix)
	elif ic == "fjs": s = from_fjs(ix)
	elif ic == "he": s = from_he(ix)
	elif ic == "monzo": s = from_monzo(ix)
	elif ic == "ratio": s = from_ratio(ix)
	else: raise unknown_input
# convert list to output: bidirectional systems
	if oc == "bj": u = to_bj(s)
	elif oc == "color": u = to_color(s)
	elif oc == "fjs": u = to_fjs(s)
	elif oc == "he": u = to_he(s)
	elif oc == "monzo": u = to_monzo(s)
	elif oc == "ratio": u = to_ratio(s)
# convert list to output: output-only systems
	elif oc == "cents": u = size(s, 1200)
	elif oc == "mo": u = size(s, 1000)
	else: raise unknown_output
# done
	print(u)
# errors
except incorrect_syntax: print("Error: Incorrect syntax.")
except limit_bj: print("Error: Input interval is above Ben Johnston's 31-limit restriction.")
except limit_he: print("Error: Input interval is above Helmholtz-Ellis's 61-limit restriction.")
except unknown_input: print("Error: Input format \"%s\" not recognized." % ic)
except unknown_output: print("Error: Output format \"%s\" not recognized." % oc)
except wrong_format_bj: print("Error: Input not in Ben Johnston format.")
except wrong_format_color: print("Error: Input not in color notation format.")
except wrong_format_fjs: print("Error: Input not in FJS format.")
except wrong_format_he: print("Error: Input not in Helmholtz-Ellis format.")
except wrong_format_monzo: print("Error: Input is not a monzo.")
except wrong_format_ratio: print("Error: Input is not a ratio.")
except wrong_interval: print("Error: Incorrect form of Pythagorean interval.")
except zero_ratio: print("Error: Zero makes no sense in ratios.")