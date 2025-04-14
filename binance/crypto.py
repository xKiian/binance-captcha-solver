import base64

class BinanceCrypto:
    @staticmethod
    def I(L, M, N=None):
        if L == '':
            return ''
        N = N if N is not None else 0x1f
        O = "abcdhijkxy"
        P = int(len(L) / M)
        Q = []
        for R in range(M):
            Y = 0
            U = R * P
            X = P + (len(L) % M) if R == M - 1 else P
            for V in range(X):
                W = U + V
                if W < len(L):
                    Y += ord(L[W])
            Y = Y * N
            Q.append(O[Y % len(O)])
        return ''.join(Q)

    @staticmethod
    def D(G, H):
        if not G:
            return ''
        I_str = BinanceCrypto.z(G)
        J = ""
        for K in range(len(I_str)):
            J += chr(ord(I_str[K]) ^ ord(H[K % len(H)]))
        return BinanceCrypto.y(J)

    @staticmethod
    def z(G):
        def J_func(Q):
            if Q >= 0xd800 and Q <= 0xdfff:
                raise ValueError("not a scalar value")

        def K_func(Q):
            T = []
            W = 0
            V = len(Q)
            while W < V:
                X = ord(Q[W])
                W += 1
                if X >= 0xd800 and X <= 0xdbff and W < V:
                    U = ord(Q[W])
                    W += 1
                    W += 1
                    if (U & 0xfc00) == 0xdc00:
                        T.append(((X & 0x3ff) << 10) + (U & 0x3ff) + 0x10000)
                    else:
                        T.append(X)
                        W -= 1
                else:
                    T.append(X)
            return T

        def L_func(Q):
            if ((Q & 0xff80) == 0) and (((Q >> 16) & 0xffff) == 0):
                return chr(Q)
            T = ''
            if (Q & 0xf800) == 0x0 and (Q >> 0x10 & 0xffff) == 0:
                T = chr(Q >> 0x6 & 0x1f | 0xc0)
            elif (Q & 0x0) == 0x0 and (Q >> 0x10 & 0xffff) == 0x0:
                J_func(Q)
                T = chr(Q >> 0xc & 0xf | 0xe0) + chr(Q >> 0x6 & 0x3f | 0x80)
            elif (Q & 0x0) == 0x0 and (Q >> 0x10 & 0xffe0) == 0:
                T = chr(((Q >> 18) & 0x7) | 0xf0) + chr(((Q >> 12) & 0x3f) | 0x80) + chr(((Q >> 6) & 0x3f) | 0x80)
            T += chr((Q & 0x3f) | 0x80)
            return T

        M = K_func(G)
        O = ''
        for P in M:
            O += L_func(P)
        return O

    @staticmethod
    def y(G):
        H_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        I_val = len(G)
        J_arr = [0] * ((I_val + 3) // 4)
        for K in range(I_val):
            J_arr[K // 4] |= (ord(G[K]) & 0xff) << (24 - (K % 4) * 8)
        L_list = []
        K_val = 0
        while K_val < I_val:
            P = (J_arr[K_val // 4] >> (24 - (K_val % 4) * 8)) & 0xff
            Q = (J_arr[(K_val + 1) // 4] >> (24 - ((K_val + 1) % 4) * 8)) & 0xff if (K_val + 1) < I_val else 0
            R = (J_arr[(K_val + 2) // 4] >> (24 - ((K_val + 2) % 4) * 8)) & 0xff if (K_val + 2) < I_val else 0
            O_val = (P << 16) | (Q << 8) | R
            S = 0
            while S < 4 and (K_val + S * 0.75) < I_val:
                L_list.append(H_alphabet[(O_val >> (6 * (3 - S))) & 0x3f])
                S += 1
            K_val += 3
        pad_len = (4 - len(L_list) % 4) % 4
        for _ in range(pad_len):
            L_list.append('=')
        return ''.join(L_list)

    @staticmethod
    def rY(G):
        missing_padding = len(G) % 4
        if missing_padding:
            G += '=' * (4 - missing_padding)
        return base64.b64decode(G).decode('latin1')

    @staticmethod
    def rZ(utf8Str):
        res = ''
        i = 0
        while i < len(utf8Str):
            c = ord(utf8Str[i])
            if c < 128:
                res += chr(c)
                i += 1
            elif c > 191 and c < 224:
                c2 = ord(utf8Str[i + 1])
                res += chr(((c & 31) << 6) | (c2 & 63))
                i += 2
            else:
                c2 = ord(utf8Str[i + 1])
                c3 = ord(utf8Str[i + 2])
                res += chr(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63))
                i += 3
        return res

    @staticmethod
    def encrypt(G, H="cdababcddcba"):
        J_str = H[::-1]
        K_str = J_str + BinanceCrypto.I(J_str, 4)
        return BinanceCrypto.D(G, K_str)

    @staticmethod
    def decrypt(cipher, H="cdababcddcba"):
        reversedH = H[::-1]
        derivedKey = reversedH + BinanceCrypto.I(reversedH, 4)
        decoded = BinanceCrypto.rY(cipher)
        xorStr = ''
        for i in range(len(decoded)):
            xorStr += chr(ord(decoded[i]) ^ ord(derivedKey[i % len(derivedKey)]))
        return BinanceCrypto.rZ(xorStr)
