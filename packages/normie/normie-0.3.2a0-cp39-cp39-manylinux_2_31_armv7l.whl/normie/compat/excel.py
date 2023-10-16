from normie import cdf, invcdf, pdf


def NORM_INV(p, m, sd):
    return invcdf(p) * sd + m


def NORM_DIST(z, m, sd, cumulative):
    if cumulative:
        return cdf((z - m) / sd)
    else:
        return pdf((z - m) / sd) / 2
