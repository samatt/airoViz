#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){
    
    ofEnableAlphaBlending();
    receiver.setup();
    currentMode = 0;
    ofAddListener(receiver.getEvents().nodeAdded, this, &testApp::nodeAdded);
    ofAddListener(receiver.getEvents().nodeUpdated, this, &testApp::nodeUpdated);
    ofAddListener(receiver.getEvents().nodeRemoved, this, &testApp::nodeRemoved);
    
    gui = new ofxUISuperCanvas("SUPER COMPACT", OFX_UI_FONT_MEDIUM);
    gui->addFPS();
    
    maxPower = 0;
    minPower = INT_MAX;

    gui->addSpacer();
    gui->addIntSlider("Router X :", -10, 20, &routerX);
    gui->addIntSlider("RouterY :", -8000, 100, &routerY);
    gui->addIntSlider("Router Width : ", 100, 800, &routerWidth);
    gui->addIntSlider("Router Height : ", 20, 200, &routerHeight);
    gui->addIntSlider("MAX DURATION : ", 10, 3600, &maxDuration);
    gui->addToggle("Show Duration", &showDuration);
    gui->addSpacer();
    gui->addToggle("Show Duration", &showSSIDs);
    gui->addToggle("Show Duration", &showPower);
    gui->addSpacer();
    gui->addIntSlider("Client X :", -10, 200, &clientX);
    gui->addIntSlider("ClientY :", -18000, 100, &clientY);
    gui->addIntSlider("client Width : ", 100, 800, &clientWidth);
    gui->addIntSlider("client Height : ", 20, 200, &clientHeight);
    gui->autoSizeToFitWidgets();
    gui->loadSettings("GUI/guiSettings.xml");
    ofAddListener(gui->newGUIEvent,this,&testApp::guiEvent);
}

//--------------------------------------------------------------
void testApp::update(){
    receiver.update();
    //    updateIndices();
    
    int rX = routerX;
    int rY = routerY;
    int cX = clientX;
    int cY = clientY;
    for(int i =0; i<nodes.size(); i++){
        Node& n = nodes[i];
        
        n.updateDuration();
        //TODO: Add check for duration
        if (n.type == Router) {
            
            if (routerPos.find(n.BSSID) == routerPos.end() ) {
                continue;
            }
            routerPos[n.BSSID] = ofPoint(rX,rY);
            rX +=  routerWidth ;
            
            if(rX > ofGetWidth() -90){
                rX  = routerX;
                rY += routerHeight;
                
            }
            
        }
        else{

            //check if there is a link bertween the current client and its associated AP
            if( ! ofContains(routerClientLinks[n.AP],i)){
                
                routerClientLinks[n.AP].push_back(i);
            }
            
            if (clientPos.find(n.BSSID) == clientPos.end() ) {
                continue;
            }
            
            clientPos[n.BSSID]=ofPoint(cX,cY);
            cX  += clientWidth;
            if(cX > ofGetWidth() -90){
                cX  = clientX;
                cY += clientHeight;
                
            }
        }
    }
    
}

//--------------------------------------------------------------
void testApp::draw(){
    
    ofBackground(0);
    x = 20;
    y = 10;
    if (currentMode == 0) {
        for (int i =0; i<nodes.size(); i++) {
            
            if (nodes[i].type == Client) {
                continue;
            }
            
            Node& router = nodes[i];
            
            stringstream ss;
            
            if (showESSIDs) {
                ofSetColor(ofColor::lightSkyBlue);
                ofDrawBitmapString(router.ESSID +"\n", routerPos[router.BSSID]);
            }
            else{
                ofSetColor(ofColor::lightSkyBlue);
                ofDrawBitmapString(router.BSSID +"\n", routerPos[router.BSSID]);
                
            }

            
        
            if(!showSSIDs) continue;
            
            vector<int> clientIndex = routerClientLinks[router.BSSID];
            
            if (clientIndex.size() == 0) {
                ofSetColor(ofColor::grey);
                ss<<"\nNo Clients"<<endl;
                ofDrawBitmapString(ss.str(), routerPos[router.BSSID]);
                continue;
            }
            
            for (int j = 0 ; j<clientIndex.size(); j++) {
                string ID;
                if(j == 0){
                 ID= "\n";
                }
                else{
                    for (int k = 0 ; k<j; k++) {
                        if(k == 0){
                            ID += "\n\n";
                        }
                        else{
                            ID += "\n";
                        }
                    }
                }

                ID += nodes[clientIndex[j]].BSSID ;
                
                if(showDuration){
                    ID += " "+ofToString(nodes[clientIndex[j]].getDurationString()) + "\n";
                }
                else if(showPower){
                    ID += " "+ofToString(nodes[clientIndex[j]].Power) + "\n";
                }
                else{
                    ID += "\n";
                }
                
                ofSetColor(255, 255, 255);
                //            float hue = ofMap(nodes[clientIndex[j]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
                int alpha = ofMap(nodes[clientIndex[j]].getDuration(), 0, maxDuration, 0, 200,true);
                ofColor c1;
//                cout<<nodes[clientIndex[j]].getDuration()   <<" : "<<alpha<<endl;
                ofSetColor(255,255,255, 255 -alpha );
                ofDrawBitmapString(ID, routerPos[router.BSSID]);
            }
            
        }
        
    }
    else if (currentMode ==1){
        for (int i =0; i<nodes.size(); i++) {
            
            if(nodes[i].type == Router){
                continue;
            }
            
            Node& client = nodes[i];



            if(showPower){
                ofColor c = ofColor(129,228,252);
                ofxEasingCubic easing;
                ofxEasingArgs a;
                float sat =ofxTween::map((float)client.Power, 20, maxPower, 10 ,240., true, ofxEasingCubic(), ofxTween::easeIn);
                c.setSaturation(sat);
                ofSetColor(c);
                
                ofDrawBitmapString(client.BSSID , clientPos[client.BSSID]);
                ofDrawBitmapString( "                "+ofToString(client.Power)+"\n", clientPos[client.BSSID].x + client.BSSID.length() + 1, clientPos[client.BSSID].y);
            }
            else{

                ofColor c = ofColor(129,228,252);
                ofxEasingCubic easing;
                ofxEasingArgs a;
                float sat =ofxTween::map((float)client.Power, -maxPower, -20 , 10 ,235, true, ofxEasingCubic(), ofxTween::easeIn);
                c.setSaturation(sat);
                ofSetColor(c);

                ofDrawBitmapString(client.BSSID + "\n" , clientPos[client.BSSID]);
            }
            
            if(!showSSIDs) continue;
            
            vector<string>& probedIDs = client.probedESSID;
            
            if (probedIDs.size() == 1 && probedIDs[0] == " ") {
                ofSetColor(ofColor::grey);

                ofDrawBitmapString("\nNo Stations Found yet", clientPos[client.BSSID]);
                continue;
                
            }
            
            for (int j = 0; j < probedIDs.size() ; j++) {
                string ID;
                if(j == 0)ID= "\n";
                
                for (int k = 0 ; k<j; k++) {
                    if(k == 0){
                        ID += "\n\n";
                    }
                    else{
                        ID += "\n";
                    }
                }
                
                ID += trim(probedIDs[j]);


                ofColor c1;
                
                ofSetColor(255,255,255,255);
                ofDrawBitmapString(ID, clientPos[client.BSSID]);
            }
        }
    }
}
//--------------------------------------------------------------
void testApp::nodeAdded(AirodumpEventArgs& args){
    
    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        if(routerMapIndex.find(ID) == routerMapIndex.end()){
            routerMapIndex[ID] = nodes.size();
        }
        else{
            ofLogError()<<"Duplicate router ignoring"<<endl;
        }
    }
    else{
        
        if (clientMapIndex.find(ID) ==  clientMapIndex.end()) {
            
            clientMapIndex[ID] = nodes.size();
        }
        else{
            ofLogError()<<"Duplicate router ignoring"<<endl;
        }
        
    }
    
    Node cur = Node(args.params);
    
    //TODO: Make less clunky. Figure out how to incoroporate this properly
    if(routerMapIndex.find(cur.AP) != routerMapIndex .end()){
        cur.indexAP = routerMapIndex[nodes[nodes.size() -1].AP];
    }
    else{
        ofLogError()<<" [Node Added] "<<" router index not found for "<<cur.BSSID<<endl;
    }
    
    
    nodes.push_back(cur);
    
    maxPower = MAX(cur.Power,maxPower);
    minPower  = MIN(cur.Power, minPower);
    
    cout<<"added  "<<args.type<<" : "<<ID<<endl;//args.params<<endl;
}
//--------------------------------------------------------------
void testApp::nodeUpdated(AirodumpEventArgs& args){
    
    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        
        if (routerMapIndex.find(ID) != routerMapIndex.end()) {
            int index = routerMapIndex[ID];
            nodes[index].updateNode(args.params);
            maxPower = MAX(nodes[index].Power,maxPower);
            minPower  = MIN(nodes[index].Power, minPower);
        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].updateNode(args.params);
            maxPower = MAX(nodes[index].Power,maxPower);
            minPower  = MIN(nodes[index].Power, minPower);
            //Updating linked router for current client
            
            if(routerMapIndex.find(nodes[index].AP) != routerMapIndex .end()){
                nodes[index].indexAP = routerMapIndex[nodes[index].AP];
            }
            else{
                ofLogError()<<" [Node Updated] "<<" router index not found for "<<nodes[index].BSSID<<endl;
            }
            
            
        }
        else{
            ofLogError()<<" Client : "<<ID<< " not found. It shouldn't be updating"<<endl;
        }
    }

    ofLog()<<"[ nodeUpdated ] "<<args.params<<endl;
}

//--------------------------------------------------------------
void testApp::nodeRemoved(AirodumpEventArgs& args){
    string ID = trim(args.BSSID);
    if(args.type == "Router"){
        
        if (routerMapIndex.find(ID) != routerMapIndex.end()) {
            int index = routerMapIndex[ID];
            nodes[index].alive = false;
            cout<<"node dead : "<<nodes[index].type<<endl;
        }
        else{
            ofLogError()<<" Router : "<<ID<< " not found. It shouldn't be removing"<<endl;
        }
        
    }
    else{
        if (clientMapIndex.find(ID) != clientMapIndex.end()) {
            int index = clientMapIndex[ID];
            nodes[index].alive = false;
        }
        else{
            ofLogError()<<" Client : "<<ID<< " not found. It shouldn't be removing"<<endl;
        }
    }
    
    ofLog()<<"[ nodeRemoved ] "<<ID<<endl;
    
    
}

//--------------------------------------------------------------
void testApp::updateIndices(){
    activeNodes.clear();
    numAliveClients = 0;
    numAliveRouters = 0;
    routerClientLinks.clear();
    int x = 0 ;
    for (int i =0 ; i<nodes.size(); i++) {
        
        nodes[i].updateDuration();
        if (nodes[i].type == Router) {
            
            numAliveRouters++;
        }
        else{
            
            routerClientLinks[nodes[i].AP].push_back(activeNodes.size());
            numAliveClients++;
        }
        
        if (nodes[i].alive) {
            activeNodes.push_back(i);
        }
        else{
            x++;
        }
    }
        
    //    cout<<"num nodes removed:"<<x<<endl;
}

//--------------------------------------------------------------
void testApp::exit(){
    gui->saveSettings("GUI/guiSettings.xml");
    delete gui;
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
    
    
    if (key == '1') {
        currentMode = 0;
    }
    
    if (key =='2') {
        currentMode = 1;
    }
    if(key == 'h'){
        gui->toggleVisible();
    }
    if(key =='t'){
        gui->toggleMinified();
    }
    
    if(key == OF_KEY_UP){
        if (currentMode == 0) {
            routerY-= 100;
        }
        else{
            clientY-= 100;
        }
    }
    
    if(key == OF_KEY_DOWN){
        if (currentMode == 0) {
            routerY+=100;
        }
        else{
            clientY+= 100;
        }
    }
    
    if(key == OF_KEY_LEFT){
        if (currentMode == 0) {
            routerHeight-=10;
        }
        else{
            clientHeight-= 10;
        }
        
    }
    
    if(key == OF_KEY_RIGHT){
        if (currentMode == 0) {
            routerHeight+=10;
        }
        else{
            clientHeight+= 10;
        }
        
    }
    
    if(key =='d'){
        showDuration = !showDuration;
    }
    
    if(key =='m'){
        showSSIDs = !showSSIDs;
    }
    
    if (key == ' ') {
//        cout<<clientX<<" : "<<clientY<<" : "<<clientWidth<<" : "<<clientHeight<<endl;

    }
    
    if(key =='r'){
        resetGrid();
    }

    if(key == 'p'){
        showPower = !showPower;
    }
    
    if(key == 'e'){
        showESSIDs = !showESSIDs;
    }
}

void testApp::resetGrid(){
    routerX = 57;
    routerY = 300;
    routerWidth = 200;
    routerHeight = 10;
    clientX = 57;
    clientY = 300;
    clientWidth = 200;
    clientHeight = 10;
}

void testApp::guiEvent(ofxUIEventArgs& args){
    
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


//    for(int i =0; i<activeNodes.size(); i++){
//
//        Node& n = nodes[activeNodes[i]];
//
//        if (n.type == Router) {
//            routerPos[n.BSSID] = ofPoint(routerX,routerY);
//        }
//
//        routerX +=  200 ;
//
//        if(routerX > ofGetWidth() -90){
//            routerX  = 20;
//            routerY += 100;
//
//        }
//    }
//
//    for (int i =0; i<activeNodes.size(); i++) {
//        Node& n  = nodes[activeNodes[i]];
//
//        if (n.type == Router) {
//            stringstream ss;
//
//            ofSetColor(ofColor::lightSkyBlue);
//            //                ss<<n.ESSID<<endl;
//            ofDrawBitmapString(n.ESSID +"\n", routerPos[n.BSSID]);
//            vector<int> cIdx = routerClientLinks[n.BSSID];
//            if (cIdx.size() == 0) {
//                ofSetColor(ofColor::grey);
//                ss<<"\nNo Clients"<<endl;
//                ofDrawBitmapString(ss.str(), routerPos[n.BSSID]);
//
//            }
//            else{
//
//                string ID = "\n" + nodes[activeNodes[cIdx[0]]].BSSID;
//                ID += " : "+ofToString(nodes[activeNodes[cIdx[i]]].duration);
//
//                float hue = ofMap(nodes[activeNodes[cIdx[i]]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
//                ofColor c1;
//                c1.setHsb(hue, 128, 128);
//                ofSetColor(c1);
//
//                ofDrawBitmapString(ID, routerPos[n.BSSID]);
//
//                for (int i = 1 ; i<cIdx.size(); i++) {
//
//                    string ID;
//                    ID= "\n\n";
//                    for (int j = 1 ; j<i; j++) {
//                        ID += "\n";
//                    }
//
//                    ID += nodes[activeNodes[cIdx[i]]].BSSID;
//                    ID += " : "+ofToString(nodes[activeNodes[cIdx[i]]].duration);
//                    float hue = ofMap(nodes[activeNodes[cIdx[i]]].getDuration(), 0, 500, ofColor::red.getHue(), ofColor::blue.getHue());
//                    ofColor c1;
//                    //                        cout<<hue<<","<<n.getDuration()<<endl;
//                    c1.setHsb(hue, 128, 128);
//                    ofSetColor(c1);
//
//                    ofDrawBitmapString(ID, routerPos[n.BSSID]);
//                }
//            }
//        }
//    }
//        for (int i =0; i<activeNodes.size(); i++) {
//            int index = activeNodes[i];
//            cout<<nodes[index].type<<endl;

//            ofColor c = ofColor(0, 0, 0);
//            if(nodes[index].type == Router){
//
//                c = ofColor::blueSteel;
//            }
//            else{
//                c = ofColor::chartreuse;
//
//                if (nodes[index].probedESSID[0] ==" " ) {
//                    continue;
//                }
//            }
//
//            ofSetColor(c);
//            ofCircle(x, y, 1);
//
//            if (nodes[index].type == Router) {
//                ofSetColor(c);
//                ofDrawBitmapString(nodes[index].ESSID, ofPoint(x,y));
//            }
//            else{
//                ofSetColor(c);
//                if (nodes[index].AP == " ") {
//                    ofDrawBitmapString(nodes[index].probedESSID[nodes[index].probedESSID.size() - 1], ofPoint(x,y));
//                }
//                else{
//                    string routerID = nodes[index].AP;
//                    int routerIndex = routerMapIndex[routerID];
//                    string networkName = nodes[routerIndex].ESSID;
//                    ofDrawBitmapString(nodes[index].BSSID + "\n" + networkName, ofPoint(x,y));
//                    ofSetColor(ofColor::white);
//                    ofDrawBitmapString("\n" + networkName, ofPoint(x,y));
//                }
//
//            }
//
//            y +=  30 ;
//
//            if(y > ofGetHeight() -20){
//                x += 180;
//                y = 10;
//
//            }
//
//        }
//
//    }
