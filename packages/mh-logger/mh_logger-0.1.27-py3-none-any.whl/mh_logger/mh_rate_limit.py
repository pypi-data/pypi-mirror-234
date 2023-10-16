import inspect
import os
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from threading import Thread
from typing import Any, Dict, NamedTuple, Optional, Tuple

from redis import Redis

ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "True") == "True"


class RateLimitException(Exception):
    rate_id: str

    def __init__(
        self,
        rate_id: str,
        rate_limit: Optional[float],
        rate: Optional[int],
        hint: str = "",
    ):
        if hint:
            hint = " Hint :: " + hint
        super().__init__(
            f"Usage rate :: {rate} exceeds rate_limit :: {rate_limit} with rate_id :: {rate_id}.{hint}"  # noqa
        )
        self.rate_id = rate_id


class Tier(Enum):
    FREE = "free"
    PRO = "pro"
    MANAGED = "managed"


UNLIMITED = float("inf")


class Counter:
    def __init__(
        self, timedelta_: timedelta, redis_host: str, redis_port: int = 6379
    ):
        self.redis_client = Redis(redis_host, redis_port)
        self.timedelta_ = timedelta_

    def incr(self, key: str) -> None:
        if self.redis_client.exists(key):
            self.redis_client.incr(key)
        else:
            self.redis_client.set(key, 1, ex=self.timedelta_)

    def get(self, key: str) -> int:
        return int(self.redis_client.get(key) or 0)


class ValidateRateLimitRedis:
    def __init__(
        self,
        rate_id: str,
        tier_limits: Dict[Tier, float],
        timedelta_: timedelta,
        redis_host: str,
        redis_port: int = 6379,
    ):
        assert (
            Tier.FREE in tier_limits and Tier.PRO in tier_limits
        ), f"ValidateRateLimit.tier_limits must declare rate limits for :: {Tier.FREE} and {Tier.PRO}"  # noqa

        self.rate_id = rate_id
        self.counter = Counter(timedelta_, redis_host, redis_port)

        # Set special tier limits
        self.tier_limits = tier_limits
        self.tier_limits[Tier.MANAGED] = UNLIMITED

    def validate_user_rate(self, user_id: str) -> None:
        if not ENABLE_RATE_LIMIT:
            return

        key = f"{user_id}/{self.rate_id}"

        # Get user data
        with ThreadPoolExecutor(max_workers=2) as executor:
            user_tier_f = executor.submit(self.get_user_tier, user_id)
            user_rate_f = executor.submit(self.counter.get, key)
            user_tier = user_tier_f.result()
            user_rate = user_rate_f.result()

        # Check rate limit
        rate_limit = self.tier_limits.get(user_tier, -1)
        if user_rate >= rate_limit:
            raise RateLimitException(self.rate_id, rate_limit, user_rate)

        # Update user rate
        self.counter.incr(key)

    @abstractmethod
    def get_user_tier(self, user_id: str) -> Tier:
        ...


from mh_logger import LoggingManager  # noqa

global_logger = LoggingManager(__name__)


@dataclass
class UserRate:
    user_id: str
    rate_id: str
    rate: int


class TierRate(NamedTuple):
    tier: Tier
    rate: int


class ValidateRateLimit:
    def __init__(
        self,
        rate_id: str,
        tier_limits: Dict[Tier, int],
        timedelta_: timedelta,
        service_name: Optional[str],
        project: str,
        resource_type: str = "cloud_run_revision",
        location: Optional[str] = "us-central1",
        severity: Optional[str] = "INFO",
        logger: Optional[LoggingManager] = None,
    ):
        assert (
            Tier.FREE in tier_limits and Tier.PRO in tier_limits
        ), f"ValidateRateLimit.tier_limits must declare rate limits for :: {Tier.FREE} and {Tier.PRO}"  # noqa

        self.rate_id = rate_id
        self.timedelta_ = timedelta_
        self.service_name = service_name
        self.project = project
        self.resource_type = resource_type
        self.location = location
        self.severity = severity
        if logger:
            self._logger = logger
        else:
            self._logger = global_logger

        # Set special tier limits
        self.tier_limits = tier_limits
        self.tier_limits[Tier.MANAGED] = 1_000_000

    def validate_user_rate(self, user_id: str) -> None:
        approx_user_rate = self.get_approx_user_rate(user_id, self.rate_id)
        if not approx_user_rate:
            raise RateLimitException(
                self.rate_id,
                None,
                None,
                hint=f"Rate limit id :: {self.rate_id} not found for user :: {user_id}.",  # noqa
            )

        # Will run in the background
        Thread(
            target=self.update_user_rate, args=[user_id, approx_user_rate.tier]
        ).start()

        rate_limit = self.tier_limits.get(approx_user_rate.tier, -1)
        if approx_user_rate.rate < rate_limit:
            return
        raise RateLimitException(
            self.rate_id, rate_limit, approx_user_rate.rate
        )

    def update_user_rate(self, user_id: str, tier: Tier) -> None:
        """
        WARNING: This method is expensive.
                 The more filters in `list_entries`, the better.

        Retrieves all log entries for a given set of filters
        and counts them against the rate_limit.
        """

        # We need the raw GCP logging client, as opposed to the wrapper
        gcp_logging_client = self._logger.gcp_logging_client
        if not gcp_logging_client:
            # Local dev most likely
            return

        time_window_start = datetime.now(timezone.utc) - self.timedelta_
        n = min(self.tier_limits.get(tier, 10_000), 10_000)
        # Returns all logging entries for timestamp >= time_window_start
        # WARNING: This method is expensive. The more filters, the better.
        filters = f"""
            jsonPayload.rate_id = {self.rate_id}
            AND jsonPayload.user_id = {user_id}
            AND resource.type = "{self.resource_type}"
            AND timestamp >= "{time_window_start.isoformat()}"
        """
        if self.service_name:
            filters += (
                f'\nAND resource.labels.service_name = "{self.service_name}"'
            )
        if self.location:
            filters += f'\nAND resource.labels.location = "{self.location}"'
        if self.severity:
            filters += f'\nAND severity = "{self.severity}"'
        usage_logs = list(
            gcp_logging_client.list_entries(
                resource_names=[f"projects/{self.project}"],
                filter_=filters,
                order_by="timestamp desc",  # Assumption: This is expensive
                page_size=n,
                max_results=n,
            )
        )

        self.save_user_rate(UserRate(user_id, self.rate_id, len(usage_logs)))

    def __call__(
        self,
        user_id: str,
        request: Dict[str, Any],
        downstream_method,
        url,
    ):
        """
        Validates user usage and logs it.
        Will be used for a FastAPI dependency.
        """

        self.validate_user_rate(user_id)  # Throws

        # This is the actual usage counter
        self._logger.info(
            url.path,
            rate_id=self.rate_id,
            module=downstream_method.__module__,
            method=downstream_method.__name__,
            endpoint=url.path,
            request=request,
            user_id=user_id,
        )

    def enforce_user_rate(self, user_id: str) -> None:
        "Validates user usage and logs it."

        self.validate_user_rate(user_id)  # Throws

        caller_module, caller_function = _get_original_caller_info()

        # This is the actual usage counter
        self._logger.info(
            f"Rate limit {caller_module}.{caller_function}",
            rate_id=self.rate_id,
            module=caller_module,
            method=caller_function,
            user_id=user_id,
        )

    @abstractmethod
    def get_approx_user_rate(
        self, user_id: str, rate_id: str
    ) -> Optional[TierRate]:
        ...

    @abstractmethod
    def save_user_rate(self, user_rate: UserRate) -> None:
        ...


def _get_original_caller_info() -> Tuple[Optional[str], Optional[str]]:
    module_name = None
    function_name = None

    current = inspect.currentframe()
    if current:
        caller = current.f_back
        if caller:
            caller = caller.f_back
            if caller:
                module = inspect.getmodule(caller)
                if module:
                    module_name = module.__name__
                function_name = caller.f_code.co_name
    return module_name, function_name
