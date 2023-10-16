import request3
from bs4 import BeautifulSoup


def ekstraksi_data():
    """
Tanggal: 17 September 2023
Waktu: 07:44:20 WIB
Magnitudo: 4.2
Kedalaman: 5km
Lokasi: LS=3.34  BT= 97.90
Pusat gempa: berada di darat 18 km Tenggara Kutacane
Dirasakan:  (Skala MMI): II-III Aceh Tenggara
    :return:
    """
    try:
        content = request3.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class' : 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result [1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        ls = None
        bt = None
        kedalaman = None
        lokasi = None
        koordinat = None
        Dirasakan = None

        for res in result:
            print(i, res)
            if i == 1 :
                magnitudo = res.text
            elif i == 2 :
                kedalaman = res.text
            elif i == 3 :
                koordinat = res.text.split (' - ')
                ls = koordinat [0]
                bt = koordinat [1]
            elif i == 4 :
                lokasi = res.text
            elif i == 5 :
                dirasakan = res.text
            i = i + 1


        hasil = dict()
        hasil['tanggal'] = tanggal #'17 September 2023'
        hasil['Waktu'] = waktu#'07:44:20 WIB'
        hasil['Magnitudo'] =  magnitudo
        hasil['Kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] =  lokasi
        hasil['Dirasakan'] = '(Skala MMI): II-III Aceh Tenggara'
        return hasil
    else:
        return None





def tampilkan_data(result):
    print('gempa terakhir berdasarkan BMKG')
    print(f"tanggal {result['tanggal']}")
    print(f"Waktu {result['Waktu']}")
    print(f"Magnitudo {result['Magnitudo']}")
    print(f"Kedalaman {result['Kedalaman']}")
    print(f"koordinat: LS={result['koordinat']['ls']},BR={result['koordinat']['bt']}")
    print(f"lokasi {result['lokasi']}")
    print(f"Dirasakan {result['Dirasakan']}")

if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)

