def get_location():
    print("generating location through kalman filter")
    return 0,0

if __name__ == "__main__":
    x,y = get_location()
    print(f"Your vehicle is at {x}, {y}")