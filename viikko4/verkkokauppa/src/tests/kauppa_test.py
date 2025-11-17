import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()
        self.tuote1 = Tuote(1, "maito", 5)
        self.tuote2 = Tuote(2, "leipa", 3)
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            return 0
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return self.tuote1
            if tuote_id == 2:
                return self.tuote2
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_yhdella_tuotteella(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kahdella_eri_tuotteella(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "54321")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "54321", "33333-44455", 8)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kahdella_samalla_tuotteella(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "11111")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "11111", "33333-44455", 10)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kun_toinen_tuote_loppu(self):
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0
            return 0
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "22222")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "22222", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "11111")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "11111", "33333-44455", 5)
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "22222")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "22222", "33333-44455", 3)


    def test_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "11111")
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "22222")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_poista_korista_poistaa_tuotteen_kortista(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "11111")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "11111", "33333-44455", 0)
