# Architecture
1. AMI/MDM/CRM synchronisent les clients et relevés.
2. PostgreSQL/PostGIS stocke les données.
3. Le scoring produit des suspects et explications.
4. React/Leaflet visualise les risques.
5. Les missions sont assignées aux agents.
6. L'application Expo fonctionne hors-ligne avec SQLite.
7. Les rapports sont synchronisés au retour du réseau.

## Production
À compléter avant mise en production :
- OAuth2/SSO complet et Refresh Tokens
- RBAC effectif
- MinIO/S3 pour preuves photos
- capture signature
- SHA-256 des preuves
- Alembic
- moteur ML + SHAP entraîné
- rate limiting
- audit renforcé
