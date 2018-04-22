import sympy as sp

ln = sp.ln


class UeCMixin:
    def rulesC(self):
        Uae_1 = (
            self._Uae_C_1(),
            self.depth >= 0,
        )

        return [
            Uae_1,
        ]

    def exprC(self):
        rules = self.rulesC()

        expr = sp.Piecewise(
            *rules,
        )

        return expr

    def _Uae_C_1(self):
        expr = 1 / (
                self.rc3i / self.Kc * sp.ln(self.rc3o / self.rc3i) +
                self.rc3i / self.Kcem * sp.ln(self.tcem / self.rc3o + 1)
        )
        return expr
