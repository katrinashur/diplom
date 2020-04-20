#include "EpocPlus.h"
#include <windows.h>
#include <iostream>

EpocPlus::EpocPlus(unsigned int userID)
{
	this->userID = userID;
	this->eState = IEE_EmoStateCreate();
	this->eEvent = IEE_EmoEngineEventCreate();
}

EpocPlus::~EpocPlus() {
	IEE_EmoStateFree(eState);
	IEE_EmoEngineEventFree(eEvent);
}

int EpocPlus::connect() {
	if (IEE_EngineConnect() != EDK_OK) {
		return EDK_FILE_ERROR;
	}
	else {
		int state;

		for (unsigned char a = 0; a < 50; a++) {

			state = IEE_EngineGetNextEvent(eEvent);

			if (state == EDK_OK)
			{
				IEE_Event_t eventType = IEE_EmoEngineEventGetType(eEvent);
				IEE_EmoEngineEventGetUserId(eEvent, &userID);

				if (eventType == IEE_UserAdded) {
					cout << "User added";
					IEE_FFTSetWindowingType(userID, IEE_HAMMING);
					ready = true;
				}
			}
			Sleep(5);
		}

		if (ready) {
			this->connectionStatus = true;
			return EDK_OK;
		}
		else
			return EDK_FILE_ERROR;
	}
}

int EpocPlus::disconnect() {
	if (IEE_EngineDisconnect() != EDK_OK) {
		return EDK_FILE_ERROR;
	}
	else {
		this->connectionStatus = false;
		return EDK_OK;
	}
}

bool EpocPlus::connected() {
	return this->connectionStatus;
}


vector <BrainWaves> EpocPlus::measuring() {

	vector<BrainWaves> brainWavesList;
	BrainWaves brainWaves;

	IEE_DataChannel_t channelList[] = { IED_AF3,                //!< Channel AF3 |0
										IED_F7,                 //!< Channel F7  |1
										IED_F3,                 //!< Channel F3  |2
										IED_FC5,                //!< Channel FC5 |3
										IED_T7,                 //!< Channel T7  |4
										IED_P7,                 //!< Channel P7  |5
										IED_Pz,                 //!< Channel Pz  |6
										IED_O1,                 //!< Channel O1  |7
										IED_O2,                 //!< Channel O2  |8
										IED_P8,                 //!< Channel P8  |9
										IED_T8,                 //!< Channel T8  |10
										IED_FC6,                //!< Channel FC6 |11
										IED_F4,                 //!< Channel F4  |12
										IED_F8,                 //!< Channel F8  |13
										IED_AF4                 //!< Channel AF4 |14
	};

	if (ready)
	{
		double alpha, low_beta, high_beta, gamma, theta;
		alpha = low_beta = high_beta = gamma = theta = 0;

		for (int i = 0; i < (int)(sizeof(channelList) / sizeof(channelList[0])); ++i)
		{
			int result = IEE_GetAverageBandPowers(userID, channelList[i], &theta, &alpha,
				&low_beta, &high_beta, &gamma);
			if (result == EDK_OK) {
				brainWaves.alpha = alpha;
				brainWaves.gamma = gamma;
				brainWaves.high_beta = high_beta;
				brainWaves.low_beta = low_beta;
				brainWaves.theta = theta;
				brainWavesList.push_back(brainWaves);
			}
		}
	}


	return brainWavesList;
}
