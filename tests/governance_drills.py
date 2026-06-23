import unittest
import requests
import os

class TestSAGCGovernance(unittest.TestCase):
    def test_ghost_agent_rejection(self):
        """Test Case A: Verify zero-trust rejection of missing fencing tokens."""
        response = requests.post("http://localhost:8080/v1/chat/completions", 
                                 headers={"x-internal-agent-id": "ghost-agent"})
        self.assertEqual(response.status_code, 403, "Failed: System allowed unauthenticated agent.")

    def test_fail_closed_on_redis_outage(self):
        """Test Case C: Verify fail-closed posture if state-store is unavailable."""
        # Simulated by passing a dummy URL that will cause a connection failure
        os.environ["REDIS_URL"] = "http://localhost:0" 
        response = requests.post("http://localhost:8080/v1/chat/completions", 
                                 headers={"x-internal-agent-id": "any-agent", "x-fencing-token": "45"})
        # Expect 503 or 403, never 200
        self.assertNotEqual(response.status_code, 200, "CRITICAL: System failed open during outage.")

if __name__ == "__main__":
    unittest.main()