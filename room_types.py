COEF = 6

NEXT_CORNER = {
    1: lambda x1, y1: ((x1 + 7) * COEF, (y1 + 7) * COEF),
    2: lambda x1, y1: ((x1 + 15) * COEF, (y1 + 7) * COEF),
    3: lambda x1, y1: ((x1 + 15) * COEF, (y1 + 7) * COEF),
    4: lambda x1, y1: ((x1 + 7) * COEF, (y1 + 15) * COEF),
    5: lambda x1, y1: ((x1 + 7) * COEF, (y1 + 15) * COEF)
}