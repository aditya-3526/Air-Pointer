import sys
from camera_test import test_camera
from hand_detection import detect_hands
from airpointer import AirPointer

def main():
    print("=== AirPointer: Hand Gesture Navigation System ===")
    print("1. Test Camera")
    print("2. Test Hand Detection")
    print("3. Launch AirPointer")
    print("4. Exit")
    
    choice = input("Select an option (1-4): ")
    
    if choice == '1':
        test_camera()
    elif choice == '2':
        detect_hands()
    elif choice == '3':
        air_pointer = AirPointer()
        air_pointer.run()
    elif choice == '4':
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
    
    # Restart the menu after each action
    main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting AirPointer...")
        sys.exit(0)