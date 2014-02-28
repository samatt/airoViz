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

}
//--------------------------------------------------------------
void testApp::nodeAdded(AirodumpEventArgs& args){
    cout<<"added"<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){
    cout<<"updated"<<endl;
    cout<<args.params<<endl;
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
