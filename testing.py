import requests
import markdown
def transform_url(url):
    urlparts=url.rstrip('/').split('/')
    apiurl=f"https://api.github.com/repos/{urlparts[-2]}/{urlparts[-1]}"
    print(apiurl)
    apiresponse=requests.get(apiurl)
    repoinfo=apiresponse.json()
    print(f"main branch: {repoinfo.get("default_branch","main")}")
    reformedUrl=f"https://raw.githubusercontent.com/{urlparts[-2]}/{urlparts[-1]}/{repoinfo.get("default_branch","main")}/README.md"
    print(reformedUrl)
    return reformedUrl
def open_md(url):
    get=requests.get(f"{url}/README.md").raise_for_status()
    content=get.text
    html_content=markdown.markdown(content)
    print(content)
    print(html_content)
response=requests.get(transform_url(input("url: ")))
print(response.text)