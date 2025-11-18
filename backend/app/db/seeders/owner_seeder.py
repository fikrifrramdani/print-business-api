# app/seeders/owner_seeder.py
from app import models
from app.utils.auth_utils import hash_password

def seed_owner_if_empty(db):
    owner = db.query(models.User).filter(models.User.role == "owner").first()
    if not owner:
        # ✅ Buat store utama dulu
        store = models.Store(
            name="Cabang Utama",
            address="Alamat Pusat",
            phone="08123456789",
            owner="owner"
        )

        db.add(store)
        db.commit()
        db.refresh(store)

        # ✅ Buat owner
        new_owner = models.User(
            username="owner",
            email="owner@mail.com",
            hashed_password=hash_password("owner1234"),
            role="owner",
            store_id=store.id
        )
        db.add(new_owner)
        db.commit()
        print("✅ Default owner berhasil dibuat (username: owner, password: owner1234)")
