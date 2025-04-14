function encrypt(G, H) {
	H = H || "cdababcddcba";

	function I(L, M, N) {
		if (L === '') {
			return '';
		}
		var O = ['a', 'b', 'c', 'd', 'h', 'i', 'j', 'k', 'x', 'y'].join('');
		var P = parseInt(L.length / M);
		var Q = [];
		for (var R = 0x0; R < M; R++) {
			var Y = 0x0;
			var U = R * P;
			var X = R == M - 0x1 ? P + L.length % M : P;
			for (var V = 0x0; V < X; V++) {
				var W = U + V;
				if (W < L.length) {
					Y = Y + L.charCodeAt(W);
				}
			}
			Y = Y * (N || 0x1f);
			Q.push(O.charAt(Y % O.length));
		}
		return Q.join('');
	}

	var J = H.split('').reverse().join('');
	var K = J + I(J, 0x4);
	return D(G, K);
}

function D(G, H) {
	if (!G) {
		return '';
	}
	var I = z(G);
	var J = '';
	for (var K = 0x0; K < I.length; K++) {
		J += String.fromCharCode(I.charCodeAt(K) ^ H.charCodeAt(K % H.length));
	}
	return y(J);
}

function z(G) {
	function J(Q) {
		if (Q >= 0xd800 && Q <= 0xdfff) {
			throw Error("not a scalar value");
		}
	}

	function K(Q) {
		var T = [];
		var W = 0x0;
		var V = Q.length;
		var X;
		var U;
		while (W < V) {
			X = Q.charCodeAt(W++);
			if (X >= 0xd800 && X <= 0xdbff && W < V) {
				U = Q.charCodeAt(W++);
				W = W + 0x1;
				if ((U & 0xfc00) == 0xdc00) {
					T.push(((X & 0x3ff) << 0xa) + (U & 0x3ff) + 0x10000);
				} else {
					T.push(X);
					W--;
				}
			} else {
				T.push(X);
			}
		}
		return T;
	}

	function L(Q) {
		if ((Q & 0xff80) == 0x0 & (Q >>> 0x10 & 0xffff) == 0x0) {
			return String.fromCharCode(Q);
		}
		var T = '';
		if ((Q & 0xf800) == 0x0 && (Q >>> 0x10 & 0xffff) == 0x0) {
			T = String.fromCharCode(Q >> 0x6 & 0x1f | 0xc0);
		} else if ((Q & 0x0) == 0x0 && (Q >>> 0x10 & 0xffff) == 0x0) {
			J(Q);
			T = String.fromCharCode(Q >> 0xc & 0xf | 0xe0);
			T += String.fromCharCode(Q >> 0x6 & 0x3f | 0x80);
		} else if ((Q & 0x0) == 0x0 && (Q >>> 0x10 & 0xffe0) == 0x0) {
			T = String.fromCharCode(Q >> 0x12 & 0x7 | 0xf0);
			T += String.fromCharCode(Q >> 0xc & 0x3f | 0x80);
			T += String.fromCharCode(Q >> 0x6 & 0x3f | 0x80);
		}
		T += String.fromCharCode(Q & 0x3f | 0x80);
		return T;
	}

	var M = K(G);
	var N = -0x1;
	var O = '';
	while (++N < M.length) {
		var P = M[N];
		O += L(P);
	}
	return O;
}

function y(G) {
	var H = '';
	H += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	H += "abcdefghijklmnopqrstuvwxyz";
	H += "0123456789";
	H += '+/';
	var I = G.length;
	var J = [];
	for (var K = 0x0; K < I; K++) {
		J[K >>> 0x2] |= (G.charCodeAt(K) & 0xff) << 0x18 - K % 0x4 * 0x8;
	}
	var L = [];
	for (var K = 0x0; K < I; K += 0x3) {
		var P = J[K >>> 0x2] >>> 0x18 - K % 0x4 * 0x8 & 0xff;
		var Q = J[K + 0x1 >>> 0x2] >>> 0x18 - (K + 0x1) % 0x4 * 0x8 & 0xff;
		var R = J[K + 0x2 >>> 0x2] >>> 0x18 - (K + 0x2) % 0x4 * 0x8 & 0xff;
		var O = P << 0x10 | Q << 0x8 | R;
		for (var S = 0x0; S < 0x4 && K + S * 0.75 < I; S++) {
			L.push(H.charAt(O >>> 0x6 * (0x3 - S) & 0x3f));
		}
	}
	for (var K = 0x0; K < L.length % 0x4; K++) {
		L.push('=');
	}
	return L.join('');
}
function decrypt(cipher, H) {
    H = H || "cdababcddcba";

    var reversedH = H.split('').reverse().join('');
    var derivedKey = reversedH + I(reversedH, 4);

    var decoded = rY(cipher);

    var xorStr = "";
    for (var i = 0; i < decoded.length; i++) {
        xorStr += String.fromCharCode(decoded.charCodeAt(i) ^ derivedKey.charCodeAt(i % derivedKey.length));
    }

    return rZ(xorStr);
}

function I(L, M, N) {
    if (L === '') {
        return '';
    }
    var O = "abcdhijkxy";
    var P = parseInt(L.length / M);
    var Q = [];
    for (var R = 0; R < M; R++) {
        var Y = 0;
        var U = R * P;
        var X = (R === M - 1 ? P + L.length % M : P);
        for (var V = 0; V < X; V++) {
            var W = U + V;
            if (W < L.length) {
                Y = Y + L.charCodeAt(W);
            }
        }
        Y = Y * (N || 0x1f);
        Q.push(O.charAt(Y % O.length));
    }
    return Q.join('');
}

function rY(G) {
    if (typeof atob === "function") {
        return atob(G);
    } else {
        return Buffer.from(G, 'base64').toString('binary');
    }
}

function rZ(utf8Str) {
    var res = '';
    var i = 0;
    while (i < utf8Str.length) {
        var c = utf8Str.charCodeAt(i);
        if (c < 128) {
            res += String.fromCharCode(c);
            i++;
        } else if ((c > 191) && (c < 224)) {
            var c2 = utf8Str.charCodeAt(i + 1);
            res += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
            i += 2;
        } else {
            var c2 = utf8Str.charCodeAt(i + 1);
            var c3 = utf8Str.charCodeAt(i + 2);
            res += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
            i += 3;
        }
    }
    return res;
}

var decrypted = decrypt("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", "9z7n");
console.log(decrypted);
