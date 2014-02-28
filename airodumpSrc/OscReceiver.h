//
//  oscReceiver.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//



#include "ofxOsc.h"
#include "ofMain.h"
#include "airodumpEvents.h"
#include "airodumpGlobals.h"



class OscReceiver{
public:
    OscReceiver();
    ofxOscReceiver receiver;
    void setup();
    void update();
    
    AirodumpEvents& getEvents();
    AirodumpEvents events;
};

