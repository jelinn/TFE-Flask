from flask import Flask, request, render_template, flash
import pyterprise
import os

DEBUG = True
app = Flask(__name__, template_folder="templates")
  
# Set up pyterprise for TFC API
client = pyterprise.Client()
client.init(token='uG3WXbx9eyJJgw.atlasv1.pe0WsMiPRzExycGXlLLSGylmyxIOe3PF3xl9QZVOlenVAp6TlD8VNMzLBwj1PzEHm84', url='https://app.terraform.io')
org = client.set_organization(id='jlinn-alt-test')


#Capabilities
# 1. Create a workspace
# 2. Run a plan / apply
# 3. Run a destroy
# 4. Delete a workspace 

@app.route('/')
def home():
  return render_template("index.html", message = "Self Service Infrastructure Portal")


@app.route('/create-workspace')
def createWorkspace():
    return render_template("create.html")

@app.route("/create", methods=['POST'])
def create():
  workspaceName = request.form['workspaceName']
  repo = request.form['repository']
  repo="jelinn/"+repo
  print("Created \n: repo="+repo)
  print("name = "+ workspaceName)
  vcs_options = {
    "identifier": repo,
    "oauth-token-id": "ot-AwB8YsDCs5XMnB8S",
    "branch": "master",
    "default-branch": False
  }
  org.create_workspace(name=workspaceName,
                vcs_repo=vcs_options,
                auto_apply=False,
                queue_all_runs=False,
                working_directory='/')

  return render_template('/', message="Successfully created Workspace")

@app.route("/list-workspaces")
def list():
  return render_template('workspaces.html', workspaces=org.list_workspaces() )

@app.route("/createrun")
def createRun():
  return render_template('run.html', workspaces=org.list_workspaces())

@app.route("/run", methods=['GET','POST'])
def run():
  workspace = org.get_workspace(request.form['workspaceName'])
  run = workspace.run(message="Testing self-service portal", destroy_flag=False)
  return render_template('runstatus.html', plan=run.get_plan_output())

@app.route("/details")
def getDetails():
  return render_template('/', workspaces=org.list_workspaces() )

@app.route("/delete-workspace")
def deleteWorksace():
    return render_template('delete.html', workspaces=org.list_workspaces())

@app.route("/delete", methods=['POST'])
def delete():
    workspaceName = request.form['workspaceName']
    org.delete_workspace(name=workspaceName)
    return render_template('index.html', message="Successfully deleted workspace")

if __name__ == '__main__':
  app.run()
