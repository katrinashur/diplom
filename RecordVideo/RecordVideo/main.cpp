#include "opencv2/opencv.hpp"
#include <windows.h>
#include <stdio.h>
#include <fstream>
#include <atlstr.h>
using namespace std;
using namespace cv;



int  main(int argc, char* argv[])
{
	HANDLE   hNamedPipe;
	char     pchMessage[1] = {};   // для сообщения
	int    nMessageLength;   // длина сообщения
	char  pchResponse[80];
	int responseCode = 0;

	SYSTEMTIME st;
	

	if (argc < 4)
	{
		cout << "Not enough arguments!" << endl;
		return -1;
	}

	string experimentPath(argv[3]);
	string experimentName(argv[2]);
	char pipeName[50];
	strcpy_s(pipeName, argv[1]);

	// создаем именованный канал для чтения и записи
	hNamedPipe = CreateNamedPipe(
		pipeName,  // имя канала
		PIPE_ACCESS_INBOUND,        // читаем из канала 
		PIPE_TYPE_MESSAGE | PIPE_WAIT,   // синхронная передача сообщений
		1,         // максимальное количество экземпляров канала 
		0,         // размер выходного буфера по умолчанию
		0,         // размер входного буфера по умолчанию
		INFINITE,  // клиент ждет связь бесконечно долго
		NULL       // безопасность по умолчанию
	);
	// проверяем на успешное создание
	if (hNamedPipe == INVALID_HANDLE_VALUE)
	{
		cerr << "Create named pipe failed." << endl
			<< "The last error code: " << GetLastError() << endl;
		cout << "Press any key to exit.";
		cin.get();

		return 0;
	}

	// ждем, пока клиент свяжется с каналом
	cout << "The record video process is waiting for connection with a EEGToeEmotionTool." << endl;
	if (!ConnectNamedPipe(
		hNamedPipe,    // дескриптор канала
		NULL      // связь синхронная
	))
	{
		cerr << "Connect named pipe failed." << endl
			<< "The last error code: " << GetLastError() << endl;
		CloseHandle(hNamedPipe);
		cout << "Press any key to exit.";
		cin.get();

		return 0;
	}

	VideoCapture cap(0); // open the default camera

	if (!cap.isOpened())  // check if we succeeded
	{
		cout << "ERROR: There is no web-camera to connect!" << endl;
		CloseHandle(hNamedPipe);
		return -1;
	}

	//-- Выставляем параметры камеры ширину и высоту кадра в пикселях
	cap.set(CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(CAP_PROP_FRAME_HEIGHT, 960);

	Mat frame;

	DWORD   dwBytesRead = 0;     // для количества прочитанных байтов
	DWORD   dwBytesAvail = 0;    // для количества доступных байтов
	DWORD   dwBytesLeft = 0;    // для количества оставшихся байтов
	OVERLAPPED gOverlapped;

	vector<string> photos;
	while (true)
	{
		if (PeekNamedPipe(
			hNamedPipe,
			pchMessage,
			sizeof(pchMessage),
			&dwBytesRead,
			&dwBytesAvail,
			&dwBytesLeft)
			&& pchMessage[0] != '\0')
		{
			if (!ReadFile(hNamedPipe,
				&pchMessage,
				sizeof(pchMessage),
				&dwBytesRead,
				NULL))
			{
				cerr << "Data reading from the named pipe failed." << endl
					<< "The last error code: " << GetLastError() << endl;
				CloseHandle(hNamedPipe);
				break;
			}
			else if (pchMessage[0] == 48) //команда закончить работу
			{
				break;
			}

		}

		if (!cap.isOpened())  // check if we succeeded
		{
			cout << "ERROR: There is no web-camera to connect!" << endl;
			CloseHandle(hNamedPipe);
			return -1;
		}
		
		cap >> frame; //-- захватываем очередной кадр
		GetLocalTime(&st);
		
		CString cstrMessage;
		string filename;

		cstrMessage.Format("%d-%02d-%02d.%02d_%02d_%02d.%03d",
			st.wYear,
			st.wMonth,
			st.wDay,
			st.wHour,
			st.wMinute,
			st.wSecond,
			st.wMilliseconds);

		filename = cstrMessage + ".jpeg";

		string photo = experimentPath + '\\' + filename;
		imwrite(photo, frame); //--cохраняем в файл
		photos.push_back(photo);

	}
	string filePhotos = experimentPath + '\\' + "photos_log" + ".txt";
	std::ofstream out(filePhotos);
	for (auto photo : photos)
		out << photo << endl;
	out.close();

	cap.release();

	// закрываем дескриптор канала 
	CloseHandle(hNamedPipe);
	// завершаем процесс
	return 0;
}
