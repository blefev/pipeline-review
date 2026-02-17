from sqlalchemy.orm import Session

from app.models import Review, ReviewStatus, Sequence, Shot, ShotStatus, Show
from app.search import clear_index, index_review

SEED_DATA = {
    "shows": [
        {"title": "Battle of the Five Armies", "code": "BOTFA", "status": "active"},
        {"title": "Avatar: The Way of Water", "code": "ATWOW", "status": "active"},
        {"title": "Planet of the Apes: New Kingdom", "code": "POTA", "status": "complete"},
    ],
    "sequences": {
        "BOTFA": [
            {"code": "BTL", "description": "Battle sequence — Erebor plains"},
            {"code": "DRG", "description": "Dragon fire — Laketown destruction"},
            {"code": "EGL", "description": "Eagle rescue — Ravenhill"},
        ],
        "ATWOW": [
            {"code": "RFF", "description": "Reef exploration — bioluminescent ocean floor"},
            {"code": "SKP", "description": "Skimwing pursuit — open ocean chase"},
            {"code": "TSK", "description": "Tulkun hunt — whaling vessel attack"},
        ],
        "POTA": [
            {"code": "JGL", "description": "Jungle chase — overgrown cityscape"},
            {"code": "CLF", "description": "Cliff confrontation — dam overlook"},
        ],
    },
    "shots": {
        "BTL": [
            {"code": "BTL_0010", "status": "final", "assigned_to": "Marcus Chen", "frame_start": 1001, "frame_end": 1086},
            {"code": "BTL_0020", "status": "approved", "assigned_to": "Sarah Kim", "frame_start": 1001, "frame_end": 1124},
            {"code": "BTL_0030", "status": "review", "assigned_to": "James Ortiz", "frame_start": 1001, "frame_end": 1048},
            {"code": "BTL_0040", "status": "in_progress", "assigned_to": "Priya Patel", "frame_start": 1001, "frame_end": 1200},
        ],
        "DRG": [
            {"code": "DRG_0010", "status": "review", "assigned_to": "Liam Torres", "frame_start": 1001, "frame_end": 1150},
            {"code": "DRG_0020", "status": "in_progress", "assigned_to": "Aiko Tanaka", "frame_start": 1001, "frame_end": 1096},
            {"code": "DRG_0030", "status": "pending", "assigned_to": None, "frame_start": 1001, "frame_end": 1072},
        ],
        "EGL": [
            {"code": "EGL_0010", "status": "final", "assigned_to": "Marcus Chen", "frame_start": 1001, "frame_end": 1180},
            {"code": "EGL_0020", "status": "review", "assigned_to": "Sarah Kim", "frame_start": 1001, "frame_end": 1060},
        ],
        "RFF": [
            {"code": "RFF_0010", "status": "approved", "assigned_to": "Daniel Reyes", "frame_start": 1001, "frame_end": 1200},
            {"code": "RFF_0020", "status": "review", "assigned_to": "Emma Walsh", "frame_start": 1001, "frame_end": 1144},
            {"code": "RFF_0030", "status": "in_progress", "assigned_to": "Yuki Sato", "frame_start": 1001, "frame_end": 1096},
        ],
        "SKP": [
            {"code": "SKP_0010", "status": "review", "assigned_to": "Liam Torres", "frame_start": 1001, "frame_end": 1300},
            {"code": "SKP_0020", "status": "pending", "assigned_to": None, "frame_start": 1001, "frame_end": 1100},
        ],
        "TSK": [
            {"code": "TSK_0010", "status": "in_progress", "assigned_to": "Priya Patel", "frame_start": 1001, "frame_end": 1250},
            {"code": "TSK_0020", "status": "review", "assigned_to": "James Ortiz", "frame_start": 1001, "frame_end": 1180},
        ],
        "JGL": [
            {"code": "JGL_0010", "status": "final", "assigned_to": "Aiko Tanaka", "frame_start": 1001, "frame_end": 1096},
            {"code": "JGL_0020", "status": "final", "assigned_to": "Daniel Reyes", "frame_start": 1001, "frame_end": 1140},
        ],
        "CLF": [
            {"code": "CLF_0010", "status": "approved", "assigned_to": "Emma Walsh", "frame_start": 1001, "frame_end": 1072},
            {"code": "CLF_0020", "status": "final", "assigned_to": "Marcus Chen", "frame_start": 1001, "frame_end": 1160},
        ],
    },
    "reviews": {
        "BTL_0010": [
            {"author": "Joe Letteri", "status": "approved", "body": "Crowd sim density looks great on the plains. Edge blending with the matte painting is seamless now.", "department": "compositing"},
            {"author": "Matt Aitken", "status": "note", "body": "Can we add more dust particulates in the midground? The charge feels too clean for this scale of battle.", "department": "fx"},
        ],
        "BTL_0020": [
            {"author": "Joe Letteri", "status": "approved", "body": "Troll animation has real weight to it. Lighting integration with the overcast HDRI is solid.", "department": "lighting"},
        ],
        "BTL_0030": [
            {"author": "Matt Aitken", "status": "needs_revision", "body": "The catapult debris trajectory feels floaty after frame 1032. Need to increase gravity on the rigid body sim and add more secondary fragments.", "department": "fx"},
            {"author": "Joe Letteri", "status": "note", "body": "Watch the motion blur on the fast-moving debris — it's smearing into the BG plate edges.", "department": "compositing"},
        ],
        "DRG_0010": [
            {"author": "Joe Letteri", "status": "needs_revision", "body": "Dragon fire illumination on the water surface needs more caustic variation. Currently too uniform — should break up with the wave displacement.", "department": "lighting"},
            {"author": "Erik Winquist", "status": "note", "body": "The fire breath volumetric is reading well but the ember trail dissipates too quickly. Extend the particle lifetime by 15-20 frames.", "department": "fx"},
        ],
        "DRG_0020": [
            {"author": "Matt Aitken", "status": "note", "body": "Building collapse timing is good but we need more internal glow from the fire as the structure crumbles. Talk to lighting about interactive light rigs.", "department": "fx"},
        ],
        "EGL_0010": [
            {"author": "Joe Letteri", "status": "approved", "body": "Eagle feather detail holds up in close-up. Subsurface scattering on the wing membranes is beautiful in the backlit hero shot.", "department": "lighting"},
        ],
        "EGL_0020": [
            {"author": "Matt Aitken", "status": "needs_revision", "body": "The wind interaction on Gandalf's robes during the eagle grab needs another pass. Cloth sim is penetrating the eagle talons.", "department": "fx"},
        ],
        "RFF_0010": [
            {"author": "Joe Letteri", "status": "approved", "body": "Bioluminescence shader is gorgeous — the colour temperature shift with depth is exactly what we discussed. Final pixel.", "department": "lighting"},
        ],
        "RFF_0020": [
            {"author": "Eric Saindon", "status": "needs_revision", "body": "The coral reef displacement is clipping through the ocean floor geo in the wide shot. Also, the caustic pattern needs to match the water surface simulation above.", "department": "fx"},
            {"author": "Joe Letteri", "status": "note", "body": "Na'vi skin shader underwater — the subsurface scattering falloff is too aggressive. They're reading too dark below 10m depth.", "department": "lighting"},
        ],
        "RFF_0030": [
            {"author": "Eric Saindon", "status": "note", "body": "Fish schooling algorithm is working well but the turn radius is too tight for the larger species. Reference the manta ray footage from the shoot.", "department": "animation"},
        ],
        "SKP_0010": [
            {"author": "Joe Letteri", "status": "needs_revision", "body": "Skimwing water interaction is missing the spray rooster tail at speed. Need to add a wake particle system driven by the creature's velocity.", "department": "fx"},
            {"author": "Eric Saindon", "status": "note", "body": "The ocean surface shader is tiling visibly at this camera angle. Increase the noise octaves on the displacement to break up the pattern.", "department": "lighting"},
        ],
        "TSK_0020": [
            {"author": "Joe Letteri", "status": "needs_revision", "body": "Harpoon rope dynamics are too stiff — needs more sag and elasticity when the tulkun pulls. The current sim looks like a rigid pole.", "department": "fx"},
            {"author": "Eric Saindon", "status": "note", "body": "Blood cloud in the water is dispersing too symmetrically. Add turbulence to the fluid sim and reference real underwater dispersal footage.", "department": "fx"},
        ],
        "JGL_0010": [
            {"author": "Joe Letteri", "status": "approved", "body": "Vine and foliage overgrowth on the ruined buildings is excellent. The procedural growth pattern feels organic and the moss shader adds great detail.", "department": "fx"},
        ],
        "CLF_0010": [
            {"author": "Joe Letteri", "status": "approved", "body": "Waterfall mist interaction with the characters is well integrated. The volumetric depth is reading correctly in stereo.", "department": "compositing"},
        ],
    },
}


def run_seed(db: Session) -> dict:
    # Clear existing data
    db.query(Review).delete()
    db.query(Shot).delete()
    db.query(Sequence).delete()
    db.query(Show).delete()
    db.commit()
    clear_index()

    show_map: dict[str, Show] = {}
    seq_map: dict[str, Sequence] = {}
    shot_map: dict[str, Shot] = {}
    review_count = 0

    # Create shows
    for show_data in SEED_DATA["shows"]:
        show = Show(**show_data)
        db.add(show)
        db.flush()
        show_map[show.code] = show

    # Create sequences
    for show_code, seqs in SEED_DATA["sequences"].items():
        for seq_data in seqs:
            seq = Sequence(show_id=show_map[show_code].id, **seq_data)
            db.add(seq)
            db.flush()
            seq_map[seq.code] = seq

    # Create shots
    for seq_code, shots in SEED_DATA["shots"].items():
        for shot_data in shots:
            shot = Shot(
                sequence_id=seq_map[seq_code].id,
                code=shot_data["code"],
                status=ShotStatus(shot_data["status"]),
                assigned_to=shot_data.get("assigned_to"),
                frame_start=shot_data["frame_start"],
                frame_end=shot_data["frame_end"],
            )
            db.add(shot)
            db.flush()
            shot_map[shot.code] = shot

    # Create reviews and index them
    for shot_code, reviews in SEED_DATA["reviews"].items():
        for review_data in reviews:
            review = Review(
                shot_id=shot_map[shot_code].id,
                author=review_data["author"],
                status=ReviewStatus(review_data["status"]),
                body=review_data["body"],
                department=review_data.get("department"),
            )
            db.add(review)
            db.flush()
            index_review(review)
            review_count += 1

    db.commit()

    return {
        "shows": len(show_map),
        "sequences": len(seq_map),
        "shots": len(shot_map),
        "reviews": review_count,
    }
