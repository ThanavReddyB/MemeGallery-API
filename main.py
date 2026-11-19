import uvicorn

#use webserver uvicorn
if __name__ == "__main__":
    # run a webserver, run an api on it [app.app is app in folder app in file app]
    # host is domainyou want to run your server on(run on any available domain)
    uvicorn.run("app.app:app",host="0.0.0.0",port=8000,reload=True)