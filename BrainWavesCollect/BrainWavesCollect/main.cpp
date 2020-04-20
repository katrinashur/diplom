#include "EpocPlus.h"
#include <iostream>
#include <string>
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


 void measuring(EpocPlus *epoc, vector <BrainWaves> &dataEEG) {

	 //timer->stop();
	 if (epoc->connected() == false) {
		 //cout <<  "Error: Include EMOTIV EPOC";
		 return;
	 }

	 dataEEG = epoc->measuring();

	 //updateTable();
	 //updatePlot();

	 //timer->start(1 / ui->period->value() * 1000);
 }

 int main()
 {
	 EpocPlus *epoc = new EpocPlus(1);
	 cout << connectEpoc(epoc) << endl;

	 vector <BrainWaves> dataEEG;
	 measuring(epoc, dataEEG);

	 return 0;
 }