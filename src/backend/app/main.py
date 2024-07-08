import uvicorn


def print_hello_world():
    print("Hello AI World #1!!!")


if __name__ == '__main__':
    print_hello_world()

    uvicorn.run("fast_api:app", app_dir="../fast_api", host="127.0.0.1", port=5000, reload=True)
