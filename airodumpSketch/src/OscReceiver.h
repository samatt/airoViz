//
//  oscReceiver.h
//  airodumpSketch
//
//  Created by Surya Mattu on 2/28/14.
//
//

#ifndef __airodumpSketch__oscReceiver__
#define __airodumpSketch__oscReceiver__


#include "ofxOsc.h"
#include "ofMain.h"



class OscReceiver{
public:
    OscReceiver();
    ofxOscReceiver receiver;
    void update();
    
};

#endif /* defined(__airodumpSketch__oscReceiver__) */
