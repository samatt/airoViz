//
//  oscReceiver.cpp
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//
#include "OscReceiver.h"

OscReceiver::OscReceiver(){
    receiver.setup(5656);
}

void OscReceiver::update(){
    while(receiver.hasWaitingMessages()){
//        cout<<"has message"<<endl;
		ofxOscMessage m;
//        m.get
		receiver.getNextMessage(&m);
//        cout<<m.getAddress()<<endl;
		if(m.getAddress() == "/new"){
        
            cout<<"new :"<<m.getArgAsString(0)<<endl;
            
		}
		else if(m.getAddress() == "/update"){
            cout<<"update :"<<m.getArgAsString(0)<<endl;
		}
		else if(m.getAddress() == "/remove"){
            cout<<"update : "<<m.getArgAsString(0)<<endl;
		}
        else if(m.getAddress() == "/quit"){
            cout<<"quit : "<<" : "<<m.getArgAsString(0)<<endl;
        }
	}
}