#pragma once
#include "BrainWaves.h"
#include <vector>

#include "IEmoStateDLL.h"
#include "Iedk.h"
#include "IedkErrorCode.h"
using namespace std;


class EpocPlus
{
public:
	EpocPlus(unsigned int userID);
	~EpocPlus();
	int connect();
	int disconnect();
	bool connected();
	vector <BrainWaves> measuring();

private:
	EmoEngineEventHandle eEvent;
	EmoStateHandle eState;
	bool ready = false;
	bool connectionStatus = false;
	unsigned int userID;

};

