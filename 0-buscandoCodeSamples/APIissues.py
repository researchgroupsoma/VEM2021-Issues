from github import Github
from datetime import datetime
#g = Github("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")
#g = Github("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")
g = Github("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")
import pandas as pd

def getAllIssuesRequests(sample):
  repo = g.get_repo(sample)
  print(sample)
  issues = []
  for issue in repo.get_issues(state = 'all'):
    if "/issues/" in issue.html_url: 
      issues.append(issue)

  return issues


def getDataframe(dataframe, framework, sample, issues):
  return dataframe.append(other=[
                              {
                                "framework" : framework,
                                "sample": sample,
                                "data de fechamento": Issue.closed_at,
                                "data de criação": Issue.created_at,
                                "tempo para fechamento": (Issue.closed_at - Issue.created_at).days if Issue.closed_at != '' and Issue.closed_at is not None else "",
                                "labels": [label.name for label in Issue.labels],
                                "state": Issue.state,
                                "update_at": Issue.updated_at,
                                "titulo": Issue.title,
                                "number": Issue.number,
                                "html-url": Issue.html_url,
                                "creator user cargo": Issue.user.role,
                                "creator user empresa": Issue.user.company,
                                "creator user local": Issue.user.location, 
                                "creator user login": Issue.user.login,
                                "creator user email": Issue.user.email,
                                "creator user seguidores": Issue.user.followers,
                                "creator user tempo no GitHub": (Issue.created_at - Issue.user.created_at).days,
                                "closed user cargo": Issue.closed_by.role if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user empresa": Issue.closed_by.company if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user local": Issue.closed_by.location if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user login": Issue.closed_by.login if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user email": Issue.closed_by.email if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user seguidores": Issue.closed_by.followers if Issue.state == "closed" and Issue.closed_by is not None else "",
                                "closed user tempo no GitHub":(Issue.closed_at - Issue.closed_by.created_at).days if Issue.state == "closed" and Issue.closed_by is not None else "" ,
                                } for Issue in issues])


def export(dataframe):
  dataframe.to_csv("Spring-Issues.csv")



def main():
  samples = pd.read_csv("rep.txt", names=["sample"])
  dataframe = pd.DataFrame(columns=["framework","sample","data de fechamento","data de criação",
                                  "tempo para fechamento","labels","state","update_at",
                                  "titulo","number", "html-url","creator user cargo","creator user empresa",
                                  "creator user local", "creator user login","creator user email","creator user seguidores",
                                  "creator user tempo no GitHub","closed user cargo","closed user empresa",
                                  "closed user local", "closed user login","closed user email","closed user seguidores",
                                  "closed user tempo no GitHub"])
  for sample in samples["sample"]:
    framework = sample.split("/")
    framework = framework[0]
    issues = getAllIssuesRequests(sample)
    dataframe = getDataframe(dataframe, framework, sample, issues)

  export(dataframe) 
  
if __name__ == "__main__":
    main()

  
  

