from django.test import TestCase, Client
from .models import News

class MainTest(TestCase):

    def test_main_url_is_exist(self):
        """
        ✅ TUJUAN:
        - Mengecek apakah URL utama ('') bisa diakses dengan benar.
        - Harus mengembalikan status code 200 (OK).
        
        💡 INTUISI:
        Ini memastikan route utama sudah terdaftar di urls.py dan view-nya berfungsi.
        """
        # TODO: Buat request GET ke URL utama (home)
        # Gunakan Client() bawaan Django untuk mengetes URL
        # Simpan hasilnya dalam variabel response
        # Lalu periksa apakah response.status_code == 200
        response = Client().get('')
        self.assertEqual(response.status_code)
        pass


    def test_main_using_main_template(self):
        """
        ✅ TUJUAN:
        - Mengecek apakah URL utama ('') menggunakan template 'main.html'.

        💡 INTUISI:
        Kita ingin pastikan view utama merender template yang benar.
        """
        # TODO: Buat request GET ke URL utama
        # Lalu gunakan self.assertTemplateUsed() untuk memastikan template yang dipakai 'main.html'
        pass


    def test_nonexistent_page(self):
        """
        ✅ TUJUAN:
        - Mengecek apakah halaman yang tidak ada (misalnya '/burhan_always_exists/')
          mengembalikan status 404 (Not Found).

        💡 INTUISI:
        Ini untuk pastikan error handling URL bekerja dengan baik.
        """
        # TODO: Buat request ke URL yang tidak ada (bebas)
        # Periksa apakah status_code == 404
        pass


    def test_news_creation(self):
        """
        ✅ TUJUAN:
        - Mengecek apakah objek News bisa dibuat dengan benar.
        - Memastikan field dan property pada model berfungsi sesuai harapan.

        💡 INTUISI:
        Ini memastikan model News dan properti seperti 'is_news_hot' berjalan sesuai logika bisnis.
        """
        # TODO: Buat 1 objek News menggunakan News.objects.create()
        # Isi field seperti title, content, category, news_views, is_featured
        # Gunakan self.assertEqual() atau self.assertTrue() untuk memeriksa:
        #   - category == 'match'
        #   - is_featured == True
        #   - is_news_hot == True  (pastikan property ini ada di model)
        pass
