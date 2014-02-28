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
        // cout<<"has message"<<endl;
		ofxOscMessage m;
		receiver.getNextMessage(&m);
        
		if(m.getAddress() == "/new"){

//            cout<<currentTopic<<" : "<<m.getArgAsString(3)<<endl;
            
		}
		else if(m.getAddress() == "/update"){

		}
		else if(m.getAddress() == "/remove"){

		}
        else if(m.getAddress() == "/quit"){

        }
	}
}