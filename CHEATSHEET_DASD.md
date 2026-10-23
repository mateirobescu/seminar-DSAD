# DASD – Cheat sheet

Formule + cum se folosesc în Python (numpy / pandas / scipy). Se completează pas cu pas.

---

## 1. Citire și pregătirea datelor

```python
import numpy as np
import pandas as pd

df = pd.read_csv("data_in/fisier.csv", index_col=0)   # prima coloană devine index
variabile = list(df)[3:]          # numele coloanelor numerice (sari peste primele 3)
x = df[variabile].values          # matrice numpy (n observații × m variabile)
```

- `df.index.name` = numele indexului, `list(df)` = lista coloanelor.
- `index_col=0` se folosește când prima coloană e un cod (ex. Siruta) după care faci `merge`.

### Înlocuirea valorilor lipse (NaN) cu media coloanei

```python
def nan_replace(x):
    x = x.copy()
    k = np.where(np.isnan(x))                 # (linii, coloane) unde e NaN
    x[k] = np.nanmean(x[:, k[1]], axis=0)     # media coloanei, ignorând NaN
    return x
```

Variantă pandas, mai simplă: `df[variabile] = df[variabile].fillna(df[variabile].mean())`.

---

## 2. Centrare și standardizare

| Operație | Formulă | Cod |
|---|---|---|
| Centrare | $x_c = x - \bar{x}$ | `x - np.mean(x, axis=0)` |
| Standardizare | $z = \dfrac{x - \bar{x}}{\sigma}$ | `(x - m) / np.std(x, axis=0)` |

- `axis=0` = calcul pe coloane (pe variabile).
- `np.std(..., ddof=0)` împarte la $n$ (implicit), `ddof=1` împarte la $n-1$.
- Alternativă: `StandardScaler().fit_transform(x)` (sklearn, folosește $n$).

---

## 3. Covarianță și corelație

$$V_{jk} = \frac{1}{n-1}\sum_{i=1}^{n}(x_{ij}-\bar{x}_j)(x_{ik}-\bar{x}_k) \qquad R_{jk} = \frac{V_{jk}}{\sigma_j\,\sigma_k}$$

```python
V = np.cov(x, rowvar=False)        # covarianță, m × m
R = np.corrcoef(x, rowvar=False)   # corelație, m × m
```

- **`rowvar=False` e obligatoriu** când variabilele sunt pe coloane (cazul normal).
- `np.cov` împarte la $n-1$ implicit.

### Pe grupe (ex. pe regiune)

```python
clase = np.unique(y)                    # y = vectorul cu eticheta grupei
for c in clase:
    z = x[y == c, :]                    # doar liniile din grupa c
    R_c = np.corrcoef(z, rowvar=False)
    V_c = np.cov(z, rowvar=False)
```

---

## 4. Salvarea unei matrici cu etichete

```python
pd.DataFrame(M, index=etichete_linii, columns=etichete_coloane).to_csv("data_out/M.csv")
```

---

## 5. Pandas – operațiile de bază pentru temele 2.x

Exemplele pornesc de la `df` = date pe localități, `activitati` = lista coloanelor numerice.

### Filtrare și coloane noi

```python
df[df["Total"] > 0]                      # filtrare pe condiție (rânduri)
df["Total"] = df[activitati].sum(axis=1) # sumă pe rând (axis=1), pe coloană (axis=0)
df.insert(0, "Localitate", serie)        # inserează coloană pe poziția 0
```

### Sortare

```python
s.sort_values(ascending=False)           # serie / coloană
df.sort_values(by="Pondere", ascending=False)
```

### Merge (JOIN) – lipirea a două tabele

```python
# după index pe ambele părți (ex. ambele au Siruta ca index)
df1.merge(df2[["Judet", "Populatie"]], left_index=True, right_index=True)

# index pe o parte, coloană pe cealaltă
df1.merge(df_coduri, left_on="Judet", right_index=True)
```

- Implicit e inner join: rămân doar rândurile care există în ambele tabele.
- Dacă ai nevoie doar de câteva coloane din al doilea tabel, selectează-le înainte (`df2[[...]]`).

### Groupby – agregare pe grupe (localitate → județ → regiune)

```python
df.groupby(by="Judet")[activitati].sum()      # sumă pe județ, fiecare activitate
df.groupby("Regiune").apply(func, include_groups=False)  # funcție proprie pe fiecare grup
```

- Rezultatul are grupul ca **index**.
- Cu `apply`, funcția primește un DataFrame (toate rândurile grupei).
- Ierarhie: localitate → județ (`merge` cu tabela de coduri localități), județ → regiune → macroregiune (`merge` cu tabela de coduri județe), apoi `groupby(...).sum()` la fiecare nivel.

### Apply – o funcție pe rând / pe coloană

```python
df[activitati].apply(lambda x: x / x.sum(), axis=1)   # fiecare RÂND (ponderi pe rând)
df[activitati].apply(lambda x: x / x.sum(), axis=0)   # fiecare COLOANĂ
```

- `axis=1` → funcția primește un rând; `axis=0` → primește o coloană.

### Activitatea / coloana cu valoarea maximă

```python
df[activitati].idxmax(axis=1)                 # numele coloanei cu maximul, pe rând
df[activitati].apply(lambda x: x.index[x.argmax()], axis=1)  # echivalent
```

### Procente și ponderi

| Ce | Formulă | Cod |
|---|---|---|
| Pondere pe rând | $p_{ij} = \dfrac{x_{ij}}{\sum_j x_{ij}}$ | `df.apply(lambda x: x/x.sum(), axis=1)` |
| Procent | $p \cdot 100$ | `.apply(lambda x: x*100/x.sum(), axis=1)` |
| Total 0 → rezultat 0 | evită NaN din 0/0 | `.fillna(0)` |
| Pondere la total coloană | $\dfrac{x_{ij}}{\sum_i x_{ij}}$ | `df / df.sum(axis=0)` |

### Media ponderată

$$\bar{x} = \frac{\sum_i x_i\,w_i}{\sum_i w_i}$$

```python
np.average(x, weights=w)        # x: vector, w: ponderi (nu trebuie normalizate)
np.average(X[:, :-1], axis=0, weights=X[:, -1])   # pe coloane, ponderi = ultima coloană
```

### Scrierea în fișier

```python
df.to_csv("data_out/Cerinta1.csv")                    # păstrează indexul
df.to_csv("data_out/Cerinta1.csv", index=False)       # fără index
s.round(5).to_csv("data_out/Cerinta3.csv")            # rotunjire la 5 zecimale
```

- Pentru o `Serie`, setează numele (`s.name = "Pondere"`) ca să apară în antetul CSV.

---

## 6. Indici Shannon și Simpson

### Pasul 0: ce înseamnă $p_i$ (aici se greșește cel mai des)

Același indice, două moduri de a alege $p_i$. Citești enunțul și vezi care se potrivește.

| Varianta | $p_i$ | Se împarte pe | Rezultatul spune | Teme |
|---|---|---|---|---|
| **Disparitate / segregare** | ponderea unității $i$ în totalul categoriei: $p_i = \dfrac{x_i}{\sum_i x_i}$ | **coloană** (`axis=0`) | cât de **împrăștiată** e categoria în teritoriu | 2.1, 2.3 |
| **Diversitate** | ponderea categoriei $i$ în unitate: $p_i = \dfrac{x_i}{\sum_i x_i}$ | **rând** (`axis=1`) | cât de **variată** e unitatea ca amestec | 2.2 |

- $n$ = numărul de unități teritoriale (varianta 1) sau numărul de categorii (varianta 2).
- Suma $p_i$ e mereu 1 (fracție, nu procent).

### Formule

| Indice | Formulă | Cod |
|---|---|---|
| Shannon-Weaver | $H = -\sum p_i \log_2 p_i$ | `entropy(p, base=2)` |
| Simpson | $S_1 = 1 - \sum p_i^2$ | `1 - (p**2).sum()` |
| Inverse Simpson | $S_2 = \dfrac{1}{\sum p_i^2}$ | `1 / (p**2).sum()` |

- `entropy` din `scipy.stats`: **`base=2` obligatoriu** (implicit e `ln`). Normalizează singură.
- Simpson nu se poate lua direct din numerele brute: întâi `p = x / x.sum()`.

### Cod: varianta pe coloane (segregare, 2.1 / 2.3)

```python
from scipy.stats import entropy

def shannon(df):
    p = df.values / df.values.sum(axis=0)       # ponderea unității în total coloană
    return pd.Series(entropy(p, base=2, axis=0), index=df.columns)

def simpson(df):
    p = df.values / df.values.sum(axis=0)
    return pd.Series(1 - (p**2).sum(axis=0), index=df.columns)

def inverse_simpson(df):
    p = df.values / df.values.sum(axis=0)
    return pd.Series(1 / (p**2).sum(axis=0), index=df.columns)

# apel: câte un rând pe județ
df.groupby(by="County").apply(func=shannon)
```

### Cod: varianta pe rând (diversitate, 2.2)

```python
def simpson(x):                    # x = un rând = populațiile pe categorii într-o unitate
    p = x / x.sum()
    return 1 - (p * p).sum()

df_jud[confesiuni].apply(simpson, axis=1)      # un număr pe județ
```

### Cum se interpretează

- **Shannon / Simpson mici** → concentrat (într-o unitate sau într-o categorie dominantă). **Mari** → împrăștiat / variat.
- Valori extreme, pentru $n$ unități:

| | Concentrat total | Distribuție egală |
|---|---|---|
| $H$ | 0 | $\log_2 n$ |
| $S_1$ | 0 | $1 - \dfrac{1}{n}$ |
| $S_2$ | 1 | $n$ |

- **Inverse Simpson = „număr efectiv" de unități/categorii.** Ex.: 17,6 → distribuit ca și cum ar fi egal între ~18 unități. Analog, $2^H$ e tot un număr efectiv.
- **Nu poți compara direct** valori între județe cu număr diferit de localități (maximul depinde de $n$).
- Acești indici **nu măsoară cât de mulți sunt**, ci **unde sunt**. Pentru mărimea unei categorii se folosesc procentele.

### Capcane

- **Total 0 (categorie absentă):** `p = x / 0` dă `0/0 = NaN`. `tx[tx==0] = 1` oprește împărțirea, dar `entropy` renormalizează și dă tot `NaN`. Fix: `np.nan_to_num(entropy(...))`.
- La Simpson, coloana absentă dă `1 - 0 = 1` (maxim, înșelător); la Inverse Simpson dă 1 (minim). Verifică ce vrei să raportezi pentru ele.
- Axa trebuie să fie aceeași la `p` și la suma pătratelor. Dacă `p` e pe coloane, suma e pe `axis=0`, altfel obții lungimi nepotrivite.

---

*Următorul pas: indicele de disimilaritate (2.1) și calculele de la 2.3 (vot).*
