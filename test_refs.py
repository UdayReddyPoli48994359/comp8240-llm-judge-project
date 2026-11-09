# Test 1003 fixed binary_search
def binary_search(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1

def insertion_point(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

arr = [1,3,5,7,9,11]
assert binary_search(arr, 7) == 3
assert binary_search(arr, 1) == 0
assert binary_search(arr, 11) == 5
assert binary_search(arr, 4) == -1
assert insertion_point(arr, 4) == 2
assert insertion_point(arr, 0) == 0
assert insertion_point(arr, 12) == 6
assert insertion_point(arr, 5) == 2  # leftmost
print("1003 OK")

# Test 1007 is_balanced
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

assert is_balanced("([{}])") == True
assert is_balanced("([)]") == False
assert is_balanced("") == True
assert is_balanced("(") == False
print("1007 part1 OK")

import re
def is_balanced_with_tags(s):
    stripped = re.sub(r'</?[a-zA-Z0-9]+>', '', s)
    if not is_balanced(stripped):
        return False
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

assert is_balanced_with_tags("<div>(hello)</div>") == True
assert is_balanced_with_tags("<div>(hello</div>)") == True  # brackets balanced overall, tags balanced
assert is_balanced_with_tags("<div><span></div></span>") == False
assert is_balanced_with_tags("<div>") == False
print("1007 part2 OK")

# Test 1001 linked list cycle
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None
    ptr = head
    while ptr is not slow:
        ptr = ptr.next
        slow = slow.next
    return ptr

a,b,c,d = Node(1), Node(2), Node(3), Node(4)
a.next, b.next, c.next, d.next = b, c, d, b  # cycle back to b
assert has_cycle(a) == True
assert detect_cycle_start(a) is b
e,f = Node(1), Node(2)
e.next = f
assert has_cycle(e) == False
assert detect_cycle_start(e) is None
print("1001 OK")

# Test 1004-style dense_rank logic conceptually via sqlite3
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE employees(id INTEGER, name TEXT, department TEXT, salary INTEGER)")
rows = [(1,'A','Eng',100),(2,'B','Eng',90),(3,'C','Eng',90),(4,'D','Eng',80),
        (5,'E','Sales',70),(6,'F','Sales',60)]
conn.executemany("INSERT INTO employees VALUES (?,?,?,?)", rows)
q = """
SELECT department, name, salary
FROM (
    SELECT department, name, salary,
           DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;
"""
res = conn.execute(q).fetchall()
print("1004 result:", res)
assert set(res) == {('Eng','B',90), ('Eng','C',90), ('Sales','F',60)}
print("1004 OK")

# Test 1002 top5_ips (turn 1: bounded-by-distinct-IPs) and ApproxTop5 (turn 2: fixed memory)
import heapq
from collections import Counter
import tempfile, os

def top5_ips(path):
    counts = Counter()
    with open(path) as f:
        for line in f:
            ip = line.strip()
            if ip:
                counts[ip] += 1
    return heapq.nlargest(5, counts.items(), key=lambda kv: kv[1])

# temp-file-backed test: known frequencies, written to disk, never fully loaded into memory as a list
ip_lines = (
    ["10.0.0.1"] * 50 + ["10.0.0.2"] * 40 + ["10.0.0.3"] * 30 +
    ["10.0.0.4"] * 20 + ["10.0.0.5"] * 10 + ["10.0.0.6"] * 1
)
fd, tmp_path = tempfile.mkstemp()
with os.fdopen(fd, "w") as f:
    f.write("\n".join(ip_lines) + "\n")
try:
    top5 = top5_ips(tmp_path)
    assert top5 == [
        ("10.0.0.1", 50), ("10.0.0.2", 40), ("10.0.0.3", 30),
        ("10.0.0.4", 20), ("10.0.0.5", 10),
    ]
finally:
    os.remove(tmp_path)
print("1002 part1 OK")

class ApproxTop5:
    def __init__(self, width=2000, depth=4):
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]
        self.top = {}

    def _hashes(self, ip):
        return [(hash((i, ip)) % self.width) for i in range(self.depth)]

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

# fixed candidate set: a clear winner should survive eviction and come out on top
approx = ApproxTop5()
candidates = ["a", "b", "c", "d", "e", "f", "g"]
for ip, n in zip(candidates, [100, 80, 60, 40, 20, 5, 1]):
    for _ in range(n):
        approx.add(ip)
top5_approx = approx.top5()
assert top5_approx[0][0] == "a"
assert {ip for ip, _ in top5_approx} <= set(candidates)
assert len(top5_approx) == 5
print("1002 part2 OK")

# Test 1005 race condition: racy counter vs. locked counter
import threading

def racy_increment(counter_box, n):
    for _ in range(n):
        counter_box[0] += 1

N_ITERS = 200_000
N_THREADS = 4
box = [0]
threads = [threading.Thread(target=racy_increment, args=(box, N_ITERS)) for _ in range(N_THREADS)]
for t in threads: t.start()
for t in threads: t.join()
# racy version: only checked for a plausible range (lost updates expected, never negative/over)
assert 0 < box[0] <= N_ITERS * N_THREADS

lock = threading.Lock()
def locked_increment(counter_box, n):
    for _ in range(n):
        with lock:
            counter_box[0] += 1

box2 = [0]
threads2 = [threading.Thread(target=locked_increment, args=(box2, N_ITERS)) for _ in range(N_THREADS)]
for t in threads2: t.start()
for t in threads2: t.join()
# locked version: asserted exact every run
assert box2[0] == N_ITERS * N_THREADS
print("1005 OK")

# Test 1006 token-bucket rate limiter: 100-thread concurrency stress test
import time

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

CAPACITY = 10
bucket = TokenBucket(capacity=CAPACITY, refill_rate=0)  # no refill during the burst
results = []
results_lock = threading.Lock()

def worker():
    allowed = bucket.allow_request()
    with results_lock:
        results.append(allowed)

stress_threads = [threading.Thread(target=worker) for _ in range(100)]
for t in stress_threads: t.start()
for t in stress_threads: t.join()
assert sum(1 for r in results if r) == CAPACITY
print("1006 OK")

# Test 1008 haversine closest-pair: real-world coordinate pairs
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

def haversine(p1, p2):
    lat1, lon1 = map(radians, p1)
    lat2, lon2 = map(radians, p2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * atan2(sqrt(a), sqrt(1 - a))

def closest_pair(points):
    best = None
    best_dist = float("inf")
    for p1, p2 in combinations(points, 2):
        d = haversine(p1, p2)
        if d < best_dist:
            best_dist, best = d, (p1, p2)
    return best, best_dist

sydney_opera_house = (-33.8568, 151.2153)
bondi_beach = (-33.8908, 151.2743)
melbourne_cbd = (-37.8136, 144.9631)

d_opera_bondi = haversine(sydney_opera_house, bondi_beach)
assert 5.5 < d_opera_bondi < 7.5  # known approx ~6.4km

points = [sydney_opera_house, bondi_beach, melbourne_cbd]
pair, dist = closest_pair(points)
assert set(pair) == {sydney_opera_house, bondi_beach}
assert dist < 10  # the Sydney pair, not the ~713km Melbourne leg
print("1008 OK")

print("ALL 8 REFERENCE ANSWERS VERIFIED")
