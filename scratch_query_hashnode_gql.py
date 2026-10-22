import urllib.request
import json

gql_url = "https://gql.hashnode.com"
query = """
query {
  post(id: "cmvjz00bn000f09kz8zrpae9i") {
    id
    title
    slug
    url
    canonicalUrl
    publication {
      id
      title
      url
    }
  }
}
"""

req = urllib.request.Request(
    gql_url,
    data=json.dumps({"query": query}).encode('utf-8'),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print("Hashnode GQL Post:", json.dumps(res, indent=2))
except Exception as e:
    print("GQL error:", e)
