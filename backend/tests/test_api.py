import os
import tempfile
import unittest
from unittest import mock

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"
os.environ["SECRET_KEY"] = "test-secret-key-for-tests"
os.environ["ENVIRONMENT"] = "testing"
os.environ["AI_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from data.schemes_seed import scheme_count, seed_schemes  # noqa: E402


def _init_db():
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_schemes(db)
    finally:
        db.close()


class ApiTestCase(unittest.TestCase):
    _counter = 0

    @classmethod
    def setUpClass(cls):
        _init_db()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        engine.dispose()
        try:
            os.unlink(_tmp.name)
        except OSError:
            pass

    def _email(self, prefix="user"):
        ApiTestCase._counter += 1
        return f"{prefix}_{ApiTestCase._counter}@example.com"

    def _register(self, email=None, password="StrongPass123"):
        return self.client.post("/api/auth/register", json={"email": email or self._email(), "password": password})

    def _login(self, email=None, password="StrongPass123"):
        return self.client.post("/api/auth/login", json={"email": email or self._email(), "password": password})

    def _token(self):
        r = self._register()
        if r.status_code != 200:
            r = self._login()
        return r.json()["access_token"]

    def _headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def _create_profile(self, token, sector="food_processing", state="maharashtra"):
        payload = {
            "full_name": "Priya Sharma",
            "phone_number": "9876543210",
            "state": state,
            "district": "Pune",
            "age_group": "26-35",
            "gender": "female",
            "social_category": "obc",
            "business_name": "Priya Foods",
            "business_sector": sector,
            "business_stage": "existing",
            "annual_revenue": "10l_50l",
            "employee_count": "1-5",
            "support_needs": ["loan", "training"],
        }
        return self.client.post("/api/profile", json=payload, headers=self._headers(token))


class TestAuth(ApiTestCase):
    def test_register(self):
        r = self._register("register_test@example.com")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], "register_test@example.com")

    def test_register_duplicate(self):
        r = self._register("dup@example.com")
        self.assertEqual(r.status_code, 200)
        r2 = self._register("dup@example.com")
        self.assertEqual(r2.status_code, 400)

    def test_login_wrong_password(self):
        self._register("login@example.com")
        r = self.client.post("/api/auth/login", json={"email": "login@example.com", "password": "WrongPass123"})
        self.assertEqual(r.status_code, 401)

    def test_login_success(self):
        self._register("login2@example.com")
        r = self.client.post("/api/auth/login", json={"email": "login2@example.com", "password": "StrongPass123"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertTrue(data["user"]["id"])

    def test_me(self):
        token = self._token()
        r = self.client.get("/api/auth/me", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertIn("email", r.json())

    def test_me_unauthenticated(self):
        r = self.client.get("/api/auth/me")
        self.assertEqual(r.status_code, 401)

    def test_register_with_phone(self):
        r = self.client.post(
            "/api/auth/register",
            json={"email": "phone_register@example.com", "password": "StrongPass123", "phone_number": "9876543210"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["user"]["phone_number"], "9876543210")
        token = r.json()["access_token"]
        me = self.client.get("/api/auth/me", headers=self._headers(token))
        self.assertEqual(me.json()["phone_number"], "9876543210")

    def test_forgot_password_does_not_leak_otp(self):
        self._register("forgot_flow@example.com")
        r = self.client.post("/api/auth/forgot-password", json={"email": "forgot_flow@example.com"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("message", data)
        self.assertNotIn("otp", data)
        self.assertNotIn("dev_otp", data)

    def test_forgot_password_unknown_email(self):
        r = self.client.post("/api/auth/forgot-password", json={"email": "nobody@example.com"})
        self.assertEqual(r.status_code, 404)

    def test_captured_otp(self):
        captured = {}

        def fake_deliver(self, user, otp):
            captured["otp"] = otp

        with mock.patch.object(AuthService, "_deliver_otp", fake_deliver):
            self._register("cap_otp@example.com")
            r = self.client.post("/api/auth/forgot-password", json={"email": "cap_otp@example.com"})
        self.assertEqual(r.status_code, 200)
        self.assertRegex(captured["otp"], r"^\d{6}$")
        return captured["otp"]

    def test_full_otp_reset_flow(self):
        self._register("otp_flow@example.com")
        captured = {}

        def fake_deliver(self, user, otp):
            captured["otp"] = otp

        with mock.patch.object(AuthService, "_deliver_otp", fake_deliver):
            forgot = self.client.post("/api/auth/forgot-password", json={"email": "otp_flow@example.com"})
        otp = captured["otp"]
        verify = self.client.post("/api/auth/verify-otp", json={"email": "otp_flow@example.com", "otp": otp})
        self.assertEqual(verify.status_code, 200)
        reset_token = verify.json()["reset_token"]
        reset = self.client.post(
            "/api/auth/reset-password", json={"token": reset_token, "new_password": "BrandNewPass123"}
        )
        self.assertEqual(reset.status_code, 200)
        login = self.client.post("/api/auth/login", json={"email": "otp_flow@example.com", "password": "BrandNewPass123"})
        self.assertEqual(login.status_code, 200)
        self.assertIn("access_token", login.json())

    def test_verify_otp_wrong_code(self):
        self._register("wrong_otp@example.com")
        captured = {}

        def fake_deliver(self, user, otp):
            captured["otp"] = otp

        with mock.patch.object(AuthService, "_deliver_otp", fake_deliver):
            self.client.post("/api/auth/forgot-password", json={"email": "wrong_otp@example.com"})
        r = self.client.post("/api/auth/verify-otp", json={"email": "wrong_otp@example.com", "otp": "000000"})
        self.assertEqual(r.status_code, 401)

    def test_verify_otp_without_request(self):
        self._register("no_otp@example.com")
        r = self.client.post("/api/auth/verify-otp", json={"email": "no_otp@example.com", "otp": "123456"})
        self.assertEqual(r.status_code, 400)

    def test_reset_without_otp_token(self):
        r = self.client.post("/api/auth/reset-password", json={"token": "garbage", "new_password": "NewPass1234"})
        self.assertEqual(r.status_code, 401)


class TestProfile(ApiTestCase):
    def test_create_profile(self):
        token = self._token()
        r = self._create_profile(token)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["business_sector"], "food_processing")
        self.assertIn("loan", r.json()["support_needs"])

    def test_get_profile(self):
        token = self._token()
        self._create_profile(token)
        r = self.client.get("/api/profile", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["full_name"], "Priya Sharma")

    def test_update_profile(self):
        token = self._token()
        self._create_profile(token)
        r = self.client.put("/api/profile", json={"business_stage": "expanding", "support_needs": ["subsidy"]},
                            headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["business_stage"], "expanding")
        self.assertIn("subsidy", r.json()["support_needs"])


class TestUnderstanding(ApiTestCase):
    def _setup(self):
        token = self._token()
        self._create_profile(token, sector="ecommerce", state="punjab")
        return token

    def test_understand_builtin(self):
        token = self._setup()
        r = self.client.post("/api/ai/understand", json={
            "description": "I make pickles and namkeen in my small kitchen and want to sell online"
        }, headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["provider"], "builtin")
        self.assertEqual(data["sector"], "food_processing")
        self.assertIn("pickle", data["tags"])
        self.assertTrue(data["summary_en"])

    def test_confirm_persists_and_profile_includes_fields(self):
        token = self._setup()
        r = self.client.post("/api/ai/confirm", json={
            "description": "I make pickles and namkeen",
            "sector": "food_processing",
            "tags": ["pickle", "namkeen"],
            "summary_en": "Food business",
            "summary_hi": "खाद्य व्यवसाय",
        }, headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        saved = self.client.get("/api/ai/understanding", headers=self._headers(token)).json()
        self.assertEqual(saved["sector"], "food_processing")
        self.assertEqual(saved["tags"], ["pickle", "namkeen"])
        prof = self.client.get("/api/profile", headers=self._headers(token)).json()
        self.assertTrue(prof["ai_confirmed"])
        self.assertEqual(prof["ai_sector"], "food_processing")
        self.assertEqual(prof["ai_tags"], ["pickle", "namkeen"])

    def test_matching_uses_confirmed_sector(self):
        token = self._setup()
        rec = self.client.post("/api/recommendations", json={}, headers=self._headers(token)).json()
        baseline = {x["scheme_id"]: x["match_score"] for x in rec["recommendations"]}
        self.client.post("/api/ai/confirm", json={
            "description": "I make pickles and namkeen",
            "sector": "food_processing",
            "tags": ["pickle", "namkeen"],
            "summary_en": "Food business",
            "summary_hi": "खाद्य व्यवसाय",
        }, headers=self._headers(token))
        rec2 = self.client.post("/api/recommendations", json={}, headers=self._headers(token)).json()
        food_scores = {x["scheme_id"]: x["match_score"] for x in rec2["recommendations"]}
        moved = [sid for sid in food_scores if food_scores[sid] > baseline.get(sid, 0)]
        self.assertTrue(moved, "confirming a food sector should lift at least one food scheme")


class TestSchemes(ApiTestCase):
    def test_list_schemes(self):
        token = self._token()
        r = self.client.get("/api/schemes?limit=200", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["total"], scheme_count())
        self.assertEqual(len(data["schemes"]), scheme_count())

    def test_filter_by_sector(self):
        token = self._token()
        r = self.client.get("/api/schemes", params={"sector": "food_processing"}, headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.json()["total"], 5)

    def test_get_scheme_detail(self):
        token = self._token()
        r = self.client.get("/api/schemes/1", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertIn("benefits", r.json())

    def test_get_scheme_missing(self):
        token = self._token()
        r = self.client.get("/api/schemes/99999", headers=self._headers(token))
        self.assertEqual(r.status_code, 404)


class TestRecommendations(ApiTestCase):
    def test_recommendations(self):
        token = self._token()
        self._create_profile(token)
        r = self.client.post("/api/recommendations", json={
            "support_needs": ["loan", "training"],
            "language": "en",
            "min_score": 40,
            "max_results": 10,
        }, headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("recommendations", data)
        self.assertGreaterEqual(data["total_schemes"], 1)
        first = data["recommendations"][0]
        self.assertIn("match_score", first)
        self.assertIn("match_breakdown", first)
        self.assertIn("explanation", first)
        self.assertTrue(first["explanation"])

    def test_recommendations_without_profile(self):
        token = self._token()
        r = self.client.post("/api/recommendations", json={}, headers=self._headers(token))
        self.assertEqual(r.status_code, 400)

    def test_recommendations_hindi_explanation(self):
        token = self._token()
        self._create_profile(token)
        r = self.client.post("/api/recommendations", json={"language": "hi", "max_results": 5},
                             headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        for rec in r.json()["recommendations"]:
            self.assertTrue(rec["explanation"])


class TestSavedScheme(ApiTestCase):
    def test_save_and_list_and_remove(self):
        token = self._token()
        r = self.client.post("/api/saved-schemes/1", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["scheme"]["id"], 1)

        r2 = self.client.get("/api/saved-schemes", headers=self._headers(token))
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["total"], 1)

        dup = self.client.post("/api/saved-schemes/1", headers=self._headers(token))
        self.assertEqual(dup.status_code, 400)

        r3 = self.client.delete("/api/saved-schemes/1", headers=self._headers(token))
        self.assertEqual(r3.status_code, 200)

        r4 = self.client.get("/api/saved-schemes", headers=self._headers(token))
        self.assertEqual(r4.json()["total"], 0)


class TestPreferences(ApiTestCase):
    def test_preferences_default(self):
        token = self._token()
        r = self.client.get("/api/preferences", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["language"], "en")
        self.assertEqual(r.json()["theme"], "light")

    def test_preferences_update(self):
        token = self._token()
        self._create_profile(token)
        r = self.client.put("/api/preferences", json={"language": "hi", "theme": "dark"},
                            headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["language"], "hi")
        self.assertEqual(r.json()["theme"], "dark")


class TestQuestionnaireProgress(ApiTestCase):
    def test_default_empty(self):
        token = self._token()
        r = self.client.get("/api/questionnaire/progress", headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["answers"], {})
        self.assertEqual(r.json()["step"], 0)

    def test_save_and_get(self):
        token = self._token()
        r = self.client.put("/api/questionnaire/progress", json={
            "answers": {"full_name": "Amit", "business_sector": "food_processing"},
            "step": 4,
        }, headers=self._headers(token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["step"], 4)

        r2 = self.client.get("/api/questionnaire/progress", headers=self._headers(token))
        self.assertEqual(r2.json()["answers"]["business_sector"], "food_processing")

    def test_progress_isolation_between_users(self):
        t1 = self._token()
        t2 = self._token()
        self.client.put("/api/questionnaire/progress", json={"answers": {"full_name": "A"}, "step": 2}, headers=self._headers(t1))
        r2 = self.client.get("/api/questionnaire/progress", headers=self._headers(t2))
        self.assertEqual(r2.json()["answers"], {})

    def test_overwrite_and_clear(self):
        token = self._token()
        self.client.put("/api/questionnaire/progress", json={"answers": {"x": "1"}, "step": 1}, headers=self._headers(token))
        r = self.client.put("/api/questionnaire/progress", json={"answers": {"x": "2"}, "step": 3}, headers=self._headers(token))
        self.assertEqual(r.json()["step"], 3)
        self.assertEqual(r.json()["answers"]["x"], "2")

        d = self.client.delete("/api/questionnaire/progress", headers=self._headers(token))
        self.assertEqual(d.status_code, 204)
        r2 = self.client.get("/api/questionnaire/progress", headers=self._headers(token))
        self.assertEqual(r2.json()["step"], 0)

    def test_requires_auth(self):
        r = self.client.get("/api/questionnaire/progress")
        self.assertEqual(r.status_code, 401)


class TestHealth(ApiTestCase):
    def test_health(self):
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()