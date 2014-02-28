//
//  oscReceiver.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//



#include "ofxOsc.h"
#include "ofMain.h"



class OscReceiver{
public:
    OscReceiver();
    ofxOscReceiver receiver;
    void update();
    
};

