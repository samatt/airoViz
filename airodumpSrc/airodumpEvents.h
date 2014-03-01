//
//  airodumpEvents.h
//  airodumpRealTime
//
//  Created by Surya Mattu on 2/28/14.
//
//

#pragma once
#include "ofMain.h"

//Placer 
class AirodumpEventArgs : public ofEventArgs {
public:
	AirodumpEventArgs(string params,string BSSID, string type): params(params),BSSID(BSSID),type(type){}
	
	string params;
    string BSSID;
    string type;
};

class AirodumpEvents{

public:

    ofEvent<AirodumpEventArgs> nodeAdded;
    ofEvent<AirodumpEventArgs> nodeUpdated;
	ofEvent<AirodumpEventArgs> nodeRemoved;
};


//void RegisterAirodumpEvents(ListenerClass * listener){
//	ofAddListener(nodeAdded, listener, &ListenerClass::interactionMoved);
//	ofAddListener(GetCloudsInput()->getEvents().interactionStarted, listener, &ListenerClass::interactionStarted);
//	ofAddListener(GetCloudsInput()->getEvents().interactionDragged, listener, &ListenerClass::interactionDragged);
//	ofAddListener(GetCloudsInput()->getEvents().interactionEnded, listener, &ListenerClass::interactionEnded);
//}