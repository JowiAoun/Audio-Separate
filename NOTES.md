Useful:
- Venv activate: `source venv/bin/activate`
- Venv deactivate: `deactivate`
- `FastAPI server with automatic reload: uvicorn main:app --reload`
- Spleeter separate (2 stems): `spleeter separate -p spleeter:2stems -o ./output ./input/FILENAME`
- Destroy process: `sudo lsof -t -i tcp:8000 | xargs kill -9`
- NOTE: Requires Python 3.8.19

Next steps:
- Research file search and access pattern & hashing
- Limit request numbers for the file to 3 times max
- Save files to /output/job_name (or hash code?)
- Figure out how to create a new spleeter job, asynchronously (see multi-threading)
- Implement logging with CloudWatch
- Add a job progress websocket/endpoint then redirect from post request if redirect parameter is passed
- Add error & logging checks to AWS functions

Before deployment:
- Change AWS root user access key to user with the least privilege and DELETE ROOT USER ACCESS KEY IN IAM
- Reduce app size as much as possible
  - Research tensorflow lite translation
- Create tests
- Containerize & Test
- Calculate prices of AWS and make a PDF of charts and data
