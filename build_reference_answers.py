import json, uuid, time

def aid():
    return uuid.uuid4().hex[:22]

refs = [
{
 "question_id": 1001,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""Use Floyd's cycle-detection algorithm (slow/fast pointers), which needs only two extra pointer variables, i.e. O(1) extra space:

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```
`fast` moves twice as fast as `slow`; if there is a cycle they must eventually meet inside it. If `fast` reaches the end (`None`), there is no cycle.""",
"""To find the start of the cycle, after `slow` and `fast` meet, reset one pointer to `head` and advance both one step at a time; they meet again exactly at the cycle's start node (a standard consequence of the distance math in Floyd's algorithm):

```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle
    ptr = head
    while ptr is not slow:
        ptr = ptr.next
        slow = slow.next
    return ptr
```
This still uses only O(1) extra space and runs in O(n) time."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1002,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""Stream the file line by line (never load it all into memory) and maintain counts with a dictionary, then use a size-5 heap to get the top-5 without sorting everything:

```python
import heapq
from collections import Counter

def top5_ips(path):
    counts = Counter()
    with open(path) as f:
        for line in f:
            ip = line.strip()
            if ip:
                counts[ip] += 1
    return heapq.nlargest(5, counts.items(), key=lambda kv: kv[1])
```
Memory use is O(number of distinct IPs), not O(number of lines), which is usually much smaller than the file itself.""",
"""For a truly unbounded/infinite stream, even the distinct-IP dictionary can grow without bound, so we switch to an approximate, fixed-memory sketch, e.g. Count-Min Sketch plus a small heap to track current top-5 candidates:

```python
import heapq

class ApproxTop5:
    def __init__(self, width=2000, depth=4):
        self.width, self.depth = width, depth
        self.table = [[0]*width for _ in range(depth)]
        self.top = {}  # small fixed-size candidate set

    def _hashes(self, ip):
        return [ (hash((i, ip)) % self.width) for i in range(self.depth) ]

    def add(self, ip):
        for i, h in enumerate(self._hashes(ip)):
            self.table[i][h] += 1
        est = min(self.table[i][h] for i, h in enumerate(self._hashes(ip)))
        self.top[ip] = est
        if len(self.top) > 5:
            worst = min(self.top, key=self.top.get)
            del self.top[worst]

    def top5(self):
        return sorted(self.top.items(), key=lambda kv: -kv[1])
```
Trade-off: counts become approximate (can overestimate due to hash collisions) and very-low-frequency IPs may be evicted early, but memory is bounded regardless of stream length."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1003,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""The bug is in the branch where `arr[mid] < target`: the code sets `hi = mid`, which narrows the search into the wrong half (it should move `lo` up, not shrink `hi`). As written, when the target is greater than `arr[mid]`, the search space shrinks away from where the target actually is, and will miss it. Fixed version:

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1   # fixed: move lo up, not hi down
        else:
            hi = mid
    return -1
```""",
"""```python
def insertion_point(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```
This is the standard "leftmost insertion point" binary search: it converges `lo` to the first index where `target` could be inserted while keeping the array sorted, whether or not `target` is already present."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1004,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""```sql
SELECT department, salary AS second_highest_salary
FROM (
    SELECT department, salary,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;
```
`DENSE_RANK()` is used rather than `ROW_NUMBER()` so that genuine ties at the top don't skip rank 2.""",
"""The query above already returns every employee tied for rank 2 in each department, because `DENSE_RANK()` assigns the same rank to tied salaries rather than a unique sequential number (which is what `ROW_NUMBER()` would do). If employee names are needed too:

```sql
SELECT department, name, salary
FROM (
    SELECT department, name, salary,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;
```
This returns all rows tied for second-highest salary per department, not just one."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1005,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""A race condition happens when multiple threads access and modify shared state without synchronization, and the final result depends on the unpredictable order in which their operations interleave. Example with an unsynchronized counter:

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1   # not atomic: read, add, write

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # often less than 400000
```
`counter += 1` is really three steps (read, add, store); two threads can interleave these steps and overwrite each other's update, so the final count is usually less than the expected 400000.""",
"""Fix it with a lock so the read-modify-write sequence becomes atomic with respect to other threads:

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # always 400000
```
The lock ensures only one thread can execute the read-modify-write sequence at a time, so no update is ever lost."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1006,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def allow_request(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```""",
"""As written, `allow_request()` is not thread-safe: two threads could both read `self.tokens >= 1` as True before either decrements it, letting both requests through when only one token was available (a race condition on `self.tokens`). Fix with a lock around the check-and-decrement:

```python
import threading, time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def allow_request(self):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
```
For use across multiple *processes* (not just threads), an in-process lock is not enough — you'd need a shared store such as Redis with an atomic operation (e.g. a Lua script or `INCR`/`EXPIRE`) instead."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1007,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""```python
def is_balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
```""",
"""```python
import re

def is_balanced_with_tags(s):
    # First check bracket balance on the string with tags stripped out
    stripped = re.sub(r'</?[a-zA-Z0-9]+>', '', s)
    if not is_balanced(stripped):
        return False
    # Then check tag balance using a stack, ignoring brackets
    stack = []
    for tag in re.findall(r'</?[a-zA-Z0-9]+>', s):
        if tag.startswith('</'):
            name = tag[2:-1]
            if not stack or stack.pop() != name:
                return False
        else:
            name = tag[1:-1]
            stack.append(name)
    return not stack
```
This treats brackets and tags as two independent balance checks, which is sufficient for the simplified (no-attribute) tag format described."""
 ]}],
 "tstamp": time.time()
},
{
 "question_id": 1008,
 "answer_id": aid(), "model_id": "reference",
 "choices": [{"index": 0, "turns": [
"""```python
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

def haversine(p1, p2):
    lat1, lon1 = map(radians, p1)
    lat2, lon2 = map(radians, p2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * atan2(sqrt(a), sqrt(1 - a))  # km

def closest_pair(points):
    best = None
    best_dist = float('inf')
    for p1, p2 in combinations(points, 2):
        d = haversine(p1, p2)
        if d < best_dist:
            best_dist, best = d, (p1, p2)
    return best, best_dist
```
This brute-force approach checks every pair, so it is O(n^2).""",
"""To beat O(n^2), use a divide-and-conquer closest-pair algorithm (classic computational-geometry technique, O(n log n)): sort points by longitude, recursively solve both halves, then only check a narrow strip near the dividing line for pairs that could beat the best distance found so far. The trade-off is implementation complexity: the planar divide-and-conquer algorithm assumes a roughly flat-earth approximation for the strip-merge step, which is only accurate for points that are relatively close together; for points spread across the globe, the small-angle approximation breaks down and a spatial index (e.g. a k-d tree or geohash-based grid) is usually a simpler, more robust way to prune the search than adapting the classic algorithm directly."""
 ]}],
 "tstamp": time.time()
},
]

with open("/tmp/comp8240/new_data/reference_answer_additions.jsonl", "w") as f:
    for r in refs:
        f.write(json.dumps(r) + "\n")

print(f"Wrote {len(refs)} reference answers")
