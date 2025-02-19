import uvicorn

# run the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", workers=4, reload=True)
