import numpy as np

X = np.random.normal(0, 1, (500, 3))

with open('fake_data.txt', 'w') as f:
    f.write('x y z\n')
    for i in range(X.shape[0]):
        f.write('%.4f %.4f %.4f\n' % tuple(X[i]))


