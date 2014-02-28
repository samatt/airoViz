//
//  oscReceiver.cpp
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//
#include "OscReceiver.h"


//class testApp;
OscReceiver::OscReceiver(){
    
}

void OscReceiver::setup(){
    receiver.setup(8000);
}
void OscReceiver::update(){
    while(receiver.hasWaitingMessages()){
		ofxOscMessage m;
		receiver.getNextMessage(&m);
        cout<<m.getAddress()<<endl;
		if(m.getAddress() == "/new"){
        
            string params = m.getArgAsString(0);
            AirodumpEventArgs args(params);
            ofNotifyEvent(events.nodeAdded, args);
		}
		else if(m.getAddress() == "/update"){
            string params = m.getArgAsString(0);
            AirodumpEventArgs args(params);
            ofNotifyEvent(events.nodeUpdated, args);
		}
		else if(m.getAddress() == "/remove"){

            string params = m.getArgAsString(0);
            AirodumpEventArgs args(params);
            ofNotifyEvent(events.nodeRemoved, args);
		}
        else if(m.getAddress() == "/quit"){
            cout<<"quit : "<<" : "<<m.getArgAsString(0)<<endl;
        }
	}
}

AirodumpEvents& OscReceiver::getEvents(){
    return events;
}