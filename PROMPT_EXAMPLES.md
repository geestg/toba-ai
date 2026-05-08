# AI Toba - Prompt Examples

Berikut adalah daftar prompt yang sudah bisa dijawab oleh AI Toba agent:

---

## 1. RECOMMENDATION (Rekomendasi Destinasi)
**Intent:** `recommendation`

Prompt yang bisa dijawab:
- `aku mau liburan healing`
- `rekomendasi tempat wisata dong`
- `saya ingin jalan-jalan ke alam`
- `tempat pantai yang bagus di mana`
- `camping mana yang seru`
- `destinasi dengan view bagus`
- `tempat cultural/budaya yang recommended`
- `museum di sekitar danau toba`
- `wisata keluarga yang cocok`
- `tempat refreshing yang tenang`
- `sunset spot yang bagus`

**Respons:** Memberikan rekomendasi top 5 destinasi berdasarkan keyword yang dideteksi

---

## 2. DESTINATION DETAIL (Detail Destinasi)
**Intent:** `destination_detail`

Prompt yang bisa dijawab:
- `bukit holbung itu apa sih`
- `cerita tentang pantai parbaba`
- `air terjun sipiso piso bagaimana`
- `desa tomok itu destinasi apa`
- `info tentang bukit sibea bea`
- `situs batu passe itu dimana`

**Respons:** Detail destinasi termasuk tipe, area, deskripsi, dan cuaca saat ini

---

## 3. FOOD/KULINER (Makanan & Restoran)
**Intent:** `food`

**Prasyarat:** Harus pilih destinasi dulu (via intent recommendation atau destination_detail)

Prompt yang bisa dijawab (setelah pilih destinasi):
- `ada makanan apa di sini`
- `kuliner apa yang recommended`
- `restoran bagus di sekitar sini`
- `mau makan apa`
- `kafe ada gak di sini`
- `makanan khas apa yang harus coba`
- `tempat makan yang enak`

**Respons:** Daftar kuliner/restoran populer di destinasi yang dipilih

---

## 4. HOTEL/PENGINAPAN (Akomodasi)
**Intent:** `hotel`

**Prasyarat:** Harus pilih destinasi dulu

Prompt yang bisa dijawab (setelah pilih destinasi):
- `hotel di sini ada apa saja`
- `penginapan mana yang bagus`
- `homestay atau villa ada`
- `tempat menginap yang recommended`
- `resort mana yang bagus`
- `penginapan dekat sini ada gak`
- `booking hotel dimana`

**Respons:** Daftar penginapan dengan nama, tipe, lokasi, harga, rating

---

## 5. RUTE/PERJALANAN (Directions & Routes)
**Intent:** `route`

**Prasyarat:** Harus pilih destinasi dulu

Prompt yang bisa dijawab (setelah pilih destinasi):
- `bagaimana cara kesana`
- `rute ke tempat ini`
- `berapa jauh dari sini`
- `berapa lama perjalanannya`
- `jalan ke sini bagaimana`
- `map ke destinasi ini`
- `arah perjalanannya`

**Respons:** Rute detail dengan jarak (km), durasi (jam), kondisi traffic

---

## 6. CUACA (Weather)
**Intent:** `weather`

**Prasyarat:** Harus pilih destinasi dulu

Prompt yang bisa dijawab (setelah pilih destinasi):
- `cuaca di sini gimana`
- `hujan gak hari ini`
- `panas gak di sini`
- `kondisi cuaca sekarang`
- `aman buat datang sekarang`
- `kabut gak di tempat ini`
- `suhu berapa di sini`

**Respons:** Kondisi cuaca dan suhu di destinasi yang dipilih

---

## FLOW EXAMPLE - Percakapan Lengkap

### Scenario 1: User mau booking
```
User: "aku mau liburan healing"
→ Intent: recommendation
→ Respon: Rekomendasi 5 destinasi

User: "bukit holbung itu gimana"
→ Intent: destination_detail
→ Respon: Detail tentang Bukit Holbung

User: "ada hotel di situ gak"
→ Intent: hotel
→ Prasyarat: ✓ Destinasi sudah dipilih (Bukit Holbung)
→ Respon: Daftar hotel di Bukit Holbung dengan contact info
```

### Scenario 2: User mau tau rute & cuaca
```
User: "tempat pantai yang bagus"
→ Intent: recommendation
→ Respon: Rekomendasi pantai

User: "pantai parbaba"
→ Intent: destination_detail
→ Respon: Detail Pantai Parbaba

User: "cuaca disini gimana"
→ Intent: weather
→ Prasyarat: ✓ Destinasi sudah dipilih
→ Respon: Cuaca di Pantai Parbaba

User: "rute kesana dari medan"
→ Intent: route
→ Prasyarat: ✓ Destinasi sudah dipilih
→ Respon: Rute dari Medan ke Pantai Parbaba
```

### Scenario 3: User mau cari kuliner
```
User: "makan apa yang seru"
→ Intent: food (tapi belum ada destinasi)
→ Respon: "Pilih destinasi terlebih dahulu sebelum mencari kuliner"

User: "recommend destinasi budaya"
→ Intent: recommendation
→ Respon: Top 5 destinasi budaya

User: "desa tomok itu apa"
→ Intent: destination_detail
→ Respon: Detail Desa Tomok

User: "kuliner apa di desa tomok"
→ Intent: food
→ Prasyarat: ✓ Destinasi sudah dipilih
→ Respon: Daftar kuliner di Desa Tomok
```

---

## INTENT YANG TERDETEKSI TAPI BELUM ADA HANDLER KHUSUS

### 1. ITINERARY (Trip Plan)
**Status:** ❌ Belum di-implement

Keyword trigger: "itinerary", "jadwal", "rencana perjalanan", "3 hari", "2 hari", "planning"

Contoh prompt yang BELUM bisa:
- `buat itinerary 3 hari`
- `rencana perjalanan 2 hari`
- `jadwal wisata dari pagi sampe malam`

**Fallback:** Akan return generic response

---

### 2. CROWD (Keramaian)
**Status:** ❌ Belum di-implement  

Keyword trigger: "ramai", "crowd", "sepi", "padat"

Contoh prompt yang BELUM bisa:
- `dimana yang paling sepi`
- `destinasi yang tidak ramai`
- `crowd level di tempat ini gimana`
- `jam berapa paling sepi`

**Fallback:** Akan return generic response

---

## TESTING DENGAN CURL/POWERSHELL

### Test Recommendation
```powershell
$body = @{"message"="aku mau liburan healing"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

### Test Destination Detail
```powershell
$body = @{"message"="bukit holbung itu gimana"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

### Test Hotel (Setelah destination dipilih)
```powershell
$body = @{"message"="ada hotel di sini gak"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

### Test Cuaca (Setelah destination dipilih)
```powershell
$body = @{"message"="cuaca di sini gimana"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

### Test Rute (Setelah destination dipilih)
```powershell
$body = @{"message"="berapa lama ke sini"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

### Test Kuliner (Setelah destination dipilih)
```powershell
$body = @{"message"="ada makanan apa di sini"; "user_id"="user1"} | ConvertTo-Json
(Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json").Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

---

## STRUKTUR RESPONS

Setiap response dari API memiliki struktur:

```json
{
  "intent": "recommendation|destination_detail|food|hotel|route|weather|unknown",
  "reply": "Jawaban dalam bahasa Indonesia",
  "data": {
    "destinations": [...],
    "selected_destination": {...},
    "hotels": [...],
    "weather": {...},
    "route": {...},
    "foods": [...]
  }
}
```

---

## TIPS MENGGUNAKAN AI TOBA

1. **Mulai dengan rekomendasi** - Tanya destinasi apa yang cocok untuk tujuan wisata kamu
2. **Pilih destinasi** - Setelah dapat rekomendasi, tanya detail destinasi spesifik
3. **Tanya detail** - Baru tanya hotel, makanan, rute, atau cuaca di destinasi tersebut
4. **User ID bisa custom** - Setiap user_id akan punya memory sendiri (history & selected destination)
5. **Destinasi terus teringat** - System simpan destinasi pilihan, jadi cukup tanya "hotel di sini gak" tanpa perlu ulang nama destinasi

---

## DATA YANG TERSEDIA

✓ 60 destinasi  
✓ 67 hotel dengan info kontak (phone, email, address, jam operasional, website)  
✓ 59 kuliner/restoran  
✓ 55 rute perjalanan  
✓ 55 cuaca per destinasi  
✓ Memory per user (history + selected destination)  

---

**Last Updated:** May 8, 2026  
**Backend:** Python + FastAPI  
**LLM Reasoning:** OpenAI GPT-4o-mini (dengan caching)
