from minusFunction import minusFunction
import sys
if __name__ == "__main__":
    # functionName = "OCR"
    functionName = sys.argv[1]
    token = sys.argv[2]
    minusFunction(functionName, token)