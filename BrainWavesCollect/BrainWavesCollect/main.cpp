#include "EpocPlus.h"
#include <iostream>
#include <string>
#include <fstream>
#include <windows.h>
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


 void measuring(EpocPlus *epoc, vector <BrainWaves> &dataEEG)
 {
	 Sleep(3000);
	 for (int i =0; i < 10000; i++)
	 {
		 vector <BrainWaves> dataTmp = epoc->measuring();
		 if (dataTmp.size() > 0)
			 cout << "Там что-то есть!" << endl;
		 for (auto element : dataTmp)
		 {
			 dataEEG.push_back(element);
		 }	 
	 }
	 
 }


 void writeDataInFile(vector <BrainWaves> dataEEG)
{
	 std::ofstream out;          // поток для записи
	 out.open("nameExperiment.tsv"); // окрываем файл для записи
	 vector <string> channels = { "AF3", "F7", "F3", "FC5", "T7", "P7", "Pz", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4" };
	 vector <string> rythms = { "theta", "alpha", "lowBeta", "highBeta", "gamma" };


	 if (out.is_open())
	 {
		 out << string("#\t");
		 for (auto channel : channels)
		 {
			 for (auto rythm : rythms)
			 {
				 out << channel << "_" << rythm << "\t";
			 }
		 }
		 out << string("\r\n");

		 for (int i = 0; i < dataEEG.size() / channels.size(); i++) 
		 {
			 out << i << "\t";
			 for (int j = 0; j < channels.size(); j++) {
				 BrainWaves waves = dataEEG.at(i * channels.size() + j);
				 out << waves.theta << "\t" << waves.alpha << "\t" << waves.low_beta << "\t" <<  waves.high_beta << "\t" << waves.gamma << "\t";
			 }
			 out << "\r\n";
		 }
		 out.close();
	 }
}

 int main()
 {
	 EpocPlus *epoc = new EpocPlus(1);
	 cout << connectEpoc(epoc) << endl;

	 vector <BrainWaves> dataEEG;
	 measuring(epoc, dataEEG);

	 writeDataInFile(dataEEG);

	 return 0;
 }