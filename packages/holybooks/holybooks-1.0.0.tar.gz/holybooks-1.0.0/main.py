import holybooks

client = holybooks.Client(
    quran_translation="id."
)

surat = client.fetch_surah(2)
ayat = surat.ayats[254]

print(surat.english_name)
print(ayat)
print(ayat.number_in_surah)