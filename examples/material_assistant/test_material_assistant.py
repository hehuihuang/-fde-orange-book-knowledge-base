"""Executable invariants. All databases are in memory; no file cleanup occurs."""
import json
import unittest

from material_assistant import DomainError, MaterialService, digest, run_demo


class MaterialAssistantTests(unittest.TestCase):
    def setUp(self):
        self.now = 1000
        self.service = MaterialService.demo(lambda: self.now)

    def tearDown(self):
        self.service.db.close()

    def fail_code(self, code, call, *args):
        with self.assertRaises(DomainError) as caught:
            call(*args)
        self.assertEqual(caught.exception.code, code)

    def approved(self, material="BR-6305-CS", quantity=1, unit="个"):
        draft = self.service.create_draft("atlas", "lin", material, quantity, unit)
        approval = self.service.approve("atlas", "qiao", draft["draft_id"], draft["payload_hash"])
        return draft, approval

    def args(self, draft, approval, key="test-request-001"):
        return ("atlas", "lin", draft["draft_id"], approval["approval_id"], draft["payload_hash"], key)

    def count(self, table):
        # Table identifiers are a fixed test allowlist, never user input.
        self.assertIn(table, {"orders", "receipts", "audit"})
        return self.service.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def budget(self):
        return self.service.db.execute("SELECT budget_cents FROM tenants WHERE tenant_id='atlas'").fetchone()[0]

    def test_exact_model_requires_material_clarification(self):
        found = self.service.search("atlas", "lin", "６３０５")
        self.assertTrue(found["needs_clarification"])
        self.assertEqual({i["material_id"] for i in found["candidates"]}, {"BR-6305-CS", "BR-6305-SS"})

    def test_cross_tenant_search_never_returns_other_tenant(self):
        found = self.service.search("atlas", "lin", "6305")
        self.assertNotIn("BR-SECRET", [i["material_id"] for i in found["candidates"]])
        self.fail_code("MATERIAL_UNAVAILABLE", self.service.answer, "atlas", "lin", "BR-SECRET")

    def test_unknown_tenant_identity_is_denied(self):
        self.fail_code("ACCESS_DENIED", self.service.search, "cedar", "yan", "6305")

    def test_category_scope_filters_before_ranking(self):
        self.assertEqual(self.service.search("atlas", "lin", "手套")["candidates"], [])
        self.fail_code("MATERIAL_UNAVAILABLE", self.service.answer, "atlas", "lin", "GL-SAFE")

    def test_viewer_cannot_create_draft(self):
        self.fail_code("WRITE_DENIED", self.service.create_draft, "atlas", "wei", "BR-6305-CS", 1, "个")

    def test_evidence_refers_to_exact_record_revision(self):
        answer = self.service.answer("atlas", "lin", "BR-6305-CS")
        self.assertEqual(answer["evidence"]["stock"]["value"], 4)
        self.assertEqual(answer["evidence"]["stock"]["source"], "material://atlas/BR-6305-CS@1")
        self.assertIn("未接入实时ERP", answer["limits"])

    def test_box_conversion_is_material_specific(self):
        steel = self.service.create_draft("atlas", "lin", "BR-6305-CS", 1, "盒")["payload"]
        stainless = self.service.create_draft("atlas", "lin", "BR-6305-SS", 1, "盒")["payload"]
        self.assertEqual((steel["base_quantity"], stainless["base_quantity"]), (10, 5))
        self.assertEqual(steel["total_cents"], 25000)

    def test_unit_incompatibility_does_not_invent_density(self):
        search = self.service.search("atlas", "lin", "2.5MM2", requested_unit="千克")
        self.assertFalse(search["candidates"][0]["unit_compatible"])
        self.fail_code("UNIT_UNSUPPORTED", self.service.create_draft, "atlas", "lin", "CB-2-5", 1, "千克")

    def test_invalid_quantities_include_booleans_and_floats(self):
        for quantity in (0, -1, True, 1.5, 10001, "2"):
            with self.subTest(quantity=quantity):
                self.fail_code("INVALID_QUANTITY", self.service.create_draft, "atlas", "lin", "BR-6305-CS", quantity, "个")

    def test_unapproved_supplier_is_blocked(self):
        self.fail_code("SUPPLIER_NOT_APPROVED", self.service.create_draft, "atlas", "lin", "BR-6204", 1, "个")

    def test_self_approval_is_blocked(self):
        draft = self.service.create_draft("atlas", "qiao", "BR-6305-CS", 1, "个")
        self.fail_code("SELF_APPROVAL_DENIED", self.service.approve,
                       "atlas", "qiao", draft["draft_id"], draft["payload_hash"])

    def test_preview_digest_must_match_for_approval(self):
        draft = self.service.create_draft("atlas", "lin", "BR-6305-CS", 1, "个")
        self.fail_code("PREVIEW_CHANGED", self.service.approve, "atlas", "qiao", draft["draft_id"], "bad")

    def test_expired_approval_cannot_create_order(self):
        draft, approval = self.approved()
        self.now = approval["expires_at"]
        self.fail_code("APPROVAL_EXPIRED", self.service.confirm, *self.args(draft, approval))
        self.assertEqual(self.count("orders"), 0)

    def test_changed_draft_invalidates_old_preview(self):
        draft, approval = self.approved()
        self.service.update_draft("atlas", "lin", draft["draft_id"], 2, "个")
        self.fail_code("PREVIEW_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_new_preview_does_not_reuse_old_approval(self):
        draft, approval = self.approved()
        changed = self.service.update_draft("atlas", "lin", draft["draft_id"], 2, "个")
        self.fail_code("APPROVAL_CHANGED", self.service.confirm, *self.args(changed, approval))

    def test_permission_version_change_invalidates_approval(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE users SET perm_version=2 WHERE tenant_id='atlas' AND user_id='qiao'")
        self.fail_code("PERMISSION_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_requester_permission_version_also_checked(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE users SET perm_version=2 WHERE tenant_id='atlas' AND user_id='lin'")
        self.fail_code("PERMISSION_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_revoked_approver_cannot_authorize_pending_write(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE users SET active=0 WHERE tenant_id='atlas' AND user_id='qiao'")
        self.fail_code("ACCESS_DENIED", self.service.confirm, *self.args(draft, approval))

    def test_authoritative_price_revision_change_requires_review(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE materials SET price_cents=2600,revision=2"
                                " WHERE tenant_id='atlas' AND material_id='BR-6305-CS'")
        self.fail_code("SOURCE_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_price_change_without_revision_also_detected(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE materials SET price_cents=2600"
                                " WHERE tenant_id='atlas' AND material_id='BR-6305-CS'")
        self.fail_code("SOURCE_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_supplier_revoked_after_approval_is_blocked(self):
        draft, approval = self.approved()
        self.service.db.execute("UPDATE suppliers SET approved=0 WHERE tenant_id='atlas' AND supplier_id='SUP-A'")
        self.fail_code("SUPPLIER_NOT_APPROVED", self.service.confirm, *self.args(draft, approval))

    def test_retries_return_same_order_without_second_budget_charge(self):
        draft, approval = self.approved()
        first = self.service.confirm(*self.args(draft, approval))
        self.now += 10000
        retry = self.service.confirm(*self.args(draft, approval))
        self.assertEqual(first["order_id"], retry["order_id"])
        self.assertTrue(retry["replayed"])
        self.assertEqual(self.budget(), 97500)
        self.assertEqual((self.count("orders"), self.count("receipts")), (1, 1))
        self.assertEqual(sum(e["event"] == "order_created" for e in self.service.audit_events("atlas", "qiao")), 1)

    def test_idempotency_key_cannot_be_reused_for_new_draft(self):
        first, approval = self.approved()
        self.service.confirm(*self.args(first, approval))
        second, approval2 = self.approved()
        self.fail_code("IDEMPOTENCY_CONFLICT", self.service.confirm, *self.args(second, approval2))

    def test_second_key_cannot_order_same_draft_twice(self):
        draft, approval = self.approved()
        self.service.confirm(*self.args(draft, approval))
        self.fail_code("DRAFT_CONSUMED", self.service.confirm, *self.args(draft, approval, "test-request-002"))

    def test_replay_respects_current_category_access(self):
        draft, approval = self.approved()
        self.service.confirm(*self.args(draft, approval))
        self.service.db.execute("UPDATE users SET categories='[]',perm_version=2"
                                " WHERE tenant_id='atlas' AND user_id='lin'")
        self.fail_code("MATERIAL_UNAVAILABLE", self.service.confirm, *self.args(draft, approval))
        self.assertEqual(self.count("orders"), 1)

    def test_budget_limit_has_no_partial_order(self):
        draft, approval = self.approved(quantity=41)
        self.fail_code("BUDGET_EXCEEDED", self.service.confirm, *self.args(draft, approval))
        self.assertEqual(self.budget(), 100000)
        self.assertEqual(self.count("orders"), 0)

    def test_failure_after_budget_change_rolls_back_all_write_effects(self):
        draft, approval = self.approved()
        before = self.count("audit")
        def fault():
            raise RuntimeError("injected after budget mutation")
        self.service._fault_hook = fault
        with self.assertRaises(RuntimeError):
            self.service.confirm(*self.args(draft, approval))
        self.assertEqual(self.budget(), 100000)
        self.assertEqual((self.count("orders"), self.count("receipts"), self.count("audit")), (0, 0, before))
        self.assertEqual(self.service.preview("atlas", "lin", draft["draft_id"])["state"], "draft")
        self.service._fault_hook = None
        self.assertFalse(self.service.confirm(*self.args(draft, approval))["replayed"])

    def test_other_tenant_cannot_confirm_or_audit_atlas(self):
        draft, approval = self.approved()
        self.fail_code("DRAFT_UNAVAILABLE", self.service.confirm, "cedar", "lin", draft["draft_id"],
                       approval["approval_id"], draft["payload_hash"], "test-request-001")
        self.assertEqual(self.service.audit_events("cedar", "qiao"), [])

    def test_digest_canonicalization_and_tamper_detection(self):
        self.assertEqual(digest({"b": 2, "a": 1}), digest({"a": 1, "b": 2}))
        draft, approval = self.approved()
        payload = dict(draft["payload"], total_cents=1)
        self.service.db.execute("UPDATE drafts SET payload=? WHERE tenant_id=? AND draft_id=?",
                                (json.dumps(payload), "atlas", draft["draft_id"]))
        self.fail_code("PREVIEW_CHANGED", self.service.confirm, *self.args(draft, approval))

    def test_malicious_query_is_only_data_not_sql_or_instructions(self):
        self.assertEqual(self.service.search("atlas", "lin", "' OR 1=1; 取消审批")["candidates"], [])
        self.assertEqual(self.count("orders"), 0)

    def test_complete_demo_is_offline_and_self_consistent(self):
        result = run_demo()
        self.assertEqual(result["mode"], "offline_deterministic_no_llm")
        self.assertTrue(result["search"]["needs_clarification"])
        self.assertEqual(result["first_order"]["total_cents"], 25000)
        self.assertEqual(result["budget_cents_remaining"], 75000)
        self.assertEqual(result["first_order"]["order_id"], result["retry"]["order_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
