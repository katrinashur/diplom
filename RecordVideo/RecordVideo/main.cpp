#include "opencv2/opencv.hpp"
#include <windows.h>
#include <stdio.h>
using namespace std;
using namespace cv;

int main(int, char**)
{
	VideoCapture cap(0); // open the default camera
	if (!cap.isOpened())  // check if we succeeded
	{
		cout << "ERROR: There is no web-camera to connect!" << endl;
		return -1;
	}
		
	//-- Выставляем параметры камеры ширину и высоту кадра в пикселях
	cap.set(CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(CAP_PROP_FRAME_HEIGHT, 960);

	Mat frame;
	while (true) {
		SYSTEMTIME st;	
		cap >> frame; //-- захватываем очередной кадр
		GetLocalTime(&st);

		string filename = to_string(st.wYear) +"-"+ to_string(st.wMonth)+ "-" + to_string(st.wDay) + " " +
			to_string(st.wHour) + "_"+ to_string(st.wMinute)+"_"+ to_string(st.wSecond) + "_" + to_string(st.wMilliseconds) + ".jpeg";
		imwrite(filename, frame); //--cохраняем в файл

		char c = waitKey(33); //-- если была нажата клавиша, узнаём её код

		if (c == 27) { //-- нажата ESC, прерываем цикл
			break;
		}
	}

	
	// the camera will be deinitialized automatically in VideoCapture destructor
	return 0;
}