#include "opencv2/opencv.hpp"
#include <windows.h>
#include <stdio.h>
#include <fstream>
using namespace std;
using namespace cv;



int  main(int argc, char* argv[])
{
	HANDLE   hNamedPipe;
	char     pchMessage[1] = {};   // ��� ���������
	int    nMessageLength;   // ����� ���������
	char  pchResponse[80];
	int responseCode = 0;

	SYSTEMTIME st;
	VideoCapture cap(0); // open the default camera

	if (argc < 4)
	{
		cout << "Not enough arguments!" << endl;
		return -1;
	}

	string experimentPath(argv[3]);
	string experimentName(argv[2]);
	char pipeName[50];
	strcpy_s(pipeName, argv[1]);



	if (!cap.isOpened())  // check if we succeeded
	{
		cout << "ERROR: There is no web-camera to connect!" << endl;
		return -1;
	}

	//-- ���������� ��������� ������ ������ � ������ ����� � ��������
	cap.set(CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(CAP_PROP_FRAME_HEIGHT, 960);

	Mat frame;

	// ������� ����������� ����� ��� ������ � ������
	hNamedPipe = CreateNamedPipe(
		pipeName,  // ��� ������
		PIPE_ACCESS_INBOUND,        // ������ �� ������ 
		PIPE_TYPE_MESSAGE | PIPE_WAIT,   // ���������� �������� ���������
		1,         // ������������ ���������� ����������� ������ 
		0,         // ������ ��������� ������ �� ���������
		0,         // ������ �������� ������ �� ���������
		INFINITE,  // ������ ���� ����� ���������� �����
		NULL       // ������������ �� ���������
	);
	// ��������� �� �������� ��������
	if (hNamedPipe == INVALID_HANDLE_VALUE)
	{
		cerr << "Create named pipe failed." << endl
			<< "The last error code: " << GetLastError() << endl;
		cout << "Press any key to exit.";
		cin.get();

		return 0;
	}

	// ����, ���� ������ �������� � �������
	cout << "The server is waiting for connection with a client." << endl;
	if (!ConnectNamedPipe(
		hNamedPipe,    // ���������� ������
		NULL      // ����� ����������
	))
	{
		cerr << "Connect named pipe failed." << endl
			<< "The last error code: " << GetLastError() << endl;
		CloseHandle(hNamedPipe);
		cout << "Press any key to exit.";
		cin.get();

		return 0;
	}


	DWORD   dwBytesRead = 0;     // ��� ���������� ����������� ������
	DWORD   dwBytesAvail = 0;    // ��� ���������� ��������� ������
	DWORD   dwBytesLeft = 0;    // ��� ���������� ���������� ������

	vector<string> photos;
	while (true)
	{
		if (!PeekNamedPipe(
			hNamedPipe,
			pchMessage,
			sizeof(pchMessage),
			&dwBytesRead,
			&dwBytesAvail,
			&dwBytesLeft)
			&& pchMessage[0] != 0)
		{
			cerr << "Data reading from the named pipe failed." << endl
			<< "The last error code: " << GetLastError() << endl;
			CloseHandle(hNamedPipe);
		}
		else if(pchMessage[0] != '\0') //������� ��������� ������
		{
			// ������� ���������� �� ������� ��������� �� �������
			cout << "The server received the message from a client: " << endl;
			cout << pchMessage[0] << endl;
			break;
		}

		cap >> frame; //-- ����������� ��������� ����
		GetLocalTime(&st);

		string filename = to_string(st.wYear) + "-" + to_string(st.wMonth) + "-" + to_string(st.wDay) + "." +
			to_string(st.wHour) + "_" + to_string(st.wMinute) + "_" + to_string(st.wSecond) + "." + to_string(st.wMilliseconds) + ".jpeg";
		string photo = experimentPath + '\\' + filename;
		imwrite(photo, frame); //--c�������� � ����
		photos.push_back(photo);

	}
	string filePhotos = experimentPath + '\\' + experimentName + ".txt";
	std::ofstream out(filePhotos);
	for (auto photo : photos)
		out << photo << endl;
	out.close();

	// ��������� ���������� ������ 
	CloseHandle(hNamedPipe);
	// ��������� �������
	return 0;
}
