
# Ajándékötletek Deploy Render-re (Dizájnos verzió)

1. Push-old a teljes projektet GitHub-ra.
2. Regisztrálj a [Render.com](https://render.com)-on.
3. Új Web Service létrehozása:
   - GitHub repo csatlakoztatása
   - Branch: main
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
4. Environment Variables:
   - SECRET_KEY = (erős titkos kulcs)
   - PAYPAL_CLIENT_ID = (PayPal éles Client ID)
5. Deploy → Render automatikusan HTTPS-sel létrehozza a weboldalt.
6. Ellenőrizd, hogy a fizetés és a kreditek működnek.
7. A weboldal most dizájnos, témához illő: pasztell színek, szép gombok és reszponzív elrendezés.
