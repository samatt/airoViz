#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){

    receiver.setup();
    ofAddListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofAddListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofAddListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);


}

//--------------------------------------------------------------
void testApp::update(){
    receiver.update();
    
}

//--------------------------------------------------------------
void testApp::draw(){

    if(nodes.size()>0){

        ofBackground(0);
        x = 10;
        y = 10;
        for (int i =0; i<nodes.size(); i++) {
            ofColor c = ofColor(0, 0, 0);
            if(nodes[i].type == Router){
                c = ofColor::cyan;
            }
            else{
                c = ofColor::chartreuse;
                
//                if (nodes[i].probedESSID.size() <= 0 ) {
//                    continue;
//                }
            }
            
            float r = ofMap(nodes[i].Power, 10, 80, 5, 10);
            ofSetColor(c);
            ofCircle(x, y, r);
            
            if (nodes[i].type == Router) {
                ofSetColor(255);
                ofDrawBitmapString(nodes[i].ESSID, ofPoint(x,y));
            }
            else{
                ofSetColor(255);
                ofDrawBitmapString(nodes[i].BSSID,ofPoint(x,y));//probedESSID[ofRandom(nodes[i].probedESSID.size() - 1)], ofPoint(x,y));
            }
        
            y +=  30 ;
            
            if(y > ofGetHeight() -20){
                x += 200;
                y = 10;
                
            }
            
        }
        
    }
}
//--------------------------------------------------------------
void testApp::nodeAdded(AirodumpEventArgs& args){
//    Node n = ;
    nodes.push_back(Node(args.params));
//    Node* n1 = &nodes[nodes.size() -1];
    

    if(args.type == "Router"){
        routerMapIndex[args.BSSID] = nodes.size()-1;
    }
    else{
        clientMapIndex[args.BSSID] = nodes.size()-1;
    }
 
    cout<<"added  "<<args.type<<" : "<<args.BSSID<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){

    
    if(args.type == "Router"){
     
        if (routerMapIndex.find(args.BSSID) != routerMapIndex.end()) {
            nodes[routerMapIndex[args.BSSID]].updateNode(args.params);

        }
        else{
            ofLogError()<<" Router : "<<args.BSSID<< " not found. It shouldn't be updating"<<endl;
        }

    }
    else{
        if (clientMapIndex.find(args.BSSID) != clientMapIndex.end()) {
            nodes[clientMapIndex[args.BSSID]].updateNode(args.params);

        }
        else{
            ofLogError()<<" Client : "<<args.BSSID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    
    ofLog()<<"[ nodeUpdated ] "<<args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeRemoved(AirodumpEventArgs& args){
    cout<<"removed"<<endl;
    cout<<args.params<<endl;
    
    
}


//--------------------------------------------------------------
void testApp::exit(){
    ofRemoveListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofRemoveListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofRemoveListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);

}
//--------------------------------------------------------------
void testApp::keyPressed(int key){
//    cout<<clientMapIndex.size()<<endl;
    if(key == 'f'){
        ofToggleFullscreen();
    }
    
    if(key == ' '){
        for (int i = 0; i<nodes.size(); i++) {
            cout<<""
        }
    }
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){

}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){
//    AirodumpEventArgs args(" xxxxx ");
//    ofNotifyEvent(events.nodeAdded, args);
}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void testApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void testApp::dragEvent(ofDragInfo dragInfo){ 

}
