FEDERAL_TAX_DATA = {
    2024: {
        "standard_deductions": {
            "single": 14600,
            "married": 29200,
            "head_of_household": 21900,
        },
        "dependents": {
            "child_tax_credit": 2000,
            "other_dependent_credit": 500,
        },
        "tax_brackets": {
            "single": [
                (0, 11600, 0.10),
                (11601, 47150, 0.12),
                (47151, 100525, 0.22),
                (100526, 191950, 0.24),
                (191951, 243725, 0.32),
                (243726, 609350, 0.35),
                (609351, float("inf"), 0.37),
            ],
            "married": [
                (0, 23200, 0.10),
                (23201, 94300, 0.12),
                (94301, 201050, 0.22),
                (201051, 383900, 0.24),
                (383901, 487450, 0.32),
                (487451, 731200, 0.35),
                (731201, float("inf"), 0.37),
            ],
            "head_of_household": [
                (0, 16550, 0.10),
                (16551, 63100, 0.12),
                (63101, 100500, 0.22),
                (100501, 191950, 0.24),
                (191951, 243700, 0.32),
                (243701, 609350, 0.35),
                (609351, float("inf"), 0.37),
            ],
        },
    },
}

