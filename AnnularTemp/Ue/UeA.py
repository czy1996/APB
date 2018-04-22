import sympy as sp

ln = sp.ln


class UeAMixin:
    def rulesA(self):
        depth_of_casing2 = self.params['well']['casing2']['depth']
        Uae_1 = (
            self._Uae_A_1(),
            self.depth >= depth_of_casing2,
        )

        toc_of_casing1 = self.params['well']['casing1']['toc']
        Uae_2 = (
            self._Uae_A_2(),
            self.depth >= toc_of_casing1,
        )

        depth_of_casing3 = self.params['well']['casing3']['depth']
        Uae_3 = (
            self._Uae_A_3(),
            self.depth >= depth_of_casing3,
        )

        toc_of_casing2 = self.params['well']['casing2']['toc']
        Uae_4 = (
            self._Uae_A_4(),
            self.depth >= toc_of_casing2,
        )

        Uae_5 = (
            self._Uae_A_5(),
            self.depth >= 0,
        )

        return [
            Uae_1,
            Uae_2,
            Uae_3,
            Uae_4,
            Uae_5,
        ]

    def exprA(self):
        rules = self.rulesA()

        expr = sp.Piecewise(
            *rules,
        )

        return expr

    def _Uae_A_1(self):
        expr = 1 / (
                self.rc1i / self.Kc * sp.ln(self.rc1o / self.rc1i) +
                self.rc1i / self.Kcem * sp.ln(self.rc2i / self.rc1o)
        )
        return expr

    def _Uae_A_2(self):
        expr = 1 / (
                self.rc1i / self.Kc * ln(self.rc1o / self.rc1i) +
                self.rc1i / self.Kcem * ln(self.rc2i / self.rc1o) +
                self.rc1i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc1i / self.Kcem * ln(self.rc3i / self.rc2o)
        )

        return expr

    def _Uae_A_3(self):
        expr = 1 / (
                self.rc1i / self.Kc * ln(self.rc1o / self.rc1i) +
                self.rc1i / self.Ka * ln(self.rc2i / self.rc1o) +
                self.rc1i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc1i / self.Kcem * ln(self.rc3i / self.rc2o)
        )

        return expr

    def _Uae_A_4(self):
        expr = 1 / (
                self.rc1i / self.Kc * ln(self.rc1o / self.rc1i) +
                self.rc1i / self.Ka * ln(self.rc2i / self.rc1o) +
                self.rc1i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc1i / self.Kcem * ln(self.rc3i / self.rc2o) +
                self.rc1i / self.Kc * ln(self.rc3o / self.rc3i) +
                self.rc1i / self.Kcem * ln(self.tcem / self.rc3o + 1)
        )

        return expr

    def _Uae_A_5(self):
        expr = 1 / (
                self.rc1i / self.Kc * ln(self.rc1o / self.rc1i) +
                self.rc1i / self.Ka * ln(self.rc2i / self.rc1o) +
                self.rc1i / self.Kc * ln(self.rc2o / self.rc2i) +
                self.rc1i / self.Ka * ln(self.rc3i / self.rc2o) +
                self.rc1i / self.Kc * ln(self.rc3o / self.rc3i) +
                self.rc1i / self.Kcem * ln(self.tcem / self.rc3o + 1)
        )

        return expr
