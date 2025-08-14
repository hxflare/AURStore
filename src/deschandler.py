import requests
import markdown
class Desc:
    def transform_url(self,url):
        urlparts=url.rstrip('/').split('/')
        apiurl=f"https://api.github.com/repos/{urlparts[-2]}/{urlparts[-1]}"
        print("fetching the main branch...")
        apiresponse=requests.get(apiurl)
        repoinfo=apiresponse.json()
        print(f"main branch: {repoinfo.get("default_branch","main")}")
        reformedUrl=f"https://raw.githubusercontent.com/{urlparts[-2]}/{urlparts[-1]}/{repoinfo.get("default_branch","main")}/README.md"
        print(f"reformed url to: {reformedUrl}")
        return reformedUrl
    def open_md(self,url):
        print("getting by url: "+url)
        get=requests.get(f"{self.transform_url(url=url)}")
        content=get.text
        html_content=markdown.markdown(content)
        return html_content
    def getHtml(self,link):
        if link.startswith("https://github.com/"):
            return self.open_md(url=link)
        else:
            return "<h1>DESCRIPTION NOT FOUND</h1>"