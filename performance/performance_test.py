import requests
import json
import time
import matplotlib.pyplot as plt

N = 62 ** 2
samples = []

urls = set()

for _ in range(N):
    start_time = time.time()
    response = requests.post(
        "http://localhost:8080",
        data=json.dumps(
            {"long_url": f"http://test_url_doesnt_matter.com"}
        )
    )
    short_url = response.json()["short_url"]
    print(short_url)
    assert short_url not in urls, f"URL {short_url} is repeated"
    urls.add(short_url)
    samples.append(
        time.time() - start_time
    )

plt.figure("Time to compute new URL")
plt.plot(list(range(N)), samples)
plt.xlabel("Request ID")
plt.ylabel("Elapsed time (seconds)")

plt.savefig("performance.png")