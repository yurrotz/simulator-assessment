def agresti_cull(n, ns, z=2):

    interval = [None, None]

    n_ = n + pow(z, 2)
    p_ = 1 / n_ * (ns + pow(z, 2)/2)

    interval[0] = round((p_ - z * pow(p_/n_ * (1 - p_), 1/2)) * 100, 2)
    interval[1] = round((p_ + z * pow(p_/n_ * (1 - p_), 1/2)) * 100, 2)

    return interval

print(agresti_cull(31, 1))