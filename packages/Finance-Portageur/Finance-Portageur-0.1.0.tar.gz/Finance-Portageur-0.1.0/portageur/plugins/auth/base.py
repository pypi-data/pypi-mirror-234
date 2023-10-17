import time, random, pdb, math
from dataclasses import dataclass, field
from typing import Optional

REQUESTS_PER_MIN_LIMIT = 10
TOKENS_PER_MIN_LIMIT = 4000


@dataclass
class StatusTracker:
    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0
    num_tasks_succeeded: int = 0
    num_tasks_failed: int = 0
    num_rate_limit_errors: int = 0
    num_api_errors: int = 0
    num_other_errors: int = 0
    time_of_last_rate_limit_error: int = 0


@dataclass
class RateLimitTracker:
    next_request_time: int = 0
    seconds_to_pause_after_rate_limit_error: int = 10
    seconds_to_sleep_each_loop: int = 0.001
    available_request_capacity: int = REQUESTS_PER_MIN_LIMIT
    available_token_capacity: int = TOKENS_PER_MIN_LIMIT
    last_update_time: int = time.time()


@dataclass
class BaseAuth:
    status_tracker: StatusTracker = field(default_factory=StatusTracker)
    ratelimit_tracker: RateLimitTracker = field(
        default_factory=RateLimitTracker)
    proxy: Optional[str] = None
    is_okay: bool = True
    is_use: bool = True
    weight: int = 1  # 默认权重，通过StatusTracker  RateLimitTracker实现权重

    def refresh(self):
        w = 0.6
        self.weight = w * self.status_tracker.num_tasks_in_progress + (
            1 - w) * self.status_tracker.num_tasks_succeeded

    def __enter__(self):
        self.status_tracker.num_tasks_in_progress += 1
        self.refresh()
        print(
            "start auth_index:{0},weight:{1},num_tasks_in_progress:{2},num_tasks_succeeded:{3}"
            .format(self.auth_index, round(self.weight, 2),
                    self.status_tracker.num_tasks_in_progress,
                    self.status_tracker.num_tasks_succeeded))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.status_tracker.num_tasks_in_progress -= 1
        self.status_tracker.num_tasks_succeeded += 1
        self.refresh()


class ChatModelManager(object):

    def __init__(self, config_path):
        self.auths = []

    def auth_config(self, node_data, auth_class):
        auths = []
        for key, value in node_data.items():
            requests_per_min = value.pop('requests_per_min',
                                         REQUESTS_PER_MIN_LIMIT)
            tokens_per_min = value.pop('tokens_per_min', TOKENS_PER_MIN_LIMIT)
            auths.append(
                auth_class(auth_index=len(auths) + 1000,
                           ratelimit_tracker=RateLimitTracker(
                               available_request_capacity=requests_per_min,
                               available_token_capacity=tokens_per_min),
                           **value))
        return auths

    def create_weight(self):
        self.auths = [auth for auth in self.auths]

    def available_auth(self):
        for auth in self.auths:
            if auth.is_okay and not auth.in_use:
                auth.in_use = True
                return auth

    ## 随机加权
    def idle_auth(self):
        total_weight = sum(auth.weight for auth in self.auths)
        cumulative_weight = 0
        #rand = random.randint(1, math.floor(total_weight))
        rand = random.uniform(0, total_weight)
        for auth in self.auths:
            cumulative_weight += 1 / auth.weight
            if rand <= cumulative_weight:
                return auth
        ## 请求正确最高(暂未加入失败请求统计)
        print("not idle auth")
        return sorted(self.auths,
                      key=lambda x: x.status_tracker.num_tasks_succeeded)[0]
