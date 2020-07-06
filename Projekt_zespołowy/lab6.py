
def parity_check(x1, x2, x3=0):
    sum = x1 + x2 + x3
    if sum % 2 == 0:
        o = 0
    else:
        o = 1
    return o

# Generowanie wiadomości
m = []
for i in range(0, 4):
    if i == 1 or i == 2:
        m.append(0)
    else:
        m.append(1)

# Kodowanie
signal = []
for idx, i in enumerate(m):
    if idx == 3:
        signal.append(0)
        signal.append(i)
    else:
        signal.append(i)
signal[3] = parity_check(signal[2], signal[1], signal[0])
signal.append(parity_check(signal[4], signal[1], signal[0]))
signal.append(parity_check(signal[4], signal[2], signal[0]))

print("Wiadomość: {}".format(m))
print("Zakodowana wiadomość: {}".format(signal))

# Dekodowanie
flag = 0
while flag >= 0:
    X1 = parity_check(signal[6], signal[6])
    X2 = parity_check(signal[5], signal[5])
    X4 = parity_check(signal[3], signal[3])
    S = X1 + X2 * 2 + X4 * 4

    if S == 0:
        break
    else:
        if signal[S] == 0:
            signal[S] = 1
        else:
            signal[S] = 0
    flag = flag + 1
    if flag == 2:
        print("Niepowodzenie przy naprawie błędu.")
        break

m2 = []
for idx, i in enumerate(m):
    if idx == 3:
        idx = idx + 1
    m2.append(signal[idx])

print("Odkodowana wiadomość: {}".format(m2))
