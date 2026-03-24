"""
Risk Engine — dynamic weighted scoring system producing deterministic,
explainable risk scores based on context awareness and leak volume.
"""

from app.core.logging_config import logger
from app.models.schemas import Finding

class RiskEngine:
    """
    Weighted dynamic risk scoring engine.
    Factoring in finding volume and environmental context (Test vs Prod).
    """

    SEVERITY_WEIGHTS: dict[str, int] = {
        "critical": 10,
        "high": 7,
        "medium": 4,
        "low": 1,
    }

    RISK_THRESHOLDS = [
        (0, "low"),
        (5, "medium"),
        (15, "high"),
        (30, "critical"),
    ]

    def calculate(self, findings: list[Finding], content: str = "") -> dict:
        """
        Calculate dynamically weighted risk score.
        """
        if not findings:
            return {"risk_score": 0, "risk_level": "low"}

        # Context Awareness Check
        is_test_env = False
        content_lower = content.lower()
        if "test" in content_lower or "mock" in content_lower or "stub" in content_lower:
            is_test_env = True
            logger.info("Context Engine: Detected test/mock environment signatures. Risk will be scaled down.")

        total_score = 0
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for finding in findings:
            risk = finding.risk.lower()
            weight = self.SEVERITY_WEIGHTS.get(risk, 1)
            
            # Dynamic Context Penalty: halve weight if in a test env
            if is_test_env:
                weight = weight * 0.5
                
            total_score += weight
            if risk in severity_counts:
                severity_counts[risk] += 1

        # Dynamic Volume Escalator: massive amounts of leaks increase risk exponentially
        total_findings = len(findings)
        if total_findings > 10 and not is_test_env:
            volume_penalty = (total_findings - 10) * 0.5
            total_score += volume_penalty
            logger.info(f"Context Engine: Mass volume penalty applied (+{volume_penalty} score)")

        # Cap score at 100
        risk_score = min(int(total_score), 100)

        # Determine structural risk level
        risk_level = "low"
        for threshold, level in self.RISK_THRESHOLDS:
            if risk_score >= threshold:
                risk_level = level

        # Hard Overrides
        if severity_counts["critical"] > 0 and not is_test_env:
            risk_level = "critical"
            
        # Volume Hard Override
        if total_findings > 50 and risk_level not in ["high", "critical"]:
             risk_level = "high"
             logger.warning("Context Engine: Finding volume exceeded 50. Hard-elevating to HIGH risk.")

        logger.info(
            f"Risk calculation: score={risk_score}, level={risk_level}, "
            f"counts={severity_counts}, is_test={is_test_env}"
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "is_test_env": is_test_env
        }
