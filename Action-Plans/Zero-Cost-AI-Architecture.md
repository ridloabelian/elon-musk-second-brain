# Blueprint: Zero-Cost AI Architecture (Rp 0)

**Filosofi:** Maksimalin Free Tier, 0% Kebocoran Cost, 100% Cache.
**Arsitektur:** Aplikasi ➔ Cloudflare AI Gateway (Cache/Tameng) ➔ 9router (Load Balancer/Rotasi) ➔ LLM Gratisan.

## Step 1: Isi Amunisi di 9router (The Backend)
9router lu (`9router.ridlo.id`) harus jadi pengepul *free tier*.
1. Masuk ke dashboard 9router lu.
2. Tambahin puluhan API key gratis:
   - **Groq** (Llama-3, ngebut buat reasoning) - 30 RPM.
   - **Gemini** (Pro/Flash) - 15 RPM.
   - **Kimi/Moonshot** - free tier.
3. Bikin **Model Routing / Fallback**. Kalo request Llama-3 kena limit (429), otomatis oper ke key Groq yang lain atau ke Gemini.
4. Buat 1 API Key 9router khusus buat aplikasi lu. (e.g. `sk-9router-prodig...`)

## Step 2: Pasang Tameng di Cloudflare (The Front)
Karena gue nggak punya akses token Cloudflare lu di environment ini, lu cukup klik ini di dashboard:
1. Buka [Cloudflare Dashboard](https://dash.cloudflare.com) ➔ AI ➔ **AI Gateway**.
2. Klik **Add New**. Kasih nama `prodig-gateway`.
3. Di setting Gateway lu, centang **Enable Caching**. (Ini kunci biar cost token jadi 0 buat request yang sama).
4. Lu bakal dapet Universal Endpoint URL. Bentuknya:
   `https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/prodig-gateway`

## Step 3: Tancep di Aplikasi (Astro / Prodig.id)
Aplikasi lu harus nge-hit CF AI Gateway, tapi ngasih tau CF buat nerusin request-nya ke 9router.

Gunakan header `cf-aig-custom-endpoint` untuk *bypass* routing bawaan CF.

**Contoh Fetch Call di API lu:**
```javascript
const response = await fetch("https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/prodig-gateway", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    // 1. Otorisasi buat 9router
    "Authorization": "Bearer sk-9router-prodig...", 
    
    // 2. Otorisasi buat CF AI Gateway (opsional jika AI gateway di-lock)
    // "cf-aig-authorization": "Bearer <cf_token>", 
    
    // 3. MAGIC HEADER: Kasih tau CF buat lempar ke 9router
    "cf-aig-custom-endpoint": "https://9router.ridlo.id/v1/chat/completions"
  },
  body: JSON.stringify({
    model: "llama3-70b-8192", // Ini ditangkap sama 9router lu
    messages: [
      { role: "user", content: "Buatkan tagline untuk website course saya." }
    ]
  })
});
```

## Hasil Akhir (The Physics)
- **User A** minta tagline ➔ CF kosong ➔ CF lempar ke 9router ➔ 9router potong kuota gratis Groq ➔ CF simpan di Cache.
- **User B** minta tagline yang sama ➔ CF langsung jawab (0 detik). 9router **NGGAK** disentuh. Kuota gratis aman. Cost Rp 0.

Extreme scaling, zero cost.
