#include "opencv2/opencv.hpp"
using namespace std;
using namespace cv;

int main(int, char**)
{
	VideoCapture cap(1); // open the default camera
	if (!cap.isOpened())  // check if we succeeded
	{
		cout << "ERROR: There is no web-camera to connect!" << endl;
		return -1;
	}
		
	//-- Выставляем параметры камеры ширину и высоту кадра в пикселях
	cap.set(CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(CAP_PROP_FRAME_HEIGHT, 960);

	Mat frame;
	int i = 1;
	while (true) {
		cap >> frame; //-- захватываем очередной кадр
		string filename =to_string(i) + ".jpeg";
		imwrite(filename, frame); //--cохраняем в файл

		char c = waitKey(33); //-- если была нажата клавиша, узнаём её код

		if (c == 27) { //-- нажата ESC, прерываем цикл
			break;
		}
		i++;
	}

	
	// the camera will be deinitialized automatically in VideoCapture destructor
	return 0;
}