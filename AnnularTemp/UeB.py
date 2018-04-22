import sympy as sp

ln = sp.ln


class UeBMixin:
    def rulesB(self):
        depth_of_casing3 = self.params['well']['casing3']['depth']
        Uae_1 = (
            self._Uae_B_1(),
            self.depth >= depth_of_casing3,
        )

        toc_of_casing2 = self.params['well']['casing2']['toc']
        Uae_2 = (
            self._Uae_B_2(),
            self.depth >= toc_of_casing2,
        )

        Uae_3 = (
            self._Uae_B_3(),
            self.depth >= 0,
        )

        return [
            Uae_1,
            Uae_2,
            Uae_3,
        ]

    def exprB(self):
        rules = self.rulesB()

        expr = sp.Piecewise(
            *rules,
        )

        return expr

    def _Uae_B_1(self):
        expr = 1 / (
                self.rc2i / self.Kc * sp.ln(self.rc2o / self.rc2i) +
                self.rc2i / self.Kcem * sp.ln(self.rc3i / self.rc2o)
        )
        return expr

    def _Uae_B_2(self):
        expr = 1 / (
                self.rc2i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc2i / self.Kcem * ln(self.rc3i / self.rc2o) +
                self.rc2i / self.Kc * ln(self.rc3o / self.rc3i) +
                self.rc2i / self.Kcem * ln(self.tcem / self.rc3o + 1)
        )

        return expr

    def _Uae_B_3(self):
        expr = 1 / (
                self.rc2i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc2i / self.Ka * ln(self.rc3i / self.rc2o) +
                self.rc2i / self.Kc * ln(self.rc3o / self.rc3i) +
                self.rc2i / self.Kcem * ln(self.tcem / self.rc3o + 1)
        )

        return expr
