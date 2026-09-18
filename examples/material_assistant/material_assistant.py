"""Original offline teaching service. No model, network, or ERP calls."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
import unicodedata
import uuid
from collections.abc import Callable
from typing import Any


class DomainError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text).upper())


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE tenants (
  tenant_id TEXT PRIMARY KEY,
  budget_cents INTEGER NOT NULL CHECK(budget_cents >= 0)
);
CREATE TABLE users (
  tenant_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('viewer','requester','approver')),
  categories TEXT NOT NULL,
  perm_version INTEGER NOT NULL CHECK(perm_version > 0),
  active INTEGER NOT NULL CHECK(active IN (0,1)),
  PRIMARY KEY(tenant_id, user_id),
  FOREIGN KEY(tenant_id) REFERENCES tenants(tenant_id)
);
CREATE TABLE suppliers (
  tenant_id TEXT NOT NULL,
  supplier_id TEXT NOT NULL,
  name TEXT NOT NULL,
  approved INTEGER NOT NULL CHECK(approved IN (0,1)),
  revision INTEGER NOT NULL CHECK(revision > 0),
  PRIMARY KEY(tenant_id, supplier_id),
  FOREIGN KEY(tenant_id) REFERENCES tenants(tenant_id)
);
CREATE TABLE materials (
  tenant_id TEXT NOT NULL,
  material_id TEXT NOT NULL,
  name TEXT NOT NULL,
  model TEXT NOT NULL,
  spec TEXT NOT NULL,
  category TEXT NOT NULL,
  base_unit TEXT NOT NULL,
  unit_factors TEXT NOT NULL,
  aliases TEXT NOT NULL,
  price_cents INTEGER NOT NULL CHECK(price_cents > 0),
  stock INTEGER NOT NULL CHECK(stock >= 0),
  lead_days INTEGER NOT NULL CHECK(lead_days >= 0),
  supplier_id TEXT NOT NULL,
  revision INTEGER NOT NULL CHECK(revision > 0),
  PRIMARY KEY(tenant_id, material_id),
  FOREIGN KEY(tenant_id, supplier_id)
    REFERENCES suppliers(tenant_id, supplier_id)
);
CREATE TABLE drafts (
  tenant_id TEXT NOT NULL,
  draft_id TEXT NOT NULL,
  requester_id TEXT NOT NULL,
  payload TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('draft','ordered')),
  PRIMARY KEY(tenant_id, draft_id),
  FOREIGN KEY(tenant_id, requester_id) REFERENCES users(tenant_id, user_id)
);
CREATE TABLE approvals (
  tenant_id TEXT NOT NULL,
  approval_id TEXT NOT NULL,
  draft_id TEXT NOT NULL,
  approver_id TEXT NOT NULL,
  approver_perm_version INTEGER NOT NULL,
  requester_perm_version INTEGER NOT NULL,
  payload_hash TEXT NOT NULL,
  expires_at INTEGER NOT NULL,
  used INTEGER NOT NULL CHECK(used IN (0,1)),
  PRIMARY KEY(tenant_id, approval_id),
  FOREIGN KEY(tenant_id, draft_id) REFERENCES drafts(tenant_id, draft_id),
  FOREIGN KEY(tenant_id, approver_id) REFERENCES users(tenant_id, user_id)
);
CREATE TABLE orders (
  tenant_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  draft_id TEXT NOT NULL,
  requester_id TEXT NOT NULL,
  payload TEXT NOT NULL,
  total_cents INTEGER NOT NULL CHECK(total_cents > 0),
  created_at INTEGER NOT NULL,
  PRIMARY KEY(tenant_id, order_id),
  UNIQUE(tenant_id, draft_id),
  FOREIGN KEY(tenant_id, draft_id) REFERENCES drafts(tenant_id, draft_id)
);
CREATE TABLE receipts (
  tenant_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  order_id TEXT NOT NULL,
  PRIMARY KEY(tenant_id, idempotency_key),
  FOREIGN KEY(tenant_id, order_id) REFERENCES orders(tenant_id, order_id)
);
CREATE TABLE audit (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tenant_id TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  event TEXT NOT NULL,
  object_id TEXT NOT NULL,
  details TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE INDEX material_scope ON materials(tenant_id, category);
"""


class MaterialService:
    def __init__(self, connection: sqlite3.Connection,
                 clock: Callable[[], float] = time.time):
        self.db = connection
        self.db.row_factory = sqlite3.Row
        # Explicit SQL transactions avoid reliance on evolving Python defaults.
        self.db.isolation_level = None
        self.db.execute("PRAGMA foreign_keys = ON")
        self.clock = clock
        self._fault_hook: Callable[[], None] | None = None

    @classmethod
    def demo(cls, clock: Callable[[], float] = time.time) -> "MaterialService":
        service = cls(sqlite3.connect(":memory:"), clock)
        service.db.executescript(SCHEMA)
        service.seed()
        return service

    def seed(self) -> None:
        self.db.execute("BEGIN IMMEDIATE")
        try:
            self.db.executemany("INSERT INTO tenants VALUES (?,?)",
                                [("atlas", 100000), ("cedar", 100000)])
            self.db.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", [
                ("atlas", "lin", "requester", '["maintenance"]', 1, 1),
                ("atlas", "qiao", "approver", '["maintenance"]', 1, 1),
                ("atlas", "wei", "viewer", '["maintenance"]', 1, 1),
                ("atlas", "yan", "requester", '["safety"]', 1, 1),
                ("cedar", "lin", "requester", '["maintenance"]', 1, 1),
                ("cedar", "qiao", "approver", '["maintenance"]', 1, 1),
            ])
            self.db.executemany("INSERT INTO suppliers VALUES (?,?,?,?,?)", [
                ("atlas", "SUP-A", "合成供应商甲", 1, 1),
                ("atlas", "SUP-B", "合成供应商乙", 0, 1),
                ("cedar", "SUP-C", "合成供应商丙", 1, 1),
            ])
            self.db.executemany("INSERT INTO materials VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
                ("atlas", "BR-6305-CS", "深沟球轴承", "6305", "碳钢，开放式", "maintenance",
                 "个", '{"个":1,"盒":10}', '["碳钢轴承","轴承6305"]', 2500, 4, 5, "SUP-A", 1),
                ("atlas", "BR-6305-SS", "深沟球轴承", "6305", "不锈钢，双侧密封", "maintenance",
                 "个", '{"个":1,"盒":5}', '["不锈钢轴承","密封轴承"]', 4800, 2, 8, "SUP-A", 1),
                ("atlas", "BL-M8-20", "六角螺栓", "M8x20", "镀锌，强度8.8级", "maintenance",
                 "个", '{"个":1,"盒":20}', '["M8螺丝","六角头螺栓"]', 120, 60, 3, "SUP-A", 1),
                ("atlas", "CB-2-5", "绝缘电线", "2.5MM2", "铜芯，蓝色，额定450/750V", "maintenance",
                 "米", '{"米":1,"卷":100}', '["蓝色电线","铜线"]', 350, 30, 6, "SUP-A", 1),
                ("atlas", "GL-SAFE", "防护手套", "G100", "耐磨，尺寸L", "safety",
                 "副", '{"副":1,"包":12}', '["手套"]', 900, 12, 4, "SUP-A", 1),
                ("atlas", "BR-6204", "深沟球轴承", "6204", "碳钢，开放式", "maintenance",
                 "个", '{"个":1}', '["待准入轴承"]', 2200, 0, 7, "SUP-B", 1),
                ("cedar", "BR-SECRET", "深沟球轴承", "6305", "仅供合成租户乙", "maintenance",
                 "个", '{"个":1}', '["秘密候选"]', 100, 99, 1, "SUP-C", 1),
            ])
            self.db.execute("COMMIT")
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def _user(self, tenant: str, user: str, write: bool = False,
              approve: bool = False) -> sqlite3.Row:
        row = self.db.execute("SELECT * FROM users WHERE tenant_id=? AND user_id=?",
                              (tenant, user)).fetchone()
        if row is None or not row["active"]:
            raise DomainError("ACCESS_DENIED")
        if write and row["role"] not in {"requester", "approver"}:
            raise DomainError("WRITE_DENIED")
        if approve and row["role"] != "approver":
            raise DomainError("APPROVE_DENIED")
        return row

    def _material(self, tenant: str, actor: sqlite3.Row,
                  material_id: str) -> sqlite3.Row:
        row = self.db.execute("SELECT * FROM materials WHERE tenant_id=? AND material_id=?",
                              (tenant, material_id)).fetchone()
        if row is None or row["category"] not in json.loads(actor["categories"]):
            # Same response for unknown and inaccessible objects.
            raise DomainError("MATERIAL_UNAVAILABLE")
        return row

    def _draft(self, tenant: str, draft_id: str) -> sqlite3.Row:
        row = self.db.execute("SELECT * FROM drafts WHERE tenant_id=? AND draft_id=?",
                              (tenant, draft_id)).fetchone()
        if row is None:
            raise DomainError("DRAFT_UNAVAILABLE")
        return row

    def _audit(self, tenant: str, actor: str, event: str,
               object_id: str, details: Any) -> None:
        self.db.execute("INSERT INTO audit(tenant_id,actor_id,event,object_id,details,created_at)"
                        " VALUES (?,?,?,?,?,?)",
                        (tenant, actor, event, object_id, canonical(details), int(self.clock())))

    def search(self, tenant: str, user: str, query: str,
               requested_unit: str | None = None) -> dict[str, Any]:
        actor = self._user(tenant, user)
        if not isinstance(query, str) or not query.strip() or len(query) > 200:
            raise DomainError("INVALID_QUERY")
        categories = json.loads(actor["categories"])
        if not categories:
            return {"candidates": [], "needs_clarification": False}
        marks = ",".join("?" for _ in categories)
        rows = self.db.execute(
            f"SELECT * FROM materials WHERE tenant_id=? AND category IN ({marks})",
            (tenant, *categories)).fetchall()
        needle = normalize(query)
        candidates = []
        for row in rows:
            model = normalize(row["model"])
            aliases = [normalize(a) for a in json.loads(row["aliases"])]
            score = 0
            if needle == model:
                score += 100
            elif needle in model:
                score += 40
            if needle in normalize(row["name"]) or needle in normalize(row["spec"]):
                score += 20
            if any(needle in alias for alias in aliases):
                score += 30
            if score:
                candidates.append({
                    "material_id": row["material_id"], "name": row["name"],
                    "model": row["model"], "spec": row["spec"], "score": score,
                    "stock": row["stock"], "lead_days": row["lead_days"],
                    "unit_compatible": requested_unit is None or
                        requested_unit in json.loads(row["unit_factors"]),
                    "source": f"material://{tenant}/{row['material_id']}@{row['revision']}",
                })
        candidates.sort(key=lambda item: (-item["score"], item["material_id"]))
        exact_model_count = sum(normalize(item["model"]) == needle for item in candidates)
        unclear = exact_model_count > 1 or (
            len(candidates) > 1 and candidates[0]["score"] - candidates[1]["score"] < 15)
        return {"candidates": candidates[:5], "needs_clarification": unclear}

    def answer(self, tenant: str, user: str, material_id: str) -> dict[str, Any]:
        actor = self._user(tenant, user)
        row = self._material(tenant, actor, material_id)
        source = f"material://{tenant}/{material_id}@{row['revision']}"
        return {
            "text": f"{row['name']}，型号{row['model']}，规格{row['spec']}。"
                    f"合成库存{row['stock']}{row['base_unit']}，记录交期{row['lead_days']}天。",
            "evidence": {field: {"value": row[field], "source": source}
                         for field in ("model", "spec", "stock", "base_unit", "lead_days")},
            "limits": ["交期不是到货承诺", "未验证替代适配性", "未接入实时ERP"],
        }

    def _payload(self, tenant: str, user: str, actor: sqlite3.Row,
                 material_id: str, quantity: int, unit: str) -> dict[str, Any]:
        if type(quantity) is not int or quantity <= 0 or quantity > 10000:
            raise DomainError("INVALID_QUANTITY")
        material = self._material(tenant, actor, material_id)
        factors = json.loads(material["unit_factors"])
        if unit not in factors:
            raise DomainError("UNIT_UNSUPPORTED")
        supplier = self.db.execute("SELECT * FROM suppliers WHERE tenant_id=? AND supplier_id=?",
                                   (tenant, material["supplier_id"])).fetchone()
        if supplier is None or not supplier["approved"]:
            raise DomainError("SUPPLIER_NOT_APPROVED")
        base_quantity = quantity * factors[unit]
        return {
            "tenant_id": tenant, "requester_id": user,
            "material_id": material_id, "name": material["name"], "model": material["model"],
            "spec": material["spec"], "category": material["category"],
            "material_revision": material["revision"], "supplier_id": supplier["supplier_id"],
            "supplier_revision": supplier["revision"], "quantity": quantity, "unit": unit,
            "base_quantity": base_quantity, "base_unit": material["base_unit"],
            "unit_factor": factors[unit], "price_cents": material["price_cents"],
            "currency": "CNY", "total_cents": base_quantity * material["price_cents"],
        }

    def create_draft(self, tenant: str, user: str, material_id: str,
                     quantity: int, unit: str) -> dict[str, Any]:
        actor = self._user(tenant, user, write=True)
        payload = self._payload(tenant, user, actor, material_id, quantity, unit)
        draft_id = "D-" + uuid.uuid4().hex[:12]
        with self._transaction():
            self.db.execute("INSERT INTO drafts VALUES (?,?,?,?,?,?)",
                            (tenant, draft_id, user, canonical(payload), digest(payload), "draft"))
            self._audit(tenant, user, "draft_created", draft_id, {"payload_hash": digest(payload)})
        return self.preview(tenant, user, draft_id)

    def update_draft(self, tenant: str, user: str, draft_id: str,
                     quantity: int, unit: str) -> dict[str, Any]:
        actor = self._user(tenant, user, write=True)
        with self._transaction():
            row = self._draft(tenant, draft_id)
            if row["requester_id"] != user:
                raise DomainError("DRAFT_UNAVAILABLE")
            if row["state"] != "draft":
                raise DomainError("DRAFT_CONSUMED")
            old = json.loads(row["payload"])
            payload = self._payload(tenant, user, actor, old["material_id"], quantity, unit)
            self.db.execute("UPDATE drafts SET payload=?,payload_hash=? WHERE tenant_id=? AND draft_id=?",
                            (canonical(payload), digest(payload), tenant, draft_id))
            self._audit(tenant, user, "draft_updated", draft_id, {"payload_hash": digest(payload)})
        return self.preview(tenant, user, draft_id)

    def preview(self, tenant: str, user: str, draft_id: str) -> dict[str, Any]:
        actor = self._user(tenant, user)
        row = self._draft(tenant, draft_id)
        payload = json.loads(row["payload"])
        self._material(tenant, actor, payload["material_id"])
        if row["requester_id"] != user and actor["role"] != "approver":
            raise DomainError("DRAFT_UNAVAILABLE")
        return {"draft_id": draft_id, "state": row["state"],
                "payload": payload, "payload_hash": row["payload_hash"]}

    def approve(self, tenant: str, approver: str, draft_id: str,
                expected_hash: str, ttl_seconds: int = 300) -> dict[str, Any]:
        if type(ttl_seconds) is not int or not 1 <= ttl_seconds <= 3600:
            raise DomainError("INVALID_TTL")
        with self._transaction():
            actor = self._user(tenant, approver, approve=True)
            draft = self._draft(tenant, draft_id)
            payload = json.loads(draft["payload"])
            self._material(tenant, actor, payload["material_id"])
            if approver == draft["requester_id"]:
                raise DomainError("SELF_APPROVAL_DENIED")
            requester = self._user(tenant, draft["requester_id"], write=True)
            self._material(tenant, requester, payload["material_id"])
            if draft["state"] != "draft":
                raise DomainError("DRAFT_CONSUMED")
            if expected_hash != draft["payload_hash"] or digest(payload) != draft["payload_hash"]:
                raise DomainError("PREVIEW_CHANGED")
            approval_id = "A-" + uuid.uuid4().hex[:12]
            expires_at = int(self.clock()) + ttl_seconds
            self.db.execute("INSERT INTO approvals VALUES (?,?,?,?,?,?,?,?,?)", (
                tenant, approval_id, draft_id, approver, actor["perm_version"],
                requester["perm_version"], expected_hash, expires_at, 0))
            self._audit(tenant, approver, "approval_granted", approval_id,
                        {"draft_id": draft_id, "payload_hash": expected_hash, "expires_at": expires_at})
        return {"approval_id": approval_id, "payload_hash": expected_hash, "expires_at": expires_at}

    class _Transaction:
        def __init__(self, db: sqlite3.Connection):
            self.db = db

        def __enter__(self):
            self.db.execute("BEGIN IMMEDIATE")
            return self

        def __exit__(self, kind, value, traceback):
            self.db.execute("COMMIT" if kind is None else "ROLLBACK")
            return False

    def _transaction(self):
        return self._Transaction(self.db)

    def confirm(self, tenant: str, requester: str, draft_id: str,
                approval_id: str, expected_hash: str,
                idempotency_key: str) -> dict[str, Any]:
        if not isinstance(idempotency_key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,80}", idempotency_key):
            raise DomainError("INVALID_IDEMPOTENCY_KEY")
        with self._transaction():
            actor = self._user(tenant, requester, write=True)
            request_hash = digest({"requester": requester, "draft_id": draft_id,
                                   "payload_hash": expected_hash})
            receipt = self.db.execute("SELECT * FROM receipts WHERE tenant_id=? AND idempotency_key=?",
                                      (tenant, idempotency_key)).fetchone()
            if receipt:
                if receipt["request_hash"] != request_hash:
                    raise DomainError("IDEMPOTENCY_CONFLICT")
                old_order = self._order(tenant, receipt["order_id"], replayed=True)
                self._material(tenant, actor, old_order["payload"]["material_id"])
                return old_order
            draft = self._draft(tenant, draft_id)
            if draft["requester_id"] != requester:
                raise DomainError("DRAFT_UNAVAILABLE")
            if draft["state"] != "draft":
                raise DomainError("DRAFT_CONSUMED")
            payload = json.loads(draft["payload"])
            if expected_hash != draft["payload_hash"] or digest(payload) != expected_hash:
                raise DomainError("PREVIEW_CHANGED")
            material = self._material(tenant, actor, payload["material_id"])
            approval = self.db.execute("SELECT * FROM approvals WHERE tenant_id=? AND approval_id=?",
                                       (tenant, approval_id)).fetchone()
            if approval is None or approval["draft_id"] != draft_id or approval["used"]:
                raise DomainError("APPROVAL_UNAVAILABLE")
            if approval["payload_hash"] != expected_hash:
                raise DomainError("APPROVAL_CHANGED")
            if int(self.clock()) >= approval["expires_at"]:
                raise DomainError("APPROVAL_EXPIRED")
            approver = self._user(tenant, approval["approver_id"], approve=True)
            self._material(tenant, approver, payload["material_id"])
            if approver["perm_version"] != approval["approver_perm_version"] or \
                    actor["perm_version"] != approval["requester_perm_version"]:
                raise DomainError("PERMISSION_CHANGED")
            supplier = self.db.execute("SELECT * FROM suppliers WHERE tenant_id=? AND supplier_id=?",
                                       (tenant, payload["supplier_id"])).fetchone()
            if supplier is None or not supplier["approved"]:
                raise DomainError("SUPPLIER_NOT_APPROVED")
            if material["revision"] != payload["material_revision"] or \
                    supplier["revision"] != payload["supplier_revision"]:
                raise DomainError("SOURCE_CHANGED")
            current = self._payload(tenant, requester, actor, payload["material_id"],
                                    payload["quantity"], payload["unit"])
            if current != payload:
                raise DomainError("SOURCE_CHANGED")
            changed = self.db.execute("UPDATE tenants SET budget_cents=budget_cents-?"
                                      " WHERE tenant_id=? AND budget_cents>=?",
                                      (payload["total_cents"], tenant, payload["total_cents"])).rowcount
            if changed != 1:
                raise DomainError("BUDGET_EXCEEDED")
            if self._fault_hook:
                self._fault_hook()
            order_id = "O-" + uuid.uuid4().hex[:12]
            self.db.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", (
                tenant, order_id, draft_id, requester, canonical(payload),
                payload["total_cents"], int(self.clock())))
            self.db.execute("UPDATE drafts SET state='ordered' WHERE tenant_id=? AND draft_id=?",
                            (tenant, draft_id))
            self.db.execute("UPDATE approvals SET used=1 WHERE tenant_id=? AND approval_id=?",
                            (tenant, approval_id))
            self.db.execute("INSERT INTO receipts VALUES (?,?,?,?)",
                            (tenant, idempotency_key, request_hash, order_id))
            self._audit(tenant, requester, "order_created", order_id,
                        {"draft_id": draft_id, "approval_id": approval_id,
                         "payload_hash": expected_hash, "total_cents": payload["total_cents"]})
            return self._order(tenant, order_id, replayed=False)

    def _order(self, tenant: str, order_id: str, replayed: bool) -> dict[str, Any]:
        row = self.db.execute("SELECT * FROM orders WHERE tenant_id=? AND order_id=?",
                              (tenant, order_id)).fetchone()
        return {"order_id": row["order_id"], "draft_id": row["draft_id"],
                "payload": json.loads(row["payload"]), "total_cents": row["total_cents"],
                "replayed": replayed}

    def audit_events(self, tenant: str, approver: str) -> list[dict[str, Any]]:
        self._user(tenant, approver, approve=True)
        return [dict(row) for row in self.db.execute(
            "SELECT * FROM audit WHERE tenant_id=? ORDER BY event_id", (tenant,))]


def run_demo() -> dict[str, Any]:
    service = MaterialService.demo()
    try:
        search = service.search("atlas", "lin", "6305")
        # A real user explicitly selects the carbon-steel item after clarification.
        evidence = service.answer("atlas", "lin", "BR-6305-CS")
        draft = service.create_draft("atlas", "lin", "BR-6305-CS", 1, "盒")
        approval = service.approve("atlas", "qiao", draft["draft_id"], draft["payload_hash"])
        args = ("atlas", "lin", draft["draft_id"], approval["approval_id"],
                draft["payload_hash"], "demo-request-001")
        first = service.confirm(*args)
        retry = service.confirm(*args)
        return {"mode": "offline_deterministic_no_llm", "search": search,
                "evidence": evidence, "draft": draft, "approval": approval,
                "first_order": first, "retry": retry,
                "budget_cents_remaining": service.db.execute(
                    "SELECT budget_cents FROM tenants WHERE tenant_id='atlas'").fetchone()[0],
                "audit": service.audit_events("atlas", "qiao")}
    finally:
        service.db.close()


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
