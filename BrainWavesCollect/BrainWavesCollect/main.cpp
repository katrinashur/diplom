#include "EpocPlus.h"
#include <iostream>
#include <string>
#include <fstream>
#include <queue>
#include <windows.h>
#include <thread>
using namespace std;



 string connectEpoc(EpocPlus *epoc)
{
	if (epoc->connected() == false) {
		if (epoc->connect() != EDK_OK) {
			return "ERROR: Headset is not detected!";
		}
		else {
			return "Connection is settled.";
		}
	}
	else {
		if (epoc->disconnect() != EDK_OK) {
			return "ERROR: Headset is not detected!";
		}
		else {
			return "Disconnection";
		}
	}

}


 void writeDataInFile(vector <BrainWaves> dataEEG, vector<string> times, string filename)
{
	 std::ofstream out(filename); // �������� ���� ��� ������
	 vector <string> channels = { "AF3", "F7", "F3", "FC5", "T7", "P7", "Pz", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4" };
	 vector <string> rythms = { "theta", "alpha", "lowBeta", "highBeta", "gamma" };


	 if (out.is_open())
	 {
		 out << "#\t";
		 for (auto channel : channels)
		 {
			 for (auto rythm : rythms)
			 {
				 out << channel << "_" << rythm << "\t";
			 }
		 }
		 out << "time" << "\n";

		 for (int i = 0; i < dataEEG.size() / channels.size(); i++) 
		 {
			 out << i << "\t";
			 for (int j = 0; j < channels.size(); j++) {
				 BrainWaves waves = dataEEG.at(i * channels.size() + j);
				 out << waves.theta << "\t" << waves.alpha << "\t" << waves.low_beta << "\t" <<  waves.high_beta << "\t" << waves.gamma << "\t";
			 }
			 out << times.at(i) << "\n";
		 }
		 out.close();
	 }
}


 int  main(int argc, char* argv[])
 {
	 HANDLE   hNamedPipe;

	 if (argc < 4)
	 {
		 cout << "Not enough arguments!" << endl;
		 return -1;
	 }

	 string experimentPath(argv[3]);
	 string experimentName(argv[2]);
	 char pipeName[50];
	 strcpy_s(pipeName, argv[1]);
	 
	 

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

	 EpocPlus *epoc = new EpocPlus(1);
	 cout << connectEpoc(epoc) << endl;

	 vector <BrainWaves> dataEEG;

	 DWORD   dwBytesRead = 0;     // ��� ���������� ����������� ������
	 DWORD   dwBytesAvail = 0;    // ��� ���������� ��������� ������
	 DWORD   dwBytesLeft = 0;    // ��� ���������� ���������� ������

	 char     pchMessage[1] = {};   // ��� ���������

	 vector<string> times;
	 Sleep(3000);
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
		 else if (pchMessage[0] != '\0') //������� ��������� ������
		 {
			 // ������� ���������� �� ������� ��������� �� �������
			 cout << "The server received the message from a client: " << endl;
			 cout << pchMessage[0] << endl;
			 break;
		 }
		 vector <BrainWaves> tmp = epoc->measuring();
		 SYSTEMTIME st;
		 GetLocalTime(&st);
		 string ms = to_string((double)st.wMilliseconds / 1000);
		 ms = ms.substr(2, 3);
		 times.push_back(to_string(st.wYear) + "-" + to_string(st.wMonth) + "-" + to_string(st.wDay) + "." +
			 to_string(st.wHour) + "_" + to_string(st.wMinute) + "_" + to_string(st.wSecond) + "." + ms);
		 dataEEG.insert(dataEEG.end(), tmp.begin(), tmp.end()); //15 �������, � ������ 5 ������
		 Sleep(1000/90);
	 }
	 string filepath = experimentPath + '\\' + experimentName + ".tsv";
	 writeDataInFile(dataEEG, times, filepath);

	 // ��������� ���������� ������ 
	 CloseHandle(hNamedPipe);

	 return 0;
 }