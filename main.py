from internal.detector import Detector
from internal.params import params

def main():
    detector = Detector(params.URL)

    detector.run()


if __name__ == '__main__':
    main()