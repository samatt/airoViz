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
//        cout<<m.getAddress()<<endl;
		if(m.getAddress() == "/new"){
        
            string type = m.getArgAsString(0);
            string params = m.getArgAsString(1);
            string BSSID = m.getArgAsString(2);
            AirodumpEventArgs args(params,BSSID,type);
            ofNotifyEvent(events.nodeAdded, args);
		}
		else if(m.getAddress() == "/update"){
            string type = m.getArgAsString(0);
            string params = m.getArgAsString(1);
            string BSSID = m.getArgAsString(2);
            AirodumpEventArgs args(params,BSSID,type);
            ofNotifyEvent(events.nodeUpdated, args);
		}
		else if(m.getAddress() == "/remove"){

            string type = m.getArgAsString(0);
            string params = m.getArgAsString(1);
            string BSSID = m.getArgAsString(2);
            AirodumpEventArgs args(params,BSSID,type);
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