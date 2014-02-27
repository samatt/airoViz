#pragma once

#include "ofMain.h"
#include "Node.h"
#include <fstream>
#include <iostream>

class testApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
    
        vector<Node> nodes;
        int maxPower, minPower;
        ofVec2f currentPos;
        int x,y;
        ofFile dataFile;
        ofBuffer buffer;
//        Poco::File file;
//    std::ifstream  stream()//"/Users/surya/Desktop/Kali/sharedTest1-01.csv");
    std::ifstream ifs;// ("test.txt", std::ifstream::in);
};
